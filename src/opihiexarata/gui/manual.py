"""
The manual GUI window.
"""

import sys
import os
import threading
import copy

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
    fits_filename : string
        The filename of the preprocessed image, this is generally generated
        automatically by the preprocess solution. This file is generally used
        for analysis.
    preprocess_solution : OpihiPreprocessSolution
        The preprocessing solution which is used to convert raw images to
        preprocessed files.
    opihi_solution : OpihiSolution
        The general OpihiExarata solution, the collection class of all other
        solutions.
    zero_point_database : OpihiZeroPointDatabaseSolution
        If a zero point database is going to be constructed, as per the
        configuration file, this is the instance which manages the database.
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
        self.fits_filename = None
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

        # Preparing the zero point database if the user desired the database
        # to record observations.
        if library.config.GUI_MANUAL_DATABASE_SAVE_OBSERVATIONS:
            database = opihiexarata.OpihiZeroPointDatabaseSolution(
                database_directory=library.config.MONITOR_DATABASE_DIRECTORY
            )
        else:
            database = None
        self.zero_point_database = database

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

        # Summary-specific buttons.
        self.ui.push_button_summary_save.clicked.connect(
            self.__connect_push_button_summary_save
        )
        self.ui.push_button_send_target_to_tcs.clicked.connect(
            self.__connect_push_button_summary_send_target_to_tcs
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
        self.ui.push_button_ephemeris_update_tcs_rate.clicked.connect(
            self.__connect_push_button_ephemeris_update_tcs_rate
        )
        self.ui.push_button_ephemeris_custom_solve.clicked.connect(
            self.__connect_push_button_ephemeris_custom_solve
        )

        # Propagate-specific buttons.
        self.ui.push_button_propagate_solve_propagation.clicked.connect(
            self.__connect_push_button_propagate_solve_propagation
        )
        self.ui.push_button_propagate_update_tcs_rate.clicked.connect(
            self.__connect_push_button_propagate_update_tcs_rate
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
                mask_b_fits_filename=library.config.PREPROCESS_MASK_B_FITS_FILENAME,
                flat_c_fits_filename=library.config.PREPROCESS_FLAT_C_FITS_FILENAME,
                flat_g_fits_filename=library.config.PREPROCESS_FLAT_G_FITS_FILENAME,
                flat_r_fits_filename=library.config.PREPROCESS_FLAT_R_FITS_FILENAME,
                flat_i_fits_filename=library.config.PREPROCESS_FLAT_I_FITS_FILENAME,
                flat_z_fits_filename=library.config.PREPROCESS_FLAT_Z_FITS_FILENAME,
                flat_1_fits_filename=library.config.PREPROCESS_FLAT_1_FITS_FILENAME,
                flat_2_fits_filename=library.config.PREPROCESS_FLAT_2_FITS_FILENAME,
                flat_b_fits_filename=library.config.PREPROCESS_FLAT_B_FITS_FILENAME,
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
        # Auto saving first, if enabled.
        self.save_auto_save()

        # Fetch a file from the directory where files are to be fetched.
        try:
            # We assume the last image is the directory to fetch from.
            automatic_fetch_directory = library.path.get_directory(
                pathname=self.raw_fits_filename
            )
            new_fits_filename = library.path.get_most_recent_filename_in_directory(
                directory=automatic_fetch_directory,
                extension="fits",
                exclude_opihiexarata_output_files=True,
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
        self.fits_filename = self.raw_fits_filename

        # Load up the new file.
        self._load_fits_file(fits_filename=self.fits_filename)
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
        # Auto saving first, if enabled.
        self.save_auto_save()

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

        # Process the file first so that what the user sees is closer to
        # what it really is.
        self.fits_filename = self.raw_fits_filename

        # Load up the new file.
        self._load_fits_file(fits_filename=self.fits_filename)
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
        self.refresh_dynamic_label_text()
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

    def __connect_push_button_summary_send_target_to_tcs(self) -> None:
        """This function serves to implement sending target information to the
        TCS. All information that can be provided will be provided to the TCS.

        Astronomical coordinates (and thus an astrometric solution) is
        required.

        If both an ephemeritic solution and a propagation solution exists
        for providing the non-sidereal rates, we prioritize those from
        the propagation.

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

        # The name of the target/asteroid. If it is None, we just default to
        # whatever is in the configuration file.
        target_name = self.opihi_solution.asteroid_name
        DEFAULT_TCS_NAME = library.config.GUI_MANUAL_T3IO_DEFAULT_TARGET_NAME
        target_name = DEFAULT_TCS_NAME if target_name is None else target_name

        # We require astrometric coordinates, and thus an astrometric solution.
        # If there are none, then there is nothing we can do.
        if not isinstance(
            self.opihi_solution.astrometrics, astrometry.AstrometricSolution
        ):
            return None
        else:
            ra_deg = self.opihi_solution.astrometrics.ra
            dec_deg = self.opihi_solution.astrometrics.dec

        # If there is a photometric solution that exists, we can obtain the
        # magnitude.
        if not isinstance(
            self.opihi_solution.photometrics, photometry.PhotometricSolution
        ):
            magnitude = self.opihi_solution.asteroid_magnitude
        else:
            magnitude = 0

        # If there is a propagative or ephemeritic solution, we can apply the
        # non-sidereal rates as well. We prioritize propagative solutions.
        if isinstance(self.opihi_solution.propagatives, propagate.PropagativeSolution):
            ra_velocity = self.opihi_solution.propagatives.ra_velocity
            dec_velocity = self.opihi_solution.propagatives.dec_velocity
        elif isinstance(
            self.opihi_solution.ephemeritics, ephemeris.EphemeriticSolution
        ):
            ra_velocity = self.opihi_solution.ephemeritics.ra_velocity
            dec_velocity = self.opihi_solution.ephemeritics.dec_velocity
        else:
            # There are no valid solutions to extract the non-sidereal rates
            # from.
            ra_velocity = 0
            dec_velocity = 0

        # We send all of the information that we could to the TCS. We do not
        # really care about the response just yet.
        __ = library.tcs.t3io_tcs_next(
            ra=ra_deg,
            dec=dec_deg,
            target_name=target_name,
            magnitude=magnitude,
            ra_velocity=ra_velocity,
            dec_velocity=dec_velocity,
        )
        # All done.
        return None

    def __connect_push_button_summary_save(self) -> None:
        """The function serving to save the fits file.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # We get the filename to save the fits file as and try to save it.
        self.save_all_results()
        # All done.
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

        # Note that we are busy solving the solution via the engine.
        self.__configuration_draw_busy_image()

        # Solve the field using the provided engine. We need to break this out
        # into its own thread so that the busy plot notification can be shown
        # to the user. The GUI thread is otherwise blocked.
        def astrometry_solving_function():
            """The function to solve the astrometry and refresh the plots."""
            __ = self.opihi_solution.solve_astrometry(
                solver_engine=engine, overwrite=True, vehicle_args=vehicle_args
            )
            # Update all of the necessary information.
            self.redraw_opihi_image()
            self.refresh_dynamic_label_text()
            self.save_auto_save()
            return None

        astrometry_thread = threading.Thread(target=astrometry_solving_function)
        astrometry_thread.start()
        # All done.
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

        # Note that we are busy solving the solution via the engine.
        self.__configuration_draw_busy_image()

        # Solve the field using the provided engine. We need to break this out
        # into its own thread so that the busy plot notification can be shown
        # to the user. The GUI thread is otherwise blocked.
        def photometry_solving_function():
            """The function to solve the photometry and refresh the plots."""
            # Solve.
            __ = self.opihi_solution.solve_photometry(
                solver_engine=engine, overwrite=True, vehicle_args=vehicle_args
            )
            # Update all of the necessary information.
            self.redraw_opihi_image()
            self.refresh_dynamic_label_text()
            self.save_auto_save()
            # Photometry is special as the data may also be saved to the
            # zero point database. We attempt to write a zero point record to
            # the database, the wrapper writing function checks if writing to
            # the database is a valid operation. We work on a copy of the
            # solution just in case.
            opihi_solution_copy = copy.deepcopy(self.opihi_solution)
            # We thread it away.
            write_database_thread = threading.Thread(
                target=self.__write_zero_point_record_to_database,
                kwargs={"opihi_solution": opihi_solution_copy},
            )
            write_database_thread.start()

            return None

        photometry_thread = threading.Thread(target=photometry_solving_function)
        photometry_thread.start()
        # All done.
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

        # Note that we are busy solving the solution via the engine.
        self.__configuration_draw_busy_image()

        # Solve the field using the provided engine. We need to break this out
        # into its own thread so that the busy plot notification can be shown
        # to the user. The GUI thread is otherwise blocked.
        def orbit_solving_function():
            """The function to solve the orbit and refresh the plots."""
            __ = self.opihi_solution.solve_orbit(
                solver_engine=engine, overwrite=True, vehicle_args=vehicle_args
            )
            # Update all of the necessary information.
            self.redraw_opihi_image()
            self.refresh_dynamic_label_text()
            self.save_auto_save()
            return None

        orbit_thread = threading.Thread(target=orbit_solving_function)
        orbit_thread.start()
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

        # Note that we are busy solving the solution via the engine.
        self.__configuration_draw_busy_image()

        # Solve the field using the provided engine. We need to break this out
        # into its own thread so that the busy plot notification can be shown
        # to the user. The GUI thread is otherwise blocked.
        def ephemeris_solving_function():
            """The function to solve the ephemeris and refresh the plots."""
            __ = self.opihi_solution.solve_ephemeris(
                solver_engine=engine, overwrite=True, vehicle_args=vehicle_args
            )
            # Update all of the necessary information.
            self.redraw_opihi_image()
            self.refresh_dynamic_label_text()
            self.save_auto_save()
            return None

        ephemeris_thread = threading.Thread(target=ephemeris_solving_function)
        ephemeris_thread.start()
        # All done.
        return None

    def __connect_push_button_ephemeris_update_tcs_rate(self) -> None:
        """A routine to update the non-sidereal rates of the TCS as provided
        by the ephemeritic solution.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no ephemeritic solution, there is nothing to be done.
        if not isinstance(
            self.opihi_solution.ephemeritics, ephemeris.EphemeriticSolution
        ):
            return None

        # We use the ephemeritic solution rates to update the TCS, the
        # function provided already converts the values as needed
        # so we can provide the units as per convention.
        # We do not care about the response for now.
        __ = library.tcs.t3io_tcs_ns_rate(
            ra_velocity=self.opihi_solution.ephemeritics.ra_velocity,
            dec_velocity=self.opihi_solution.ephemeritics.dec_velocity,
        )

        # All done.
        return None

    def __connect_push_button_ephemeris_custom_solve(self) -> None:
        """Solving for the location of the target through the ephemeris based
        on the time and date provided by the user.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no ephemeris solution, there is nothing to be done.
        if not isinstance(
            self.opihi_solution.ephemeritics, ephemeris.EphemeriticSolution
        ):
            return None

        # Get the time and date from the user input.
        datetime_input = self.ui.date_time_edit_ephemeris_date_time.dateTime()
        # Getting the timezone, as the ephemeris requires UTC/JD time, a
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

        # Using this unique time provided to solve the forward ephemeris.
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

        # Note that we are busy solving the solution via the engine.
        self.__configuration_draw_busy_image()

        # Solve the field using the provided engine. We need to break this out
        # into its own thread so that the busy plot notification can be shown
        # to the user. The GUI thread is otherwise blocked.
        def propagate_solving_function():
            """The function to solve the propagation and refresh the plots."""
            __ = self.opihi_solution.solve_propagate(
                solver_engine=engine, overwrite=True, vehicle_args=vehicle_args
            )
            # Update all of the necessary information.
            self.redraw_opihi_image()
            self.refresh_dynamic_label_text()
            self.save_auto_save()
            return None

        propagate_thread = threading.Thread(target=propagate_solving_function)
        propagate_thread.start()
        # All done.
        return None

    def __connect_push_button_propagate_update_tcs_rate(self) -> None:
        """A routine to update the non-sidereal rates of the TCS as provided
        by the propagation solution.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no propagative solution, there is nothing to be done.
        if not isinstance(
            self.opihi_solution.propagatives, propagate.PropagativeSolution
        ):
            return None

        # We use the propagative solution rates to update the TCS, the
        # function provided already converts the values as needed
        # so we can provide the units as per convention.
        # We do not care about the response for now.
        __ = library.tcs.t3io_tcs_ns_rate(
            ra_velocity=self.opihi_solution.propagatives.ra_velocity,
            dec_velocity=self.opihi_solution.propagatives.dec_velocity,
        )

        # All done.
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
        if self.asteroid_set_name is None:
            raise error.SequentialOrderError(
                "There is no asteroid name to derive the MPC record filename from."
            )
        else:
            mpc_target_name = self.asteroid_set_name

        suffix = str(library.config.GUI_MANUAL_DEFAULT_MPC_RECORD_SAVING_SUFFIX)
        mpc_record_filename = mpc_target_name + suffix
        # Search the same directory as the fits file for this information as
        # that is currently the expected location.
        # Preferring the preprocessed filename if it exists, have a fall back.
        fits_pathname = (
            self.raw_fits_filename if self.fits_filename is None else self.fits_filename
        )
        if fits_pathname is not None:
            fits_directory = library.path.get_directory(pathname=fits_pathname)
        else:
            raise error.SequentialOrderError(
                "There is no FITS file to derive the directory where the MPC record"
                " file should go."
            )
        mpc_record_filename = library.path.merge_pathname(
            directory=fits_directory, filename=mpc_record_filename, extension="txt"
        )
        return mpc_record_filename

    def __get_saving_fits_filename(self) -> str:
        """This is a function which derives the FITS filename which will be
        used to save the results of the many computations done for this given
        image.

        Parameters
        ----------
        None

        Returns
        -------
        saving_fits_filename : str
            The filename of the MPC record for this object/image.
        """
        # We can use OpihiSolution's built-in function, but we need to
        # define the filename. Adding a suffix is sufficient here.
        if self.fits_filename is not None:
            reference_fits_filename = self.fits_filename
        else:
            reference_fits_filename = self.raw_fits_filename
        # Check if a proper filename exists.
        if reference_fits_filename is None:
            raise error.SequentialOrderError(
                "There is no fits filename to derive the saving fits filename."
            )

        # Extracting the entire path from the current name, we are saving it
        # to the same location.
        directory, basename, extension = library.path.split_pathname(
            pathname=reference_fits_filename
        )
        # We are just adding the suffix to the filename.
        suffix = str(library.config.GUI_MANUAL_DEFAULT_FITS_SAVING_SUFFIX)
        new_filename = basename + suffix
        # Recombining the path.
        saving_fits_filename = library.path.merge_pathname(
            directory=directory, filename=new_filename, extension=extension
        )
        return saving_fits_filename

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

        # Extracting the header of this fits file to get the observing
        # metadata from it.
        header, __ = library.fits.read_fits_image_file(filename=fits_filename)

        # The filter which image is in, extracted from the fits file,
        # assuming standard form.
        filter_header_string = str(header["FWHL"])
        filter_name = library.conversion.filter_header_string_to_filter_name(
            header_string=filter_header_string
        )

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
            if isinstance(self.asteroid_set_name, str):
                mpcrecord_filename = self.__get_mpc_record_filename()
                # Reading the file, or making one if it does not already exist.
                if not os.path.isfile(mpcrecord_filename):
                    with open(mpcrecord_filename, "w"):
                        pass
                # Read the historical data.
                with open(mpcrecord_filename, "r") as mpcfile:
                    raw_lines = mpcfile.readlines()
                    # The files have new line characters on them, they need
                    # to be removed to have the normal 80 characters.
                    asteroid_history = [
                        linedex.removesuffix("\n") for linedex in raw_lines
                    ]
            else:
                # The MPC record filename does not exist because there is
                # no specified asteroid name.
                asteroid_history = None
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
        # The target name and the directory the images are in should
        # not reset just because of a new image.
        # self.ui.label_dynamic_summary_target_name.setText("None")
        # self.ui.label_dynamic_summary_directory.setText("/path/to/dir/")
        self.ui.label_dynamic_summary_fits_file.setText(
            "opi.20XXA999.YYMMDD.AAAAAAAAA.00001.a.fits"
        )
        self.ui.line_edit_summary_save_filename.setText("")

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
        # All of this information does not depend on an OpihiSolution.
        self.__refresh_dynamic_label_text_summary()

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

    def __refresh_dynamic_label_text_summary(self) -> None:
        """Refresh all of the dynamic label text for the summary.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Refreshing the target name and the FITS filename.
        if self.asteroid_set_name is not None:
            self.ui.label_dynamic_summary_target_name.setText(
                str(self.asteroid_set_name)
            )

        # A FITS filename has to have been provided to fill in the file
        # path location of it.
        if self.fits_filename is not None:
            self.ui.label_dynamic_summary_directory.setText(
                library.path.get_directory(pathname=self.fits_filename)
            )
            self.ui.label_dynamic_summary_fits_file.setText(
                library.path.get_filename_with_extension(pathname=self.fits_filename)
            )

        # Refreshing the saving filename if possible.
        try:
            self.ui.line_edit_summary_save_filename.setText(
                self.__get_saving_fits_filename()
            )
        except error.SequentialOrderError:
            # There is no FITS filename to update with.
            pass

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

        # Obtaining the computed magnitude of the target as computed. Some
        # rounding is needed so it can properly fit in the GUI.
        asteroid_magnitude = round(opihi_solution.asteroid_magnitude, 2)
        asteroid_magnitude_error = round(opihi_solution.asteroid_magnitude_error, 3)
        # Building the string for display and updating the text.
        pm_sym = "\u00B1"
        magnitude_str = "{mag} {pm} {err}".format(
            mag=asteroid_magnitude, pm=pm_sym, err=asteroid_magnitude_error
        )
        self.ui.label_dynamic_photometry_magnitude.setText(magnitude_str)

        # Obtaining the computed zero point of the image. Some rounding is
        # needed so it can properly fit in the GUI.
        zero_point = round(photometrics.zero_point, 3)
        zero_point_error = round(photometrics.zero_point_error, 4)
        # Building the string for display and updating the text.
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

        # There is no solution and thus no image can be plotted.
        if self.opihi_solution is None:
            return None

        # These are points in future time which will be used to plot the
        # ephemeris and propagation solutions, if they exist. However,
        # as the time step is in seconds, and the standard time of this
        # system is in Julian days, we convert.
        if isinstance(self.opihi_solution.observing_time, (int, float)):
            # We can only do this if we know the time that the image was taken
            # at.
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
            # It does not work, something is wrong with the asteroid location
            # provided.
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

    def draw_busy_image(self, replace: bool = True, transparency: float = 1) -> None:
        """This draws the busy image.

        We draw the busy image on top of the Opihi image to signify that
        the software is going to be doing something and will be busy for a
        short time. As the window will be frozen for a period of time, the
        plot will not be intractable so it does not matter that we use that
        space. It also means that a separate window won't be needed and the
        user would not get confused or miss it.

        Parameters
        ----------
        replace : bool, default = True
            If True, we replace the Opihi image with the busy image instead
            of over-plotting it. This does not affect the Opihi image in
            general and it can be restored with a redraw.
        transparency : float, default = 1
            If `replace` is False, the image is instead over-plotted with the
            transparency provided here.

        Returns
        -------
        None
        """
        # If we replace the image, there is no need for transparency to be
        # anything but one. We also clear the plot at this step.
        if replace:
            # Clearing the plot as we are replacing it with the busy image.
            self.opihi_axes.clear()
            # Doesn't really make sense to have a transparency when replacing
            # the image.
            transparency = 1
        else:
            # We do a transparency value check to make sure it is between the
            # values as described.
            if 0 <= transparency <= 1:
                # All good.
                transparency = float(transparency)
            else:
                raise error.InputError(
                    "The transparency value {alpha} provided is not a number between 0"
                    " and 1.".format(alpha=transparency)
                )

        # We load the busy image.
        busy_image = gui.functions.get_busy_image_array()

        # Determining the width/height shape of the image.
        busy_height, busy_width, __ = busy_image.shape
        # From the shape of the image, and the shape of the array, we pin the
        # origin of the image. We desired a centered image.
        data_height, data_width = self.opihi_solution.data.shape

        # Defining the extents.
        left_extent = (
            0 if busy_width > data_width else data_width // 2 - busy_width // 2
        )
        right_extent = (
            data_width if busy_width > data_width else data_width // 2 + busy_width // 2
        )
        bottom_extent = (
            0 if busy_height > data_height else data_height // 2 - busy_height // 2
        )
        top_extent = (
            data_height
            if busy_height > data_height
            else data_height // 2 + busy_height // 2
        )

        # Showing the image.
        self.opihi_axes.imshow(
            busy_image,
            aspect="equal",
            alpha=transparency,
            extent=(left_extent, right_extent, bottom_extent, top_extent),
            zorder=10,
        )
        # Redraw the canvas.
        self.opihi_canvas.draw()
        # All done.
        return None

    def __configuration_draw_busy_image(self) -> None:
        """Exactly the same as `draw_busy_image`, but we use the settings
        as per the configuration. This function is just a connivent wrapper.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Getting the configuration values.
        config_replace = library.config.GUI_MANUAL_BUSY_ALERT_IMAGE_REPLACEMENT
        config_transparency = library.config.GUI_MANUAL_BUSY_ALERT_IMAGE_TRANSPARENCY
        # Executing the plotting.
        self.draw_busy_image(replace=config_replace, transparency=config_transparency)
        # All done.
        return None

    def save_auto_save(self) -> None:
        """This function should be used when auto save is active across
        every and all aspects of the GUI where automatic saving is desired.

        Auto-saving is enabled by the checkbox.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        autosave_bool = bool(self.ui.check_box_summary_autosave.isChecked())
        if autosave_bool:
            try:
                self.save_all_results()
            except Exception:
                raise
        else:
            # No auto-save.
            pass
        # All done.
        return None

    def save_all_results(self) -> None:
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
        # Beginning with the FITS file. We get the filename to save the FITS
        # file as and try to save it.
        saving_fits_filename = str(self.ui.line_edit_summary_save_filename.text())
        if len(saving_fits_filename) == 0:
            # If the saving filename is blank then we ought to try an
            # alternative by trying to derive the name from the fits file.
            try:
                saving_fits_filename = self.__get_saving_fits_filename()
            except error.SequentialOrderError:
                # There is no FITS file to even derive the filename. We cannot
                # save the FITS file.
                saving_fits_filename = None
        # Attempt to save the file.
        if saving_fits_filename is None:
            # There is no FITS filename to save as. We cannot save the file.
            print("warn fits not save.")
        else:
            # Attempt to save the file.
            self._save_fits_file_results(fits_filename=saving_fits_filename)

        # Next the MPC record file. We get the filename to save the mpc
        # record file as and try to save it.
        try:
            saving_mpcrecord_filename = self.__get_mpc_record_filename()
        except error.SequentialOrderError:
            # There is no FITS file to even derive the filename. We cannot
            # save the FITS file.
            saving_mpcrecord_filename = None
        # Attempt to save the file.
        if saving_mpcrecord_filename is None:
            # There is no MPC record filename to save as. We cannot save the
            # file.
            print("warn mpc not save.")
        else:
            # Attempt to save the file.
            self._save_mpc_record_results(record_filename=saving_mpcrecord_filename)

        # All done.
        return None

    def _save_fits_file_results(self, fits_filename: str) -> None:
        """We save the results which can be stored in a FITS file, this is
        typically the data and other related information.

        Parameters
        ----------
        fits_filename : string
            The fits filename which it will be saved to.

        Returns
        -------
        None
        """
        # If there is no solution class, there is nothing to save. Exiting
        # early.
        if not isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            return None
        # Saving, it should be fine as we overwrite as only more data will
        # be added.
        self.opihi_solution.save_to_fits_file(filename=fits_filename, overwrite=True)
        # All done.
        return None

    def _save_mpc_record_results(self, record_filename: str) -> None:
        """We save the MPC record information which can be saved as a
        text file.

        Parameters
        ----------
        record_filename : string
            The text filename which will contain the 80-column MPC formatted
            list of asteroid observations.

        Returns
        -------
        None
        """
        # The OpihiSolution class does not exist so there is nothing for it
        # to provide. However, if there is no file, we still can create it.
        if not isinstance(self.opihi_solution, opihiexarata.OpihiSolution):
            if os.path.isfile(record_filename):
                # We do not want to overwrite something if we have nothing to
                # provide it.
                return None
            else:
                with open(record_filename, "w") as mpcfile:
                    pass

        # The current record to add.
        try:
            mpc_record = self.opihi_solution.mpc_record_full()
        except error.PracticalityError:
            # If the user did not solve for astrometry, this will raise
            # because it cannot properly make an MPC row. We ignore it
            # and we do not add any observational data. We just return it
            # to the state it was.
            mpc_record = self.opihi_solution.asteroid_history
        finally:
            # Adding the new line character as write lines do not do this
            # to make the multi-rowed file.
            mpc_record = [rowdex + "\n" for rowdex in mpc_record]
        # If the record file already exists, replace our information with
        # it. We can do this because we already are using their data.
        with open(record_filename, "w") as mpcfile:
            mpcfile.writelines(mpc_record)
        return None

    def __write_zero_point_record_to_database(
        self, opihi_solution: hint.OpihiSolution
    ) -> None:
        """This function writes the zero point information assuming a solved
        photometric solution. This function is so that threading this process
        away is a lot easier.

        Parameters
        ----------
        opihi_solution : OpihiSolution
            The solution class of the image.

        Returns
        -------
        None
        """
        # The photometry solution must exist and it must be properly solved.
        if not isinstance(opihi_solution.photometrics, photometry.PhotometricSolution):
            return None
        if not opihi_solution.photometrics_status:
            return None
        # The database solution must exist to write to, and the user must
        # actually want to write to it.
        if not isinstance(
            self.zero_point_database, opihiexarata.OpihiZeroPointDatabaseSolution
        ):
            return None
        if not library.config.GUI_MANUAL_DATABASE_SAVE_OBSERVATIONS:
            return None

        # Because many files are being written to the database, we do not
        # want to try and busy the database with cleaning itself up every time
        # we want to write to it so we do it randomly.
        CLEAN_RATE = library.config.GUI_MANUAL_DATABASE_CLEAN_FILE_RATE
        will_clean_record_file = np.random.random() <= CLEAN_RATE

        # We write the record based on the information from the solution.
        self.zero_point_database.write_zero_point_record_julian_day(
            jd=opihi_solution.observing_time,
            zero_point=opihi_solution.photometrics.zero_point,
            zero_point_error=opihi_solution.photometrics.zero_point_error,
            filter_name=opihi_solution.filter_name,
            clean_file=will_clean_record_file,
        )

        # We additionally create a new figure for the monitoring webpage.
        self.zero_point_database.create_plotly_monitoring_html_plot_via_configuration()

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
