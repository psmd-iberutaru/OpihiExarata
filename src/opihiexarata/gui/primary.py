"""
The primary GUI window.
"""

import time
import sys
import os

import PyQt6 as PyQt
from PyQt6 import QtCore, QtWidgets, QtGui

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

# import opihiexarata.ephemeris as ephemeris

import opihiexarata.gui as gui


class OpihiPrimaryWindow(QtWidgets.QMainWindow):
    """The GUI that is responsible for interaction between the user and the
    two primary Opihi solutions, the image (OpihiPreprocessSolution) and the
    results (OpihiSolution).

    Only non-GUI attributes are listed here.

    Attributes
    ----------
    asteroid_set_name
    raw_fits_filename
    raw_record_filename
    process_fits_filename
    preprocess_solution
    opihi_solution

    """

    def __init__(self) -> None:
        """The primary GUI window for OpihiExarata. This interacts directly
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
        super(OpihiPrimaryWindow, self).__init__()
        self.ui = gui.qtui.Ui_PrimaryWindow()
        self.ui.setupUi(self)

        # Establishing the defaults for all of the relevant attributes.
        self.asteroid_set_name = None
        self.raw_fits_filename = None
        self.raw_record_filename = None
        self.process_fits_filename = None
        self.preprocess_solution = None
        self.opihi_solution = None

        # Preparing the buttons and their functionality.
        self.__init_push_button_connections()

        # Preparing the image area for Opihi sky images.
        self.__init_opihi_image()

        # Preparing the preprocessing solution so that the raw files loaded
        # into Exarata can be instantly turned into reduced images.
        self.__init_preprocess_solution()

        # All done.
        return None

    def __init_push_button_connections(self) -> None:
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

            def __init__(self, gui_instance: OpihiPrimaryWindow) -> None:
                self.gui_instance = gui_instance
                return None

            def __call__(self, x, y) -> str:
                """The coordinate string going to be put onto the navigation
                bar."""
                x_index = int(x)
                y_index = int(y)
                coord_string = "Helllo [{x_int:d}, {y_int:d}]".format(
                    x_int=x_index, y_int=y_index
                )
                return coord_string

        # Assigning the coordinate formatter derived.
        self._opihi_coordinate_formatter = CoordinateFormatter(self)
        self.opihi_axes.format_coord = self._opihi_coordinate_formatter

        # Setting the layout, it is likely better to have the toolbar below
        # rather than above to avoid conflicts with the reset buttons in the
        # event of a misclick.
        self.ui.vertical_layout_image.addWidget(self.opihi_canvas)
        self.ui.vertical_layout_image.addWidget(self.opihi_nav_toolbar)
        # Remove the dummy spacers otherwise it is just extra unneeded space.
        self.ui.vertical_layout_image.removeWidget(self.ui.dummy_opihi_image)
        self.ui.vertical_layout_image.removeWidget(self.ui.dummy_opihi_navbar)
        self.ui.dummy_opihi_image.deleteLater()
        self.ui.dummy_opihi_navbar.deleteLater()
        self.ui.dummy_opihi_image = None
        self.ui.dummy_opihi_navbar = None
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
        """The automatic method relying on earliest fits file avaliable in
        the expected directory. This function is a connected function action to
        a button in the GUI.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # TODO
        new_fits_filename = "pie"

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
        """The manual method relying on earliest fits file avaliable in
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
            directory="./",
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
        # Determine the engine from user input.
        engine = astrometry.AstrometryNetWebAPIEngine
        # Solve.
        __ = self.opihi_solution.solve_astrometry(solver_engine=engine, overwrite=True)
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

        # Prioritize the presense of the pixel location text.
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
        # Determine the engine from user input.
        engine = propagate.LinearPropagationEngine
        # Solve.
        __ = self.opihi_solution.solve_propagate(solver_engine=engine, overwrite=True)

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
            self.opihi_solution.propagatives, propagate.PropagationSolution
        ):
            return None

        # Get the time and date from the user input.
        datetime_input = self.ui.date_time_edit_propagate_date_time.dateTime()
        # Getting the timezone, as the propagation requires UTC/UNIX time, a
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
                "The timezone dropdown entry provided by the GUI is not implimented and"
                " has no translation to an IANA timezone ID."
            )

        # Using Qt's own datetime conversion just because it is already here.
        qt_timezone_bytearray = QtCore.QByteArray(qt_timezone_str.encode())
        qt_timezone = QtCore.QTimeZone(qt_timezone_bytearray)
        datetime_input.setTimeZone(qt_timezone)
        unix_time_input = datetime_input.toSecsSinceEpoch()

        # Using this unique time provided to solve the propagation.
        ra_deg, dec_deg = self.opihi_solution.propagatives.forward_propagate(
            future_time=unix_time_input
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
        header, data = library.fits.read_fits_image_file(filename=fits_filename)

        # The filter which image is in, extracted from the fits file,
        # assuming standard form.
        filter_name = "g"

        # The exposure time of the image, extracted from the fits file,
        # assuming standard form.
        exposure_time = float(header["ITIME"])

        # Converting date to UNIX as the solution class requires it.
        # The YMD and HMS formats in the header file are UTC in a
        # ISO 8601 like format.
        yr_s, mh_s, dy_s = header["DATE_OBS"].split("-")
        hr_s, mn_s, sc_s = header["TIME_OBS"].split(":")
        # These values are currently strings, they need to be the proper type.
        yr_i = int(yr_s)
        mh_i = int(mh_s)
        dy_i = int(dy_s)
        hr_i = int(hr_s)
        mn_i = int(mn_s)
        sc_f = float(sc_s)
        # Convert.
        observing_time = library.conversion.full_date_to_unix_time(
            year=yr_i, month=mh_i, day=dy_i, hour=hr_i, minute=mn_i, second=sc_f
        )

        # For asteroid information, if we are to prompt the user for
        # information about the asteroid.
        if library.config.GUI_PROMPT_FOR_ASTEROID_INFORMATION:
            # The name is derived from the current object set that we are on.
            asteroid_name = self.asteroid_set_name
            # Use the target selector GUI for the position of the asteroid.
            asteroid_location = gui.selector.ask_user_target_selector_window(
                data_array=data
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

    def clear_dynamic_label_text(self) -> None:
        """Clear all of the dynamic label text and other related fields,
        this is traditionally done just before a new image is going to be
        introduced.

        This resets the text back to their defaults as per the GUI builder.

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

        ## Resetting Orbit information.
        #####

        ## Resetting Ephemeris information.
        #####

        ## Resetting Propagate information.
        #####
        self.ui.label_dynamic_propagate_ra_velocity.setText("+VV.VVV")
        self.ui.label_dynamic_propagate_dec_velocity.setText("+VV.VVV")
        self.ui.label_dynamic_propagate_ra_acceleration.setText("+AA.AAA")
        self.ui.label_dynamic_propagate_dec_acceleration.setText("+AA.AAA")
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
        information based on the current solutions avaliable and solved.

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
            self.__refresh_dynamic_label_text_propagate()

        # All done.
        return None

    def __refresh_dynamic_label_text_astrometry(self) -> None:
        """Refresh all of the dynamic label text for astrometry.
        This fills out the information based on the current solutions
        avaliable and solved.

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

    def __refresh_dynamic_label_text_propagate(self) -> None:
        """Refresh all of the dynamic label text for propagate.
        This fills out the information based on the current solutions
        avaliable and solved.

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
            self.opihi_solution.propagatives, propagate.PropagationSolution
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
        # Converting to the more familiar arcsec/s. Round after and prepare
        # to make it a string for the GUI.
        def deg_to_arcsec_str(degree: float) -> str:
            return str(round(degree * 3600, 3))

        ra_v_arcsec_str = deg_to_arcsec_str(ra_v_deg)
        dec_v_arcsec_str = deg_to_arcsec_str(dec_v_deg)
        ra_a_arcsec_str = deg_to_arcsec_str(ra_a_deg)
        dec_a_arcsec_str = deg_to_arcsec_str(dec_a_deg)
        # Update the dynamic text.
        self.ui.label_dynamic_propagate_ra_velocity.setText(ra_v_arcsec_str)
        self.ui.label_dynamic_propagate_dec_velocity.setText(dec_v_arcsec_str)
        self.ui.label_dynamic_propagate_ra_acceleration.setText(ra_a_arcsec_str)
        self.ui.label_dynamic_propagate_dec_acceleration.setText(dec_a_arcsec_str)

        # Use the current time and date to determine the future positions with
        # the time interval provided.
        ENTRY_COUNT = library.config.GUI_PROPAGATE_PRECOMPUTED_FUTURE_ENTRY_COUNT
        INTERVAL = library.config.GUI_PROPAGATE_PRECOMPUTED_FUTURE_TIMESTEP_SECONDS
        current_unix_time = time.time()
        precomputed_future_text = ""
        for countdex in range(int(ENTRY_COUNT)):
            # The unix time for this future.
            future_unix_time = current_unix_time + INTERVAL * countdex
            # Converting this to the date and time string for this entry.
            # As this is UNIX time, the date is in UTC or Zulu time.
            yr, mh, dy, hr, mn, sc = library.conversion.unix_time_to_full_date(
                unix_time=future_unix_time
            )
            datetime_str = "{yr}-{mh}-{dy}  {hr}:{mn}:{sc}  Z".format(
                yr=int(yr), mh=int(mh), dy=int(dy), hr=int(hr), mn=int(mn), sc=int(sc)
            )
            # Using the unix time to compute the propagated solution for this
            # time and formatting this as the needed string.
            ra_deg, dec_deg = propagatives.forward_propagate(
                future_time=future_unix_time
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
        # This is a function which allows for the disabling of other axes
        # formatting their data values and messing with the formatter class.
        def empty_string(string: str) -> str:
            return str()

        # Clear the information before replotting, it is easier just to draw
        # it all again.
        self.opihi_axes.clear()

        # Attempt to plot the image data if it exists.
        if self.opihi_solution is not None:
            image = self.opihi_axes.imshow(self.opihi_solution.data, cmap="gray")
            # Disable their formatting in favor of ours.
            image.format_cursor_data = empty_string

        # Attempt to plot the location of the specified asteroid.
        try:
            target_x, target_y = self.opihi_solution.asteroid_location
            TARGET_MARKER_SIZE = float(library.config.GUI_IMAGE_PLOT_TARGET_MARKER_SIZE)
            target_marker = self.opihi_axes.scatter(
                target_x,
                target_y,
                s=TARGET_MARKER_SIZE,
                marker="^",
                color="r",
                facecolors="None",
            )
            # Disable their formatting in favor of ours.
            target_marker.format_cursor_data = empty_string
        except Exception:
            pass

        # TESTING
        rand = np.random.rand(5)
        self.opihi_axes.plot(rand, 1 / rand)

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
        # information and the MPC record as retriveable historical data.
        def _save_results_fits_image() -> None:
            """First, doing the image data."""

        def _save_results_mpcrecord() -> None:
            """Second, the MPC record historical data."""
            # The current record to add.
            mpc_record = self.opihi_solution.mpc_record_row()
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


def main():
    app = QtWidgets.QApplication([])

    application = OpihiPrimaryWindow()

    application.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
