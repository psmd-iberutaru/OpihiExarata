"""
The manual GUI window.
"""

import sys
import os

from PySide6 import QtCore, QtWidgets, QtGui

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import opihiexarata
import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

import opihiexarata.astrometry as astrometry
import opihiexarata.photometry as photometry
import opihiexarata.propagate as propagate
import opihiexarata.orbit as orbit
import opihiexarata.ephemeris as ephemeris

import opihiexarata.gui as gui


class OpihiManualWindow(QtWidgets.QMainWindow):
    """The GUI that is responsible for interaction between the user and the
    two Opihi solutions, the image (OpihiPreprocessSolution) and the
    results (OpihiSolution).

    Only non-GUI attributes are listed here.

    Attributes
    ----------
    asteroid_set_name : string
        The current asteroid name provided by the user.
    raw_fits_filename : string
        The raw input filename. This file is usually preprocessed before
        analysis.
    raw_record_filename : string
        The raw MPC record filename. This contains historical asteroid
        information collected (with the unique identifier being the name).
    process_fits_filename : string
        The filename of the preprocessed image, this is generally generated
        automatically by the preprocess solution. This file is generally used
        for analysis.
    automatic_fetch_directory : string
        The directory where fits files are to be automatically fetched from.
        Getting a file using the manual method updates this to the directory
        of the manual file.
    preprocess_solution : OpihiPreprocessSolution
        The preprocessing solution which is used to convert raw images to
        preprocessed files.
    opihi_solution : OpihiSolution
        The general OpihiExarata solution, the collection class of all other
        solutions.
    """

    def __init__(self) -> None:
        """The manual GUI window for OpihiExarata. This interacts directly
        with the total solution object of Opihi.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Creating the GUI itself using the Qt framework and the converted
        # Qt designer files.
        super(OpihiManualWindow, self).__init__()
        self.ui = gui.qtui.Ui_ManualWindow()
        self.ui.setupUi(self)
        # Window icon, we use the default for now.
        gui.functions.apply_window_icon(window=self, icon_path=None)

        # Establishing the defaults for all of the relevant attributes.
        self.asteroid_set_name = None
        self.raw_fits_filename = None
        self.raw_record_filename = None
        self.process_fits_filename = None
        self.automatic_fetch_directory = None
        self.preprocess_solution = None
        self.opihi_solution = None

        # The automatic fetching directory default is stored in the
        # configuration file.
        AF_DIR = library.config.GUI_MANUAL_INITIAL_AUTOMATIC_IMAGE_FETCHING_DIRECTORY
        if os.path.isdir(AF_DIR):
            self.automatic_fetch_directory = AF_DIR
        else:
            self.automatic_fetch_directory = None

        # Preparing the image area for Opihi sky images.
        self.__init_opihi_image()

        # Preparing the buttons, GUI, and other functionality.
        self.__init_gui_connections()

        # Preparing the preprocessing solution so that the raw files loaded
        # into Exarata can be instantly turned into reduced images.
        self.__init_preprocess_solution()

        # All done.
        return None

    def __init_gui_connections(self) -> None:
        """Assign the action bindings for the buttons which get new
        file(names).

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # The new file and new object buttons.
        self.ui.push_button_new_image_automatic.clicked.connect(
            self.__connect_push_button_new_image_automatic
        )
        self.ui.push_button_new_image_manual.clicked.connect(
            self.__connect_push_button_new_image_manual
        )
        self.ui.push_button_new_target.clicked.connect(
            self.__connect_push_button_new_target
        )

        # The window and plot refresh button.
        self.ui.push_button_refresh_window.clicked.connect(
            self.__connect_push_button_refresh_window
        )

        # Astrometry-specific buttons.
        self.ui.push_button_astrometry_solve_astrometry.clicked.connect(
            self.__connect_push_button_astrometry_solve_astrometry
        )
        self.ui.push_button_astrometry_custom_solve.clicked.connect(
            self.__connect_push_button_astrometry_custom_solve
        )

        # Photometry-specific buttons.
        self.ui.push_button_photometry_solve_photometry.clicked.connect(
            self.__connect_push_button_photometry_solve_photometry
        )

        # Orbit-specific buttons.
        self.ui.push_button_orbit_solve_orbit.clicked.connect(
            self.__connect_push_button_orbit_solve_orbit
        )

        # Ephemeris-specific buttons.
        self.ui.push_button_ephemeris_solve_ephemeris.clicked.connect(
            self.__connect_push_button_orbit_solve_ephemeris
        )

        # Propagate-specific buttons.
        self.ui.push_button_propagate_solve_propagation.clicked.connect(
            self.__connect_push_button_propagate_solve_propagation
        )
        self.ui.push_button_propagate_custom_solve.clicked.connect(
            self.__connect_push_button_propagate_custom_solve
        )

    def __init_opihi_image(self) -> None:
        """Create the image area which will display what Opihi took from the
        sky. This takes advantage of a reserved image vertical layout in the
        design of the window.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Deriving the size of the image from the filler dummy image. The
        # figure should be a square. (Height really is the primary concern.)
        pix_to_in = lambda p: p / plt.rcParams["figure.dpi"]
        dummy_edge_size = self.ui.dummy_opihi_image.height()
        edge_size = pix_to_in(dummy_edge_size)
        # The figure, canvas, and navigation toolbar of the image plot
        # using a Matplotlib Qt widget backend. We will add these to the
        # layout later.
        fig, ax = plt.subplots(figsize=(edge_size, edge_size), constrained_layout=True)
        self.opihi_figure = fig
        self.opihi_axes = ax
        self.opihi_canvas = FigureCanvas(self.opihi_figure)
        self.opihi_nav_toolbar = NavigationToolbar(self.opihi_canvas, self)

        # For ease of usage, a custom navigation bar coordinate formatter
        # function/class is used.
        class CoordinateFormatter:
            """A simple function class to properly format the navigation bar
            coordinate text. This assumes the current structure of the GUI."""

            def __init__(self, gui_instance: OpihiManualWindow) -> None:
                self.gui_instance = gui_instance
                return None

            def __call__(self, x, y) -> str:
                """The coordinate string going to be put onto the navigation
                bar."""
                # The pixel locations.
                x_index = int(x)
                y_index = int(y)
                x_coord_string = "{x_int:d}".format(x_int=x_index)
                y_coord_string = "{y_int:d}".format(y_int=y_index)
                # Extracting the data.
                try:
                    z_float = self.gui_instance.opihi_solution.data[y_index, x_index]
                except AttributeError:
                    # There is no data to index.
                    z_coord_string = "NaN"
                else:
                    # Parse the string from the number provided.
                    z_coord_string = "{z_flt:.2f}".format(z_flt=z_float)

                # Compiling it all together.
                coord_string = "[{x_str}, {y_str}] = {z_str}".format(
                    x_str=x_coord_string, y_str=y_coord_string, z_str=z_coord_string
                )
                return coord_string

        # Assigning the coordinate formatter derived.
        self._opihi_coordinate_formatter = CoordinateFormatter(self)
        self.opihi_axes.format_coord = self._opihi_coordinate_formatter

        # Setting the layout, it is likely better to have the toolbar below
        # rather than above to avoid conflicts with the reset buttons in the
        # event of a mis-click.
        self.ui.vertical_layout_image.addWidget(self.opihi_canvas)
        self.ui.vertical_layout_image.addWidget(self.opihi_nav_toolbar)
        # Remove the dummy spacers otherwise it is just extra unneeded space.
        self.ui.vertical_layout_image.removeWidget(self.ui.dummy_opihi_image)
        self.ui.vertical_layout_image.removeWidget(self.ui.dummy_opihi_navbar)
        self.ui.dummy_opihi_image.hide()
        self.ui.dummy_opihi_navbar.hide()
        self.ui.dummy_opihi_image.deleteLater()
        self.ui.dummy_opihi_navbar.deleteLater()
        del self.ui.dummy_opihi_image
        del self.ui.dummy_opihi_navbar
        return None

    def __init_preprocess_solution(self):
        """Initialize the preprocessing solution. The preprocessing files
        should be specified in the configuration file.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Using the configuration file to extract where the preprocessing
        # filenames are to build the solution.
        try:
            preprocess = opihiexarata.OpihiPreprocessSolution(
                mask_c_fits_filename=library.config.PREPROCESS_MASK_C_FITS_FILENAME,
                mask_g_fits_filename=library.config.PREPROCESS_MASK_G_FITS_FILENAME,
                mask_r_fits_filename=library.config.PREPROCESS_MASK_R_FITS_FILENAME,
                mask_i_fits_filename=library.config.PREPROCESS_MASK_I_FITS_FILENAME,
                mask_z_fits_filename=library.config.PREPROCESS_MASK_Z_FITS_FILENAME,
                mask_1_fits_filename=library.config.PREPROCESS_MASK_1_FITS_FILENAME,
                mask_2_fits_filename=library.config.PREPROCESS_MASK_2_FITS_FILENAME,
                mask_3_fits_filename=library.config.PREPROCESS_MASK_3_FITS_FILENAME,
                flat_c_fits_filename=library.config.PREPROCESS_FLAT_C_FITS_FILENAME,
                flat_g_fits_filename=library.config.PREPROCESS_FLAT_G_FITS_FILENAME,
                flat_r_fits_filename=library.config.PREPROCESS_FLAT_R_FITS_FILENAME,
                flat_i_fits_filename=library.config.PREPROCESS_FLAT_I_FITS_FILENAME,
                flat_z_fits_filename=library.config.PREPROCESS_FLAT_Z_FITS_FILENAME,
                flat_1_fits_filename=library.config.PREPROCESS_FLAT_1_FITS_FILENAME,
                flat_2_fits_filename=library.config.PREPROCESS_FLAT_2_FITS_FILENAME,
                flat_3_fits_filename=library.config.PREPROCESS_FLAT_3_FITS_FILENAME,
                bias_fits_filename=library.config.PREPROCESS_BIAS_FITS_FILENAME,
                dark_current_fits_filename=library.config.PREPROCESS_DARK_CURRENT_FITS_FILENAME,
                linearity_fits_filename=library.config.PREPROCESS_LINEARITY_FITS_FILENAME,
            )
        except Exception:
            # Something failed with making the preprocess solution, a
            # configuration file issue is likely the reason.
            # TODO
            preprocess = None
        finally:
            self.preprocess_solution = preprocess
        # All done.
        return None

    def __connect_push_button_new_image_automatic(self):
        """The automatic method relying on earliest fits file available in
        the expected directory. This function is a connected function action to
        a button in the GUI.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Fetch a file from the directory where files are to be fetched.
        try:
            new_fits_filename = library.path.get_most_recent_filename_in_directory(
                self.automatic_fetch_directory, "fits"
            )
        except Exception:
            # Something happened and a new fits file cannot be properly
            # derived.
            new_fits_filename = ""

        # If the user did not provide a file to enter, there is nothing to be
        # changed.
        if os.path.isfile(new_fits_filename):
            # Assign the new fits filename.
            self.raw_fits_filename = os.path.abspath(new_fits_filename)
        else:
            # Exit!
            return None

        # Process the file first so that what the user sees is closer to
        # what it really is.

        # Load up the new file.
        self._load_fits_file(fits_filename=self.raw_fits_filename)
        # All done.
        return None

    def __connect_push_button_new_image_manual(self):
        """The manual method relying on earliest fits file available in
        the expected directory. This function is a connected function action to
        a button in the GUI.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Ask the user for the filename via a dialog.
        new_fits_filename, __ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Open Opihi Image",
            dir="./",
            filter="FITS Files (*.fits)",
        )
        # If the user did not provide a file to enter, there is nothing to be
        # changed.
        if os.path.isfile(new_fits_filename):
            # Assign the new fits filename.
            self.raw_fits_filename = os.path.abspath(new_fits_filename)
        else:
            # Exit!
            return None

        # We update the automatic fetching directory with the path from this
        # manual file. It is usually the case that the user expects updates
        # from their same directory.
        new_fits_directory = library.path.get_directory(pathname=self.raw_fits_filename)
        self.automatic_fetch_directory = new_fits_directory

        # Process the file first so that what the user sees is closer to
        # what it really is.

        # Load up the new file.
        self._load_fits_file(fits_filename=self.raw_fits_filename)
        # All done.
        return None

    def __connect_push_button_new_target(self) -> None:
        """The function serving to set the software to be on a new target.
        A name is prompted from the user.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Find what the new name of the target from the user.
        previous_set_name = (
            self.asteroid_set_name if self.asteroid_set_name is not None else str()
        )
        new_set_name = gui.name.ask_user_target_name_window(default=previous_set_name)
        self.asteroid_set_name = new_set_name

        # Reset the previous text as it is all going to be a new target.
        # It is expected after this a new image would be selected.
        self.clear_dynamic_label_text()

        return None

    def __connect_push_button_refresh_window(self) -> None:
        """The function serving to refresh the window and redrawing the plot.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Just redraw the plot and redo the dynamic text.
        self.redraw_opihi_image()
        self.refresh_dynamic_label_text()
        return None

    def __connect_push_button_astrometry_solve_astrometry(self) -> None:
        """The button to instruct on the solving of the astrometric solution.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no image (and thus no solution class), there is nothing
        # to do.
        if not isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            return None

        # Determine the engine from user input via the drop down menu. The
        # recognizing text ought to be case insensitive, makes life easier.
        input_engine_name = self.ui.combo_box_astrometry_solve_engine.currentText()
        input_engine_name = input_engine_name.casefold()
        # Search programed engines for the one specified.
        engine = opihiexarata.gui.functions.pick_engine_class_from_name(
            engine_name=input_engine_name, engine_type=library.engine.AstrometryEngine
        )
        vehicle_args = {}

        # Solve the field using the provided engine.
        __ = self.opihi_solution.solve_astrometry(
            solver_engine=engine, overwrite=True, vehicle_args=vehicle_args
        )
        # Update all of the necessary information.
        self.redraw_opihi_image()
        self.refresh_dynamic_label_text()
        return None

    def __connect_push_button_astrometry_custom_solve(self) -> None:
        """ "The button which uses an astrometric solution to solve for a
        custom pixel location or RA DEC location depending on entry.

        This prioritizes solving RA DEC from pixel location.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no astrometric solution, nothing can be done. Exit this
        # early.
        if not (
            isinstance(self.opihi_solution, opihiexarata.OpihiSolution)
            and isinstance(
                self.opihi_solution.astrometrics, astrometry.AstrometricSolution
            )
        ):
            return None

        # Obtain the current values in the entry field.
        in_custom_x = self.ui.line_edit_astrometry_custom_x.text()
        in_custom_y = self.ui.line_edit_astrometry_custom_y.text()
        in_custom_ra = self.ui.line_edit_astrometry_custom_ra.text()
        in_custom_dec = self.ui.line_edit_astrometry_custom_dec.text()

        # Prioritize the presence of the pixel location text.
        if len(in_custom_x) != 0 and len(in_custom_y) != 0:
            # Using pixel locations to determine RA DEC.
            in_custom_x = float(in_custom_x)
            in_custom_y = float(in_custom_y)
            # Reformatting the entry.
            out_custom_x = str(in_custom_x)
            out_custom_y = str(in_custom_y)
            # Converting.
            (
                out_custom_ra,
                out_custom_dec,
            ) = self.opihi_solution.astrometrics.pixel_to_sky_coordinates(
                x=in_custom_x, y=in_custom_y
            )
            (
                out_custom_ra,
                out_custom_dec,
            ) = library.conversion.degrees_to_sexagesimal_ra_dec(
                ra_deg=out_custom_ra, dec_deg=out_custom_dec, precision=2
            )
        elif len(in_custom_ra) != 0 and len(in_custom_dec) != 0:
            # Using RA DEC to solve for pixel locations.
            # Reformatting the entry.
            out_custom_ra = str(in_custom_ra)
            out_custom_dec = str(in_custom_dec)

            (
                in_custom_ra_deg,
                in_custom_dec_deg,
            ) = library.conversion.sexagesimal_ra_dec_to_degrees(
                ra_sex=in_custom_ra, dec_sex=in_custom_dec
            )
            (
                out_custom_x,
                out_custom_y,
            ) = self.opihi_solution.astrometrics.sky_to_pixel_coordinates(
                ra=in_custom_ra_deg, dec=in_custom_dec_deg
            )
            # Needs to be a string.
            out_custom_x = str(out_custom_x)
            out_custom_y = str(out_custom_y)
        else:
            # No matching pair has been provided, ignore.
            out_custom_x = str(in_custom_x)
            out_custom_y = str(in_custom_y)
            out_custom_ra = str(in_custom_ra)
            out_custom_dec = str(in_custom_dec)

        # Finally, set the text on the values.
        self.ui.line_edit_astrometry_custom_x.setText(out_custom_x)
        self.ui.line_edit_astrometry_custom_y.setText(out_custom_y)
        self.ui.line_edit_astrometry_custom_ra.setText(out_custom_ra)
        self.ui.line_edit_astrometry_custom_dec.setText(out_custom_dec)
        return None

    def __connect_push_button_photometry_solve_photometry(self) -> None:
        """A routine to use the current observation and historical observations
        to derive the propagation solution.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no image (and thus no solution class), there is nothing
        # to do.
        if not isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            return None

        # Determine the engine from user input via the drop down menu. The
        # recognizing text ought to be case insensitive, makes life easier.
        input_engine_name = self.ui.combo_box_photometry_solve_engine.currentText()
        input_engine_name = input_engine_name.casefold()
        # Search programed engines for the one specified.
        engine = opihiexarata.gui.functions.pick_engine_class_from_name(
            engine_name=input_engine_name, engine_type=library.engine.PhotometryEngine
        )
        vehicle_args = {}

        # Solve.
        __ = self.opihi_solution.solve_photometry(
            solver_engine=engine, overwrite=True, vehicle_args=vehicle_args
        )

        # Update all of the necessary information.
        self.redraw_opihi_image()
        self.refresh_dynamic_label_text()
        return None

    def __connect_push_button_orbit_solve_orbit(self) -> None:
        """A routine to use the current observation and historical observations
        to derive the orbit solution.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no image (and thus no solution class), there is nothing
        # to do.
        if not isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            return None

        # Determine the engine from user input via the drop down menu. The
        # recognizing text ought to be case insensitive, makes life easier.
        input_engine_name = self.ui.combo_box_orbit_solve_engine.currentText()
        input_engine_name = input_engine_name.casefold()
        # Search programed engines for the one specified.
        engine = opihiexarata.gui.functions.pick_engine_class_from_name(
            engine_name=input_engine_name, engine_type=library.engine.OrbitEngine
        )
        vehicle_args = {}
        # If a custom orbit has been specified, then it is captured by the
        # vehicle arguments.
        if issubclass(engine, orbit.CustomOrbitEngine):
            custom_orbit_elements = self._parse_custom_orbital_elements()
            vehicle_args = custom_orbit_elements

        # Solve.
        __ = self.opihi_solution.solve_orbit(
            solver_engine=engine, overwrite=True, vehicle_args=vehicle_args
        )

        # Update all of the necessary information.
        self.redraw_opihi_image()
        self.refresh_dynamic_label_text()
        # All done.
        return None

    def __connect_push_button_orbit_solve_ephemeris(self) -> None:
        """A routine to use the current observation and historical observations
        to derive the orbit solution.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no image (and thus no solution class), there is nothing
        # to do.
        if not isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            return None

        # Determine the engine from user input via the drop down menu. The
        # recognizing text ought to be case insensitive, makes life easier.
        input_engine_name = self.ui.combo_box_ephemeris_solve_engine.currentText()
        input_engine_name = input_engine_name.casefold()
        # Search programed engines for the one specified.
        engine = opihiexarata.gui.functions.pick_engine_class_from_name(
            engine_name=input_engine_name, engine_type=library.engine.EphemerisEngine
        )
        vehicle_args = {}

        # Solve.
        __ = self.opihi_solution.solve_ephemeris(
            solver_engine=engine, overwrite=True, vehicle_args=vehicle_args
        )

        # Update all of the necessary information.
        self.redraw_opihi_image()
        self.refresh_dynamic_label_text()
        # All done.
        return None

    def __connect_push_button_propagate_custom_solve(self) -> None:
        """Solving for the location of the target through the ephemeris based
        on the time and date provided by the user.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no propagation solution, there is nothing to be done.
        if not isinstance(
            self.opihi_solution.ephemeritics, ephemeris.EphemeriticSolution
        ):
            return None

        # Get the time and date from the user input.
        datetime_input = self.ui.date_time_edit_ephemeris_date_time.dateTime()
        # Getting the timezone, as the propagation requires UTC/JD time, a
        # conversion is needed. Qt uses IANA timezone IDs so we convert from
        # the human readable ones to it. We only deal with current timezones.
        timezone_input = self.ui.combo_box_ephemeris_timezone.currentText()
        timezone_input = timezone_input.casefold()
        if timezone_input == "utc+00:00":
            qt_timezone_str = "Etc/UTC"
        elif timezone_input == "hst-10:00":
            qt_timezone_str = "Pacific/Honolulu"
        else:
            error.DevelopmentError(
                "The timezone dropdown entry provided by the GUI is not implemented and"
                " has no translation to an IANA timezone ID."
            )

        # Using Qt's own datetime conversion just because it is already here.
        qt_timezone_bytearray = QtCore.QByteArray(qt_timezone_str.encode())
        qt_timezone = QtCore.QTimeZone(qt_timezone_bytearray)
        datetime_input.setTimeZone(qt_timezone)
        unix_time_input = datetime_input.toSecsSinceEpoch()
        # As a Julian day as that is the standard time system.
        julian_day_input = library.conversion.unix_time_to_julian_day(
            unix_time=unix_time_input
        )

        # Using this unique time provided to solve the propagation.
        ra_deg, dec_deg = self.opihi_solution.ephemeritics.forward_ephemeris(
            future_time=julian_day_input
        )
        ra_sex, dec_sex = library.conversion.degrees_to_sexagesimal_ra_dec(
            ra_deg=ra_deg, dec_deg=dec_deg, precision=2
        )
        # Updating the RA and DEC values.
        self.ui.label_dynamic_ephemeris_custom_ra.setText(ra_sex)
        self.ui.label_dynamic_ephemeris_custom_dec.setText(dec_sex)

        # All done.
        return None

    def __connect_push_button_propagate_solve_propagation(self) -> None:
        """A routine to use the current observation and historical observations
        to derive the propagation solution.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no image (and thus no solution class), there is nothing
        # to do.
        if not isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            return None

        # Determine the engine from user input via the drop down menu. The
        # recognizing text ought to be case insensitive, makes life easier.
        input_engine_name = self.ui.combo_box_propagate_solve_engine.currentText()
        input_engine_name = input_engine_name.casefold()
        # Search programed engines for the one specified.
        engine = opihiexarata.gui.functions.pick_engine_class_from_name(
            engine_name=input_engine_name, engine_type=library.engine.PropagationEngine
        )
        vehicle_args = {}

        # Solve.
        __ = self.opihi_solution.solve_propagate(
            solver_engine=engine, overwrite=True, vehicle_args=vehicle_args
        )

        # Update all of the necessary information.
        self.redraw_opihi_image()
        self.refresh_dynamic_label_text()
        return None

    def __connect_push_button_propagate_custom_solve(self) -> None:
        """Solving for the location of the target through propagation based on
        the time and date provided by the user.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no propagation solution, there is nothing to be done.
        if not isinstance(
            self.opihi_solution.propagatives, propagate.PropagativeSolution
        ):
            return None

        # Get the time and date from the user input.
        datetime_input = self.ui.date_time_edit_propagate_date_time.dateTime()
        # Getting the timezone, as the propagation requires UTC/JD time, a
        # conversion is needed. Qt uses IANA timezone IDs so we convert from
        # the human readable ones to it. We only deal with current timezones.
        timezone_input = self.ui.combo_box_propagate_timezone.currentText()
        timezone_input = timezone_input.casefold()
        if timezone_input == "utc+00:00":
            qt_timezone_str = "Etc/UTC"
        elif timezone_input == "hst-10:00":
            qt_timezone_str = "Pacific/Honolulu"
        else:
            error.DevelopmentError(
                "The timezone dropdown entry provided by the GUI is not implemented and"
                " has no translation to an IANA timezone ID."
            )

        # Using Qt's own datetime conversion just because it is already here.
        qt_timezone_bytearray = QtCore.QByteArray(qt_timezone_str.encode())
        qt_timezone = QtCore.QTimeZone(qt_timezone_bytearray)
        datetime_input.setTimeZone(qt_timezone)
        unix_time_input = datetime_input.toSecsSinceEpoch()
        # As a Julian day as that is the standard time system.
        julian_day_input = library.conversion.unix_time_to_julian_day(
            unix_time=unix_time_input
        )

        # Using this unique time provided to solve the propagation.
        ra_deg, dec_deg = self.opihi_solution.propagatives.forward_propagate(
            future_time=julian_day_input
        )
        ra_sex, dec_sex = library.conversion.degrees_to_sexagesimal_ra_dec(
            ra_deg=ra_deg, dec_deg=dec_deg, precision=2
        )
        # Updating the RA and DEC values.
        self.ui.label_dynamic_propagate_custom_ra.setText(ra_sex)
        self.ui.label_dynamic_propagate_custom_dec.setText(dec_sex)

        # All done.
        return None

    def __get_mpc_record_filename(self) -> str:
        """This is a function which derives the MPC record filename from
        naming conventions and the current fits file name.

        Parameters
        ----------
        None

        Returns
        -------
        mpc_record_filename : str
            The filename of the MPC record for this object/image.
        """
        mpc_target_name = self.asteroid_set_name
        mpc_record_filename = "{an}__exarata_mpcrecord".format(an=mpc_target_name)
        # Search the same directory as the fits file for this information as
        # that is currently the expected location.
        # Preferring the preprocessed filename if it exists, have a fall back.
        fits_pathname = (
            self.raw_fits_filename
            if self.process_fits_filename is None
            else self.process_fits_filename
        )
        fits_directory = library.path.get_directory(pathname=fits_pathname)
        mpc_record_filename = library.path.merge_pathname(
            directory=fits_directory, filename=mpc_record_filename, extension="txt"
        )
        return mpc_record_filename

    def _preprocess_fits_file(
        self, raw_filename: str, process_filename: str = None
    ) -> str:
        """Using the provided filename, preprocess the fits file listed.

        This is used primarily during the loading of a new fits file.

        Parameters
        ----------
        raw_filename : string
            The filename of the raw fits file to be preprocessed.
        process_filename : string, default = None
            The filename where the processed fits file will be saved to. If
            None, it defaults to a sensible naming convention to distinguish
            the two.

        Returns
        -------
        process_filename : string
            The filename of the preprocessed file is returned, this is just
            in case the value was derived from the naming convention. This is
            an absolute path.
        """
        # Deriving saving location of the processed fits file.
        if isinstance(process_filename, str):
            process_filename = os.path.abspath(process_filename)
        else:
            # Use a sensible naming convention to distinguish between the raw
            # and processed file.
            # TODO
            process_filename = "./process.fits"

        # Saving for later.
        self.process_fits_filename = process_filename

        # Process the fits file.
        __ = self.preprocess_solution.preprocess_fits_file(
            raw_filename=raw_filename, out_filename=process_filename
        )
        # All done.
        return process_filename

    def _load_fits_file(self, fits_filename: str) -> None:
        """Load a fits file into the GUI to derive all of the solutions needed.

        This loads the fits file into an OpihiSolution class for which this
        GUI interacts with and derives the information from.

        Parameters
        ----------
        fits_filename : str
            The fits filename which will be loaded.

        Returns
        -------
        None
        """
        # Saving the previous file and other information.
        self.save_results()

        # Extracting the header of this fits file to get the observing
        # metadata from it.
        header, __ = library.fits.read_fits_image_file(filename=fits_filename)

        # The filter which image is in, extracted from the fits file,
        # assuming standard form.
        filter_name = "g"

        # The exposure time of the image, extracted from the fits file,
        # assuming standard form.
        exposure_time = float(header["ITIME"])

        # Converting date to Julian day as the solution class requires it.
        # We use the modified Julian day from the header file.
        observing_time = library.conversion.modified_julian_day_to_julian_day(
            mjd=header["MJD_OBS"]
        )

        # For asteroid information, if we are to prompt the user for
        # information about the asteroid.
        if library.config.GUI_MANUAL_PROMPT_FOR_ASTEROID_INFORMATION:
            # The name is derived from the current object set that we are on.
            asteroid_name = self.asteroid_set_name
            # Use the target selector GUI for the position of the asteroid.
            asteroid_location = gui.selector.ask_user_target_selector_window(
                current_fits_filename=fits_filename
            )
            # If there exists a MPC record of previous observations, use it
            # for the history. If it does not exist, make one.
            mpcrecord_filename = self.__get_mpc_record_filename()
            if not os.path.isfile(mpcrecord_filename):
                with open(mpcrecord_filename, "w"):
                    pass
            # Read the historical data.
            with open(mpcrecord_filename, "r") as mpcfile:
                raw_lines = mpcfile.readlines()
            # The files have new line characters on them, they need to be
            # removed to have the normal 80 characters.
            asteroid_history = [linedex.removesuffix("\n") for linedex in raw_lines]
        else:
            asteroid_name = None
            asteroid_location = None
            asteroid_history = None

        # Although the OpihiSolution could derive these values from the
        # header of the filename, the solution class is built to be general.
        # Creating the solution from the data.
        opihi_solution = opihiexarata.OpihiSolution(
            fits_filename=fits_filename,
            filter_name=filter_name,
            exposure_time=exposure_time,
            observing_time=observing_time,
            asteroid_name=asteroid_name,
            asteroid_location=asteroid_location,
            asteroid_history=asteroid_history,
        )
        self.opihi_solution = opihi_solution

        # Because a new image was loaded, the previous values and other
        # information derived from the last image are invalid, reset and replot.
        self.clear_dynamic_label_text()
        self.refresh_dynamic_label_text()
        self.redraw_opihi_image()
        return None

    def _parse_custom_orbital_elements(self) -> dict:
        """This function takes the textual form of the orbital elements as
        entered and tries to parse it into a set of orbital elements and errors.

        Parameters
        ----------
        None

        Returns
        -------
        orbital_elements : dictionary
            A dictionary of the orbital elements and their errors, if they
            exist.
        """
        # Extracting all of the values from the text.
        sm_axis_str = self.ui.line_edit_orbit_semimajor_axis.text().strip()
        ecc_str = self.ui.line_edit_orbit_eccentricity.text().strip()
        incli_str = self.ui.line_edit_orbit_inclination.text().strip()
        as_node_str = self.ui.line_edit_orbit_ascending_node.text().strip()
        peri_str = self.ui.line_edit_orbit_perihelion.text().strip()
        m_anom_str = self.ui.line_edit_orbit_mean_anomaly.text().strip()
        epoch_str = self.ui.line_edit_orbit_epoch.text().strip()

        # Parse if there is an error bar or not. Writing a function because
        # this is going to be happening a lot.
        def error_bar_parse(entry_string: str) -> tuple[float, float]:
            """The deliminator for an error bar is any non numeric or decimal
            marker."""
            entry_string = entry_string.strip()
            non_demlim_marks = tuple("1234567890.,")
            # In the event there are more than one character acting as
            # a deliminator.
            lower_delim_index = None
            upper_delim_index = None
            for index, chardex in enumerate(entry_string):
                if chardex not in non_demlim_marks:
                    # This character is a deliminator, mark it.
                    if lower_delim_index is None:
                        # This is the first time a deliminator character has
                        # been encountered.
                        lower_delim_index = index
                    else:
                        # Other deliminator characters have been encountered so
                        # this is the last known deliminator.
                        upper_delim_index = index
            # Split the string based on the deliminator for the value and
            # error segment.
            if lower_delim_index is None and upper_delim_index is None:
                # There was never a deliminator, there is only one value and
                # no error bars.
                value_number = float(entry_string)
                error_number = 0
            elif lower_delim_index is not None and upper_delim_index is None:
                # There is only one deliminator character, use this to split
                # the string.
                value_string = entry_string[:lower_delim_index].strip()
                error_string = entry_string[lower_delim_index:].strip()
                # Converting to values.
                value_number = float(value_string)
                error_number = float(error_string)
            elif lower_delim_index is not None and upper_delim_index is not None:
                # There are more than one characters for the deliminator.
                value_string = entry_string[:lower_delim_index].strip()
                error_string = entry_string[upper_delim_index:].strip()
                # Converting to values.
                value_number = float(value_string)
                error_number = float(error_string)
            # All done.
            return value_number, error_number

        # Parsing the strings.
        sm_axis_val, sm_axis_err = error_bar_parse(sm_axis_str)
        ecc_val, ecc_err = error_bar_parse(ecc_str)
        incli_val, incli_err = error_bar_parse(incli_str)
        as_node_val, as_node_err = error_bar_parse(as_node_str)
        peri_val, peri_err = error_bar_parse(peri_str)
        m_anom_val, m_anom_err = error_bar_parse(m_anom_str)
        epoch_val, epoch_err = error_bar_parse(epoch_str)
        # The Epoch should not have an error.
        if epoch_err != 0:
            raise error.InputError(
                "The Epoch value is detecting that it is specified with an error term"
                " with a non-numeric deliminator. However, the Epoch should not have an"
                " error specified."
            )
        # The orbital element dictionary which would be used for a custom
        # orbit.
        orbital_elements = {
            "semimajor_axis": sm_axis_val,
            "semimajor_axis_error": sm_axis_err,
            "eccentricity": ecc_val,
            "eccentricity_error": ecc_err,
            "inclination": incli_val,
            "inclination_error": incli_err,
            "longitude_ascending_node": as_node_val,
            "longitude_ascending_node_error": as_node_err,
            "argument_perihelion": peri_val,
            "argument_perihelion_error": peri_err,
            "mean_anomaly": m_anom_val,
            "mean_anomaly_error": m_anom_err,
            "epoch_julian_day": epoch_val,
        }
        # All done.
        return orbital_elements

    def clear_dynamic_label_text(self) -> None:
        """Clear all of the dynamic label text and other related fields,
        this is traditionally done just before a new image is going to be
        introduced.

        This resets the text back to their defaults as per the GUI builder.

        The selections on the engines do not need to be reset as they are
        just a selection criteria and do not actually provide any information.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        ## Resetting Summary information.
        #####

        ## Resetting Astrometry information.
        #####
        self.ui.label_dynamic_astrometry_center_x.setText("0000")
        self.ui.label_dynamic_astrometry_center_y.setText("0000")
        self.ui.label_dynamic_astrometry_center_ra.setText("HH:MM:SS.SS")
        self.ui.label_dynamic_astrometry_center_dec.setText("+DD:MM:SS.SS")
        self.ui.label_dynamic_astrometry_target_x.setText("0000")
        self.ui.label_dynamic_astrometry_target_y.setText("0000")
        self.ui.label_dynamic_astrometry_target_ra.setText("HH:MM:SS.SS")
        self.ui.label_dynamic_astrometry_target_dec.setText("+DD:MM:SS.SS")
        self.ui.line_edit_astrometry_custom_x.setText("")
        self.ui.line_edit_astrometry_custom_y.setText("")
        self.ui.line_edit_astrometry_custom_ra.setText("")
        self.ui.line_edit_astrometry_custom_dec.setText("")

        ## Resetting Photometric information.
        #####
        self.ui.label_dynamic_photometry_filter_name.setText("FF")
        self.ui.label_dynamic_photometry_zero_point_value.setText("ZZ.ZZ + E.EEE")

        ## Resetting Orbit information.
        #####

        ## Resetting Ephemeris information.
        #####
        self.ui.label_dynamic_ephemeris_ra_velocity.setText("+VV.VVV")
        self.ui.label_dynamic_ephemeris_dec_velocity.setText("+VV.VVV")
        self.ui.label_dynamic_ephemeris_ra_acceleration.setText("+AA.AAAeXX")
        self.ui.label_dynamic_ephemeris_dec_acceleration.setText("+AA.AAAeXX")

        ## Resetting Propagate information.
        #####
        self.ui.label_dynamic_propagate_ra_velocity.setText("+VV.VVV")
        self.ui.label_dynamic_propagate_dec_velocity.setText("+VV.VVV")
        self.ui.label_dynamic_propagate_ra_acceleration.setText("+AA.AAAeXX")
        self.ui.label_dynamic_propagate_dec_acceleration.setText("+AA.AAAeXX")
        self.ui.text_browser_propagate_future_results.setPlainText(
            "YYYY-MM-DD  HH:MM:SS  Z   |   HH:MM:SS.SS    +DD:MM:SS.SS"
        )
        # Keeping the timezone and time information for convenience.
        self.ui.label_dynamic_propagate_custom_ra.setText("HH:MM:SS.SS")
        self.ui.label_dynamic_propagate_custom_dec.setText("+DD:MM:SS.SS")

        # All done.
        return None

    def refresh_dynamic_label_text(self) -> None:
        """Refresh all of the dynamic label text, this fills out the
        information based on the current solutions available and solved.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # These values are only to be done if the OpihiSolution actually
        # exists, otherwise, there is nothing to update in the text.
        if isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            self.__refresh_dynamic_label_text_astrometry()
            self.__refresh_dynamic_label_text_photometry()
            self.__refresh_dynamic_label_text_orbit()
            self.__refresh_dynamic_label_text_ephemeris()
            self.__refresh_dynamic_label_text_propagate()

        # All done.
        return None

    def __refresh_dynamic_label_text_astrometry(self) -> None:
        """Refresh all of the dynamic label text for astrometry.
        This fills out the information based on the current solutions
        available and solved.

        An astrometric solution must exist.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Everything in this function needs the OpihiSolution, if it does not
        # exist, then exit early as there is nothing to refresh.
        if not isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            return None
        else:
            opihi_solution = self.opihi_solution

        # The pixel center location of the image and the pixel location of
        # the asteroid does not require the astrometric solution.
        cen_x, cen_y = [side / 2 for side in opihi_solution.data.shape]
        trg_x, trg_y = (
            opihi_solution.asteroid_location
            if opihi_solution.asteroid_location is not None
            else (0, 0)
        )
        # Replace the text with the new information.
        self.ui.label_dynamic_astrometry_center_x.setText(str(cen_x))
        self.ui.label_dynamic_astrometry_center_y.setText(str(cen_y))
        self.ui.label_dynamic_astrometry_target_x.setText(str(trg_x))
        self.ui.label_dynamic_astrometry_target_y.setText(str(trg_y))

        # Everything beyond this point requires an astrometric solution, if
        # it does not exist, there is no point in continuing, exiting early.
        if not isinstance(
            self.opihi_solution.astrometrics, astrometry.AstrometricSolution
        ):
            return None
        else:
            astrometrics = self.opihi_solution.astrometrics

        # The pixel locations converted to RA DEC via the astrometric solution.
        cen_ra, cen_dec = astrometrics.pixel_to_sky_coordinates(x=cen_x, y=cen_y)
        trg_ra, trg_dec = astrometrics.pixel_to_sky_coordinates(x=trg_x, y=trg_y)

        # The format really ought to be in HMSDMS hexadecimal-like as it
        # is more familiar to Astronomers.
        cen_ra_sex, cen_dec_sex = library.conversion.degrees_to_sexagesimal_ra_dec(
            ra_deg=cen_ra, dec_deg=cen_dec, precision=2
        )
        trg_ra_sex, trg_dec_sex = library.conversion.degrees_to_sexagesimal_ra_dec(
            ra_deg=trg_ra, dec_deg=trg_dec, precision=2
        )
        # Replace the text.
        self.ui.label_dynamic_astrometry_center_ra.setText(cen_ra_sex)
        self.ui.label_dynamic_astrometry_center_dec.setText(cen_dec_sex)
        self.ui.label_dynamic_astrometry_target_ra.setText(trg_ra_sex)
        self.ui.label_dynamic_astrometry_target_dec.setText(trg_dec_sex)

        # All done.
        return None

    def __refresh_dynamic_label_text_photometry(self) -> None:
        """Refresh all of the dynamic label text for photometry.
        This fills out the information based on the current solutions
        available and solved.

        A photometric solution must exist.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Everything in this function needs the OpihiSolution, if it does not
        # exist, then exit early as there is nothing to refresh.
        if not isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            return None
        else:
            opihi_solution = self.opihi_solution

        # The filter is provided by the image's header, a solution is not
        # required for displaying this information.
        filter_name = str(opihi_solution.filter_name)
        self.ui.label_dynamic_photometry_filter_name.setText(filter_name)

        # Everything beyond this point requires an astrometric solution, if
        # it does not exist, there is no point in continuing, exiting early.
        if not isinstance(
            self.opihi_solution.photometrics, photometry.PhotometricSolution
        ):
            return None
        else:
            photometrics = self.opihi_solution.photometrics

        # Obtaining the computed zero point of the image. Some rounding is
        # needed so it can properly fit in the GUI.
        zero_point = round(photometrics.zero_point, 2)
        zero_point_error = round(photometrics.zero_point_error, 3)
        # Building the string for display and updating the text.
        pm_sym = "\u00B1"
        zero_point_str = "{zp} {pm} {err}".format(
            zp=zero_point, pm=pm_sym, err=zero_point_error
        )
        self.ui.label_dynamic_photometry_zero_point_value.setText(zero_point_str)

        # All done.
        return None

    def __refresh_dynamic_label_text_orbit(self) -> None:
        """Refresh all of the dynamic label text for orbit.
        This fills out the information based on the current solutions
        available and solved.

        An orbital solution must exist.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Everything in this function needs the OpihiSolution, if it does not
        # exist, then exit early as there is nothing to refresh.
        if not isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            return None
        else:
            opihi_solution = self.opihi_solution

        # Nothing so far.
        pass

        # Everything beyond this point requires an orbital solution, if
        # it does not exist, there is no point in continuing, exiting early.
        if not isinstance(self.opihi_solution.orbitals, orbit.OrbitalSolution):
            return None
        else:
            orbitals = self.opihi_solution.orbitals

        # Refreshing the values of the Keplerian orbital elements.
        # The orbital elements' values and errors should be reported. We define
        # the string formatting here.
        def orb_str_conv(val: float, err: float) -> str:
            """Unified string formatting for orbital element values and errors."""
            # Rounding values to sensible values.
            val = round(val, 7)
            err = round(err, 3)
            # Building the string, allowing for the usage of the plus minus
            # symbol to demark the error.
            pm_sym = "\u00B1"
            ele_string = "{v} {pm} {e}".format(v=val, pm=pm_sym, e=err)
            return ele_string

        # Using the above function to derive the display strings for all of the
        # elements.
        semimajor_axis_string = orb_str_conv(
            val=orbitals.semimajor_axis, err=orbitals.semimajor_axis_error
        )
        eccentricity_string = orb_str_conv(
            val=orbitals.eccentricity, err=orbitals.eccentricity_error
        )
        inclination_string = orb_str_conv(
            val=orbitals.inclination, err=orbitals.inclination_error
        )
        ascending_node_string = orb_str_conv(
            val=orbitals.longitude_ascending_node,
            err=orbitals.longitude_ascending_node_error,
        )
        perihelion_string = orb_str_conv(
            val=orbitals.argument_perihelion, err=orbitals.argument_perihelion_error
        )
        mean_anomaly_string = orb_str_conv(
            val=orbitals.mean_anomaly, err=orbitals.mean_anomaly_error
        )
        # Changing the text using the derived strings.
        self.ui.line_edit_orbit_semimajor_axis.setText(semimajor_axis_string)
        self.ui.line_edit_orbit_eccentricity.setText(eccentricity_string)
        self.ui.line_edit_orbit_inclination.setText(inclination_string)
        self.ui.line_edit_orbit_ascending_node.setText(ascending_node_string)
        self.ui.line_edit_orbit_perihelion.setText(perihelion_string)
        self.ui.line_edit_orbit_mean_anomaly.setText(mean_anomaly_string)

        # Maximum precision on the epoch Julian day is desired however.
        julian_day_string = str(orbitals.epoch_julian_day)
        self.ui.line_edit_orbit_epoch.setText(julian_day_string)

        # All done.
        return None

    def __refresh_dynamic_label_text_ephemeris(self) -> None:
        """Refresh all of the dynamic label text for ephemerides.
        This fills out the information based on the current solutions
        available and solved.

        An ephemeritic solution must exist.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Everything in this function needs the OpihiSolution, if it does not
        # exist, then exit early as there is nothing to refresh.
        if not isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            return None
        else:
            opihi_solution = self.opihi_solution

        # Nothing so far.
        pass

        # Everything beyond this point requires an orbital solution, if
        # it does not exist, there is no point in continuing, exiting early.
        if not isinstance(
            self.opihi_solution.ephemeritics, ephemeris.EphemeriticSolution
        ):
            return None
        else:
            ephemeritics = self.opihi_solution.ephemeritics

        # Update the rate text with the velocity terms provided by the
        # propagation solution. The propagation solution provides rates as
        # degrees per second.
        ra_v_deg = ephemeritics.ra_velocity
        dec_v_deg = ephemeritics.dec_velocity
        # And acceleration, as degrees per second squared.
        ra_a_deg = ephemeritics.ra_acceleration
        dec_a_deg = ephemeritics.dec_acceleration
        # Converting to the more familiar arcsec/s from deg/s along with
        # arcsec/s/s from deg/s/s. Round after and prepare to make it a
        # string for the GUI.
        def vel_deg_to_arcsec_str(degree: float) -> str:
            return str(round(degree * 3600, 5))

        def accl_deg_to_arcsec_str(degree: float) -> str:
            # Accelerations are usually a lot less and thus should get their
            # own method of manipulation.
            return str("{acc:2.3e}".format(acc=degree))

        ra_v_arcsec_str = vel_deg_to_arcsec_str(ra_v_deg)
        dec_v_arcsec_str = vel_deg_to_arcsec_str(dec_v_deg)
        ra_a_arcsec_str = accl_deg_to_arcsec_str(ra_a_deg)
        dec_a_arcsec_str = accl_deg_to_arcsec_str(dec_a_deg)
        # Update the dynamic text.
        self.ui.label_dynamic_ephemeris_ra_velocity.setText(ra_v_arcsec_str)
        self.ui.label_dynamic_ephemeris_dec_velocity.setText(dec_v_arcsec_str)
        self.ui.label_dynamic_ephemeris_ra_acceleration.setText(ra_a_arcsec_str)
        self.ui.label_dynamic_ephemeris_dec_acceleration.setText(dec_a_arcsec_str)

        # All done.
        return None

    def __refresh_dynamic_label_text_propagate(self) -> None:
        """Refresh all of the dynamic label text for propagate.
        This fills out the information based on the current solutions
        available and solved.

        A propagative solution must exist.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Everything in this function needs the OpihiSolution, if it does not
        # exist, then exit early as there is nothing to refresh.
        if not isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            return None
        else:
            opihi_solution = self.opihi_solution

        # Nothing so far.
        pass

        # Everything beyond this point requires an astrometric solution, if
        # it does not exist, there is no point in continuing, exiting early.
        if not isinstance(
            self.opihi_solution.propagatives, propagate.PropagativeSolution
        ):
            return None
        else:
            propagatives = self.opihi_solution.propagatives

        # Update the rate text with the velocity terms provided by the
        # propagation solution. The propagation solution provides rates as
        # degrees per second.
        ra_v_deg = propagatives.ra_velocity
        dec_v_deg = propagatives.dec_velocity
        # And acceleration, as degrees per second squared.
        ra_a_deg = propagatives.ra_acceleration
        dec_a_deg = propagatives.dec_acceleration
        # Converting to the more familiar arcsec/s from deg/s along with
        # arcsec/s/s from deg/s/s. Round after and prepare to make it a
        # string for the GUI.
        def vel_deg_to_arcsec_str(degree: float) -> str:
            return str(round(degree * 3600, 5))

        def accl_deg_to_arcsec_str(degree: float) -> str:
            # Accelerations are usually a lot less and thus should get their
            # own method of manipulation.
            return str("{acc:2.3e}".format(acc=degree))

        ra_v_arcsec_str = vel_deg_to_arcsec_str(ra_v_deg)
        dec_v_arcsec_str = vel_deg_to_arcsec_str(dec_v_deg)
        ra_a_arcsec_str = accl_deg_to_arcsec_str(ra_a_deg)
        dec_a_arcsec_str = accl_deg_to_arcsec_str(dec_a_deg)
        # Update the dynamic text.
        self.ui.label_dynamic_propagate_ra_velocity.setText(ra_v_arcsec_str)
        self.ui.label_dynamic_propagate_dec_velocity.setText(dec_v_arcsec_str)
        self.ui.label_dynamic_propagate_ra_acceleration.setText(ra_a_arcsec_str)
        self.ui.label_dynamic_propagate_dec_acceleration.setText(dec_a_arcsec_str)

        # Use the current time and date to determine the future positions with
        # the time interval provided.
        ENTRY_COUNT = library.config.GUI_MANUAL_PROPAGATE_FUTURE_COMPUTE_ENTRY_COUNT
        INTERVAL = library.config.GUI_MANUAL_PROPAGATE_FUTURE_COMPUTE_TIMESTEP_SECONDS
        INTERVAL_DAYS = INTERVAL / 86400
        current_julian_day = library.conversion.current_utc_to_julian_day()
        precomputed_future_text = ""
        for countdex in range(int(ENTRY_COUNT)):
            # The future Julian day time for this future, as the Julian time
            # scale is in days.
            future_julian_day = current_julian_day + INTERVAL_DAYS * countdex
            # Converting this to the date and time string for this entry.
            # As this is UNIX time, the date is in UTC or Zulu time.
            yr, mh, dy, hr, mn, sc = library.conversion.julian_day_to_full_date(
                jd=future_julian_day
            )
            datetime_str = "{yr}-{mh}-{dy}  {hr}:{mn}:{sc}  Z".format(
                yr=int(yr), mh=int(mh), dy=int(dy), hr=int(hr), mn=int(mn), sc=int(sc)
            )
            # Using the Julian day time to compute the propagated solution for
            # this time and formatting this as the needed string.
            ra_deg, dec_deg = propagatives.forward_propagate(
                future_time=future_julian_day
            )
            ra_sex, dec_sex = library.conversion.degrees_to_sexagesimal_ra_dec(
                ra_deg=ra_deg, dec_deg=dec_deg, precision=2
            )
            ra_dec_str = "{ra}   {dec}".format(ra=ra_sex, dec=dec_sex)
            # The final format for this line per the GUI specification, just
            # adding some space and the new line
            entry_line = "{dt}   |   {rd} \n".format(dt=datetime_str, rd=ra_dec_str)
            precomputed_future_text = precomputed_future_text + entry_line
        # Set the text for the set of future solutions.
        self.ui.text_browser_propagate_future_results.setPlainText(
            precomputed_future_text
        )

        # All done.
        return None

    def redraw_opihi_image(self) -> None:
        """Redraw the Opihi image given that new results may have been added
        because some solutions were completed. This modifies the GUI in-place.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Clear the information before re-plotting, it is easier just to draw
        # it all again.
        self.opihi_axes.clear()

        # This is a function which allows for the disabling of other axes
        # formatting their data values and messing with the formatter class.
        def empty_string(string: str) -> str:
            return str()

        # These are points in future time which will be used to plot the
        # ephemeris and propagation solutions, if they exist. However,
        # as the time step is in seconds, and the standard time of this
        # system is in Julian days, convert.
        TIMESTEP_JD = (
            library.config.GUI_MANUAL_FUTURE_TIME_PLOT_TIMESTEP_SECONDS / 86400
        )
        N_POINTS = library.config.GUI_MANUAL_FUTURE_TIME_PLOT_STEP_COUNT
        # Numpy says linspace is more stable for decimal non-integer steps.
        future_time_plot = np.linspace(
            self.opihi_solution.observing_time,
            self.opihi_solution.observing_time + TIMESTEP_JD * N_POINTS,
            N_POINTS,
            endpoint=True,
        )

        # There is no solution and thus no image can be plotted.
        if self.opihi_solution is None:
            return None

        # The data that will be plotted.
        plotting_data = self.opihi_solution.data
        # We set the bounds of the colorbar based on the 1-99 % bounds.
        colorbar_low, colorbar_high = np.nanpercentile(plotting_data, [1, 99])
        # Plotting the image, should be in the background of everything.
        image = self.opihi_axes.imshow(
            plotting_data, cmap="gray", vmin=colorbar_low, vmax=colorbar_high, zorder=-3
        )
        # Disable their formatting in favor of ours.
        image.format_cursor_data = empty_string

        # Attempt to plot the location of the specified asteroid. If this does
        # not work, it is often because the location of the asteroid was not
        # provided.
        try:
            target_x, target_y = self.opihi_solution.asteroid_location
            target_marker = self.opihi_axes.scatter(
                target_x,
                target_y,
                s=float(library.config.GUI_MANUAL_IMAGE_PLOT_TARGET_MARKER_SIZE),
                marker="^",
                color=str(library.config.GUI_MANUAL_IMAGE_PLOT_TARGET_MARKER_COLOR),
                facecolors="None",
            )
            # Disable their formatting in favor of ours.
            target_marker.format_cursor_data = empty_string
        except Exception:
            # It does not work.
            pass

        # If there is an ephemeris solution, it is helpful to trace out the
        # future path predicted by the ephemeris.
        if isinstance(self.opihi_solution.ephemeritics, ephemeris.EphemeriticSolution):
            # The astrometric solution is also needed to convert it back to
            # pixel coordinates. As the ephemeritic solution requires the
            # astrometric solution, this is fine.
            astrometrics = self.opihi_solution.astrometrics
            ephemeritics = self.opihi_solution.ephemeritics
            # Find the future coordinates based on the future plot times
            # from the configuration.
            ephemeris_future_ra, ephemeris_future_dec = ephemeritics.forward_ephemeris(
                future_time=future_time_plot
            )
            # Converting to pixel locations.
            (
                ephemeris_future_x,
                ephemeris_future_y,
            ) = astrometrics.sky_to_pixel_coordinates(
                ra=ephemeris_future_ra, dec=ephemeris_future_dec
            )
            # Plotting.
            future_ephemeris_plot = self.opihi_axes.plot(
                ephemeris_future_x,
                ephemeris_future_y,
                color=library.config.GUI_MANUAL_FUTURE_TIME_PLOT_EPHEMERIS_LINE_COLOR,
            )
            # Disable their formatting in favor of ours.
            future_ephemeris_plot[0].format_cursor_data = empty_string

        # If there is a propagation solution, it is helpful to trace out the
        # future path predicted by the propagation.
        if isinstance(self.opihi_solution.propagatives, propagate.PropagativeSolution):
            # The astrometric solution is also needed to convert it back to
            # pixel coordinates. As the ephemeritic solution requires the
            # astrometric solution, this is fine.
            astrometrics = self.opihi_solution.astrometrics
            propagatives = self.opihi_solution.propagatives
            # Find the future coordinates based on the future plot times
            # from the configuration.
            propagate_future_ra, propagate_future_dec = propagatives.forward_propagate(
                future_time=future_time_plot
            )
            # Converting to pixel locations.
            (
                propagate_future_x,
                propagate_future_y,
            ) = astrometrics.sky_to_pixel_coordinates(
                ra=propagate_future_ra, dec=propagate_future_dec
            )
            # Plotting.
            future_propagate_plot = self.opihi_axes.plot(
                propagate_future_x,
                propagate_future_y,
                color=library.config.GUI_MANUAL_FUTURE_TIME_PLOT_PROPAGATE_LINE_COLOR,
            )
            # Disable their formatting in favor of ours.
            future_propagate_plot[0].format_cursor_data = empty_string

        # Make sure the coordinate formatter does not change.
        self.opihi_axes.format_coord = self._opihi_coordinate_formatter
        # Update and redraw the image via redrawing the canvas.
        self.opihi_canvas.draw()
        return None

    def save_results(self) -> None:
        """Save all of the results of the solutions to date. This is especially
        done upon selecting a new image, the previous image results are
        saved.

        If there is no solution class, then there is no results to save either
        and this function does nothing.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no solution class, there is nothing to save. Exiting
        # early.
        if not isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            return None

        # There are two primary things to save, the image and solution
        # information and the MPC record as retrievable historical data.
        def _save_results_fits_image() -> None:
            """First, doing the image data."""

        def _save_results_mpcrecord() -> None:
            """Second, the MPC record historical data."""
            # The current record to add.
            try:
                mpc_record = self.opihi_solution.mpc_record_row()
            except error.PracticalityError:
                # If the user did not solve for astrometry, this will raise 
                # because it cannot properly make an MPC row. We ignore it 
                # and we do not add any observational data.
                return None
            else:
                # Adding the new line character as write lines do not do this.
                mpc_record = mpc_record + "\n"
            # If the record file already exists, append this information to it.
            with open(self.__get_mpc_record_filename(), "a") as mpcfile:
                mpcfile.writelines([mpc_record])
            # All done.
            return None

        # Executing the saving functions.
        _save_results_fits_image()
        _save_results_mpcrecord()
        # All done.
        return None


def start_manual_window() -> None:
    """This is the function to create the manual window for usage.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    # Creating the application and its infrastructure.
    app = QtWidgets.QApplication([])
    # The manual GUI window.
    manual_window = OpihiManualWindow()
    manual_window.show()
    # Closing out of the window.
    sys.exit(app.exec())
    # All done.
    return None


if __name__ == "__main__":
    start_manual_window()
