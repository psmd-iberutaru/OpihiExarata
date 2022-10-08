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
    fits_filename_list : string
        The FITS filenames of the data for the image/files. If
        any of the entries are None, then no file was specified.

    last_used_directory : string
        The default directory where the file dialog should open up should be
        the last directory that the file dialog loaded a file from.

    primary_file_index : int
        The primary file number which to work on. This is determined by the
        radio buttons on the GUI and is the file/data which is considered the
        preferable one for some computations.

    target_set_name : string
        The name of the target. This is typically extracted from the filenames
        but may otherwise be manually specified.


    opihi_solution_list : list
        This is a container which contains all of the Opihi solutions for all
        of the FITS files/images specified. If any of the entries are None,
        then no file was provided or the solution class could not be created
        from the file for some reason.
    preprocess_solution : OpihiPreprocessSolution
        The preprocessing solution which is used to convert raw images to
        preprocessed files.
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

        # These defaults are later overwritten with something more clever and
        # appropriate. Establishing the dummy defaults for....
        # ...the filenames.
        self.fits_filename_list = [error.IntentionalError, None, None, None, None]
        # ...the file dialog.
        self.last_used_directory = None
        # ...the file index.
        self.primary_file_index = None
        # ...the asteroid/target set name and other information.
        self.target_set_name = None
        # ...the solutions. We follow the indexing of the GUI for the
        # OpihiSolutions. So, to avoid off-by-one errors, we just add a filler
        # into the 0th index location.
        self.opihi_solution_list = [error.IntentionalError, None, None, None, None]
        self.preprocess_solution = None
        self.zero_point_database = None

        # True initialization...
        # Preparing the preprocessing solution so that the raw files loaded
        # into Exarata can be instantly turned into reduced images.
        self.__init_preprocess_solution()
        # Preparing the image area for Opihi sky images.
        self.__init_opihi_image()
        # Creating the zero point database. Or more specifically, its API.
        self.__init_zero_point_database()

        # Preparing the buttons, GUI, and other functionality.
        self.__init_gui_connections()
        # Preparing the radio buttons, or, more specifically, specifying the
        # primary index. We borrow the connection for this.
        self.__connect_button_group_primary_working_file()

        # Finally, a reset to bring it all to normal.
        self.reset_all()
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
        # The total reset button.
        #####
        self.ui.push_button_reset.clicked.connect(self.__connect_push_button_reset)

        # The filename and target location changing buttons. The primary
        # radio button is also defined here.
        #####
        self.ui.push_button_change_filename_1.clicked.connect(
            lambda: self.__connect_push_button_change_filename(index=1)
        )
        self.ui.push_button_change_filename_2.clicked.connect(
            lambda: self.__connect_push_button_change_filename(index=2)
        )
        self.ui.push_button_change_filename_3.clicked.connect(
            lambda: self.__connect_push_button_change_filename(index=3)
        )
        self.ui.push_button_change_filename_4.clicked.connect(
            lambda: self.__connect_push_button_change_filename(index=4)
        )
        self.ui.push_button_locate_target_location_1.clicked.connect(
            lambda: self.__connect_push_button_locate_target_location(index=1)
        )
        self.ui.push_button_locate_target_location_2.clicked.connect(
            lambda: self.__connect_push_button_locate_target_location(index=2)
        )
        self.ui.push_button_locate_target_location_3.clicked.connect(
            lambda: self.__connect_push_button_locate_target_location(index=3)
        )
        self.ui.push_button_locate_target_location_4.clicked.connect(
            lambda: self.__connect_push_button_locate_target_location(index=4)
        )
        self.ui.radio_button_primary_file_1.clicked.connect(
            self.__connect_button_group_primary_working_file
        )
        self.ui.radio_button_primary_file_2.clicked.connect(
            self.__connect_button_group_primary_working_file
        )
        self.ui.radio_button_primary_file_3.clicked.connect(
            self.__connect_button_group_primary_working_file
        )
        self.ui.radio_button_primary_file_4.clicked.connect(
            self.__connect_button_group_primary_working_file
        )

        # The summary page buttons and other functionality.
        self.ui.push_button_change_target_name.clicked.connect(
            self.__connect_push_button_change_target_name
        )
        self.ui.push_button_send_target_to_tcs.clicked.connect(self.__connect_push_button_send_target_to_tcs)

        # The astrometry page and other functionality.
        self.ui.push_button_solve_astrometry.clicked.connect(
            self.__connect_push_button_solve_astrometry
        )
        self.ui.push_button_astrometry_custom_solve.clicked.connect(
            self.__connect_push_button_astrometry_custom_solve
        )

        # The photometry page and other functionality.
        self.ui.push_button_solve_photometry.clicked.connect(
            self.__connect_push_button_solve_photometry
        )

        # The orbit page and other functionality.
        self.ui.push_button_solve_orbit.clicked.connect(
            self.__connect_push_button_orbit_solve_orbit
        )

        # The ephemeris page and other functionality.
        self.ui.push_button_solve_ephemeris.clicked.connect(
            self.__connect_push_button_solve_ephemeris
        )
        self.ui.push_button_ephemeris_results_update_tcs_rates.clicked.connect(
            self.__connect_push_button_ephemeris_results_update_tcs_rates
        )
        self.ui.push_button_ephemeris_forward_solve.clicked.connect(
            self.__connect_push_button_ephemeris_forward_solve
        )

        # The propagation page and other functionality.
        self.ui.push_button_solve_propagation.clicked.connect(
            self.__connect_push_button_solve_propagation
        )
        self.ui.push_button_propagate_results_update_tcs_rates.clicked.connect(
            self.__connect_push_button_propagate_results_update_tcs_rates
        )
        self.ui.push_button_propagate_forward_solve.clicked.connect(
            self.__connect_push_button_propagate_forward_solve
        )

        # All done
        return None

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
        dpi = self.logicalDpiY()
        pix_to_in = lambda p: p / dpi
        dummy_edge_size_px = self.ui.graphics_view_dummy_opihi_image.maximumHeight()
        edge_size_in = pix_to_in(dummy_edge_size_px)

        # The figure, canvas, and navigation toolbar of the image plot
        # using a Matplotlib Qt widget backend. We will add these to the
        # layout later.
        fig, ax = plt.subplots(figsize=(edge_size_in, edge_size_in), dpi=dpi,constrained_layout=True)
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
                except (AttributeError, IndexError):
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

        # Setting the size of the canvas to be more representative of the 
        # designer file.
        self.opihi_canvas.setMinimumHeight(dummy_edge_size_px)
        self.opihi_canvas.setMaximumHeight(dummy_edge_size_px)
        self.opihi_canvas.setMinimumWidth(dummy_edge_size_px)
        self.opihi_canvas.setMaximumWidth(dummy_edge_size_px)
        # And setting the navigation bar.
        self.opihi_nav_toolbar.setMaximumWidth(dummy_edge_size_px)

        # Remove the dummy spacers otherwise it is just extra unneeded space.
        self.ui.vertical_layout_image.removeWidget(
            self.ui.graphics_view_dummy_opihi_image
        )
        self.ui.vertical_layout_image.removeWidget(
            self.ui.label_static_dummy_opihi_navbar
        )
        self.ui.graphics_view_dummy_opihi_image.hide()
        self.ui.label_static_dummy_opihi_navbar.hide()
        self.ui.graphics_view_dummy_opihi_image.deleteLater()
        self.ui.label_static_dummy_opihi_navbar.deleteLater()
        del self.ui.graphics_view_dummy_opihi_image
        del self.ui.label_static_dummy_opihi_navbar
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

    def __init_zero_point_database(self) -> None:
        """This function initializes the zero point database as specified
        by the configuration file.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Preparing the zero point database if the user desired the database
        # to record observations.
        if library.config.GUI_MANUAL_DATABASE_SAVE_OBSERVATIONS:
            database = opihiexarata.OpihiZeroPointDatabaseSolution(
                database_directory=library.config.MONITOR_DATABASE_DIRECTORY
            )
        else:
            database = None
        self.zero_point_database = database
        return None

    def __connect_push_button_reset(self) -> None:
        """This resets the entire GUI, removing all of the information solved
        or unsolved.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Just in case, we batch save everything before doing a total reset.
        self.save_all_fits_files()
        self.save_target_history_archive(archive_filename=None)

        # Resetting everything.
        self.reset_all()

        # All done.
        return None

    def __connect_push_button_change_filename(self, index: int) -> None:
        """The method for loading in a new file(name) for a file based on the
        index.

        Parameters
        ----------
        index : int
            The file index of which this loading should be for.

        Returns
        -------
        None
        """
        # We save the old file before actually changing the file.
        self.save_index_fits_file(index=index)

        # Ask the user for the filename via a dialog.
        new_fits_filename, __ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Open Opihi Image {i}".format(i=index),
            dir=self.last_used_directory,
            filter="FITS Files (*.fits)",
        )
        # If the user did not provide a file to enter, there is nothing to be
        # changed.
        if not os.path.isfile(new_fits_filename):
            # Exit!
            return None

        # We desire to reduce the data if a preprocess solution exists to do so.
        if isinstance(self.preprocess_solution, opihiexarata.OpihiPreprocessSolution):
            # We want to check if the FITS file has already been preprocessed.
            header, __ = library.fits.read_fits_image_file(filename=new_fits_filename)
            was_processed = header.get("OXM_REDU", False)
            if was_processed:
                # The user already loaded a preprocessed FITS file, there is
                # no reason to preprocess it again.
                current_fits_filename = new_fits_filename
            else:
                # We derive the FITS filename for the preprocessed solution, if it
                # exists.
                nf_dir, nf_base, nf_ext = library.path.split_pathname(
                    pathname=new_fits_filename
                )
                # Appending the preprocessing suffix.
                PREPROCESS_SUFFIX = library.config.PREPROCESS_DEFAULT_SAVING_SUFFIX
                current_fits_filename = library.path.merge_pathname(
                    directory=nf_dir,
                    filename=nf_base + PREPROCESS_SUFFIX,
                    extension=nf_ext,
                )
                # Preprocessing the input file.
                self.preprocess_solution.preprocess_fits_file(
                    raw_filename=new_fits_filename, out_filename=current_fits_filename
                )
        else:
            # There is no preprocessing to do.
            current_fits_filename = new_fits_filename

        # The load the fits file itself and assign it to the proper file index.
        self.fits_filename_list[index] = current_fits_filename

        # If this is the first file loaded, the target set name needs to be 
        # determined.
        if not isinstance(self.target_set_name, str):
            self.target_set_name = self._get_target_set_name_guess()

        # Derive the Opihi solution for this file.
        self.opihi_solution_list[index] = self.load_fits_file(
            fits_filename=current_fits_filename
        )
        # Because a new image was loaded, the previous values and other
        # information derived from the last image are invalid, reset and
        # re-plot.
        self.reset_dynamic_label_text()
        self.refresh_dynamic_label_text()
        self.draw_opihi_image()
        # All done.
        return None

    def __connect_push_button_locate_target_location(self, index: int) -> None:
        """The method for re-determining the location of the asteroid for
        file/image of the given index.

        Parameters
        ----------
        index : int
            The file index of which the target location is being changed for.

        Returns
        -------
        None
        """
        # We cannot find the asteroid location if there is no image to load
        # or file to load.
        if self.fits_filename_list[index] is None:
            # No file to load, nothing to do.
            return None
        elif not isinstance(
            self.opihi_solution_list[index], opihiexarata.OpihiSolution
        ):
            # Nowhere to put the asteroid target location.
            return None
        else:
            # Attempt to get the correct filenames for the target selector
            # window.
            # First, the current filename for target selection.
            current_fits_filename = self.fits_filename_list[index]
            # Second, the reference filename. Assume primary, first, then
            # last. We cannot have the current filename and reference filename
            # be the same file.
            reference_fits_file = self._get_target_selector_reference_filename(
                current_filename=current_fits_filename
            )

        # We use the selector to determine the asteroid location.
        asteroid_location = gui.selector.ask_user_target_selector_window(
            current_fits_filename=current_fits_filename,
            reference_fits_filename=reference_fits_file,
        )
        
        # If the new asteroid location was not selected, then the locations 
        # are Nones and should not be applied.
        if asteroid_location == (None, None):
            pass
        else:
            # The asteroid location is saved to the proper solution.
            self.opihi_solution_list[index].asteroid_location = asteroid_location
        
        # Because a new asteroid location has been found, the previous values 
        # and other information derived from the last image are invalid, 
        # reset and re-plot.
        self.reset_dynamic_label_text()
        self.refresh_dynamic_label_text()
        self.draw_opihi_image()
        # All done.
        return None

    def __connect_button_group_primary_working_file(self) -> None:
        """On any click of the primary working file radio buttons, we
        find and apply the primary file index.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # We search all of the buttons to see which one is active, and thus
        # the primary file index.
        if self.ui.radio_button_primary_file_1.isChecked():
            primary_file_index = 1
        elif self.ui.radio_button_primary_file_2.isChecked():
            primary_file_index = 2
        elif self.ui.radio_button_primary_file_3.isChecked():
            primary_file_index = 3
        elif self.ui.radio_button_primary_file_4.isChecked():
            primary_file_index = 4
        else:
            raise error.InputError(
                "None of the radio buttons are clicked. The primary file index cannot"
                " be determined."
            )
        # And we set the primary file index to whatever it was that was
        # determined.
        self.primary_file_index = primary_file_index

        # Because the primary FITS file has changed, reset and replot.
        self.reset_dynamic_label_text()
        self.refresh_dynamic_label_text()
        self.draw_opihi_image()
        # All done.
        return None

    def __connect_push_button_change_target_name(self) -> None:
        """Change the target name of the GUI, and by extension, all of the
        OpihiSolution instances as well.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Get the name from text box.
        new_target_set_name = str(self.ui.line_edit_detected_target_name.text())
        # Setting it on the GUI level.
        self.target_set_name = new_target_set_name
        # And changing the target name for all of solution classes where
        # available.
        for index, solutiondex in enumerate(self.opihi_solution_list):
            if isinstance(solutiondex, opihiexarata.OpihiSolution):
                self.opihi_solution_list[index].asteroid_name = new_target_set_name
        # All done.
        return None

    def __connect_push_button_send_target_to_tcs(self) -> None:
        """The button which extracts the parameters of the primary image and 
        sends it to the TCS.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        # If there is no astrometric solution, nothing can be done. Exit this
        # early.
        primary_solution = self.opihi_solution_list[self.primary_file_index]
        if not isinstance(primary_solution, opihiexarata.OpihiSolution):
            print("warn")
            return None
        # In order to send the TCS the target's location, it must have been 
        # defined already. Otherwise, there is nothing to do.
        if (primary_solution.asteroid_location is None or primary_solution.asteroid_location == (None, None)):
            print("warn")
            return None
        # The astrometric solution itself is also required.
        if not (isinstance(primary_solution.astrometrics, astrometry.AstrometricSolution) and primary_solution.astrometrics_status):
            print("warn")
            return None

        # Extracting the needed parameters for the TCS command.
        # Name...
        target_name = primary_solution.asteroid_name
        # On-sky location...
        target_x, target_y = primary_solution.asteroid_location
        target_ra, target_dec = primary_solution.astrometrics.pixel_to_sky_coordinates(x=target_x, y=target_y)
        # Photometry...
        if isinstance(primary_solution.photometrics, photometry.PhotometricSolution) and primary_solution.photometrics_status:
            magnitude = primary_solution.photometrics.calculate_star_aperture_magnitude(pixel_x=target_x, pixel_y=target_y)
        else:
            # No available solution
            magnitude = 0
        # On-sky motion, we prioritize propagation.
        if isinstance(primary_solution.propagatives, propagate.PropagativeSolution) and primary_solution.propagatives_status:
            ra_velocity = primary_solution.propagatives.ra_velocity
            dec_velocity = primary_solution.propagatives.dec_velocity
        elif isinstance(primary_solution.ephemeritics, ephemeris.EphemeriticSolution) and primary_solution.ephemeritics_status:
            ra_velocity = primary_solution.ephemeritics.ra_velocity
            dec_velocity = primary_solution.ephemeritics.dec_velocity
        else:
            # No available solution
            ra_velocity = 0
            dec_velocity = 0

        # Sending the information to the TCS.
        library.tcs.t3io_tcs_next(ra=target_ra, dec=target_dec, target_name=target_name, magnitude=magnitude,ra_velocity=ra_velocity, dec_velocity=dec_velocity)
        # All done.
        return None

    def __connect_push_button_solve_astrometry(self) -> None:
        """The button to instruct on the solving of the astrometric solution.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Determine the engine from user input via the drop down menu. The
        # recognizing text ought to be case insensitive, makes life easier.
        input_engine_name = self.ui.combo_box_astrometry_engine.currentText()
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
            # Cycling through all of the indexes to try and solve the astrometry.
            # We need to use the index based method because for-loops do copying.
            for index in range(len(self.opihi_solution_list)):
                if not isinstance(
                    self.opihi_solution_list[index], opihiexarata.OpihiSolution
                ):
                    # There is nothing to solve.
                    continue
                try:
                    self.opihi_solution_list[index].solve_astrometry(
                        solver_engine=engine,
                        overwrite=True,
                        raise_on_error=True,
                        vehicle_args=vehicle_args,
                    )
                except Exception as _e:
                    print("warn", _e)
            # Finally updating all of the needed information.
            self.draw_opihi_image()
            self.refresh_dynamic_label_text()
            self.save_all_fits_files()
            # All done.
            return None

        # Starting the thread.
        astrometry_thread = threading.Thread(target=astrometry_solving_function)
        astrometry_thread.start()

        # All done.
        return None

    def __connect_push_button_astrometry_custom_solve(self) -> None:
        """The button which uses an astrometric solution to solve for a
        custom pixel location or RA DEC location depending on entry.

        This prioritizes solving RA DEC from pixel location. The OpihiSolution
        which is used is the primary solution based on the primary index.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no astrometric solution, nothing can be done. Exit this
        # early.
        primary_solution = self.opihi_solution_list[self.primary_file_index]
        if not (
            isinstance(primary_solution, opihiexarata.OpihiSolution)
            and isinstance(
                primary_solution.astrometrics, astrometry.AstrometricSolution
            )
        ):
            return None

        # Obtain the current values in the entry field.
        in_custom_x = self.ui.line_edit_astrometry_custom_pixel_x.text()
        in_custom_y = self.ui.line_edit_astrometry_custom_pixel_y.text()
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
            ) = primary_solution.astrometrics.pixel_to_sky_coordinates(
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
            ) = primary_solution.astrometrics.sky_to_pixel_coordinates(
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
        self.ui.line_edit_astrometry_custom_pixel_x.setText(out_custom_x)
        self.ui.line_edit_astrometry_custom_pixel_y.setText(out_custom_y)
        self.ui.line_edit_astrometry_custom_ra.setText(out_custom_ra)
        self.ui.line_edit_astrometry_custom_dec.setText(out_custom_dec)
        return None

    def __connect_push_button_solve_photometry(self) -> None:
        """The button to instruct on the solving of the photometric solution.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Determine the engine from user input via the drop down menu. The
        # recognizing text ought to be case insensitive, makes life easier.
        input_engine_name = self.ui.combo_box_photometry_engine.currentText()
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
            # Cycling through all of the indexes to try and solve the astrometry.
            # We need to use the index based method because for-loops do copying.
            for index in range(len(self.opihi_solution_list)):
                if not isinstance(
                    self.opihi_solution_list[index], opihiexarata.OpihiSolution
                ):
                    # There is nothing to solve.
                    continue
                try:
                    self.opihi_solution_list[index].solve_photometry(
                        solver_engine=engine,
                        overwrite=True,
                        raise_on_error=True,
                        vehicle_args=vehicle_args,
                    )
                except Exception as _e:
                    print("warn", _e)
                else:
                    # Photometry is special as the data may also be saved to the
                    # zero point database. We attempt to write a zero point record to
                    # the database, the wrapper writing function checks if writing to
                    # the database is a valid operation. We work on a copy of the
                    # solution just in case.
                    opihi_solution_copy = copy.deepcopy(self.opihi_solution_list[index])
                    # We thread it away just in case.
                    self.__write_zero_point_record_to_database(
                        opihi_solution=opihi_solution_copy
                    )
                    write_database_thread = threading.Thread(
                        target=self.__write_zero_point_record_to_database,
                        kwargs={"opihi_solution": opihi_solution_copy},
                    )
                    write_database_thread.start()
            # Finally updating all of the needed information.
            self.draw_opihi_image()
            self.refresh_dynamic_label_text()
            self.save_all_fits_files()
            # All done.
            return None

        # Starting the thread.
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
        # Determine the engine from user input via the drop down menu. The
        # recognizing text ought to be case insensitive, makes life easier.
        input_engine_name = self.ui.combo_box_orbit_engine.currentText()
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
            for index in range(len(self.opihi_solution_list)):
                if not isinstance(
                    self.opihi_solution_list[index], opihiexarata.OpihiSolution
                ):
                    # There is nothing to solve.
                    continue
                try:
                    # The histories provided in the classes are not as complete
                    # as they should be. We can add the supplemental
                    # information to the orbit solvers.
                    replacing_history = (
                        self.load_target_history_archive()
                        + self.get_target_history_current()
                    )
                    replacing_history = library.mpcrecord.clean_minor_planet_record(
                        records=replacing_history
                    )
                    # Replacing the history.
                    self.opihi_solution_list[index].asteroid_history = replacing_history

                    self.opihi_solution_list[index].solve_orbit(
                        solver_engine=engine,
                        overwrite=True,
                        raise_on_error=True,
                        vehicle_args=vehicle_args,
                    )
                except Exception as _e:
                    print("warn", _e)
            # Finally updating all of the needed information.
            self.draw_opihi_image()
            self.refresh_dynamic_label_text()
            self.save_all_fits_files()
            # All done.
            return None

        orbit_thread = threading.Thread(target=orbit_solving_function)
        orbit_thread.start()
        # All done.
        return None

    def __connect_push_button_solve_ephemeris(self) -> None:
        """A routine to use the current observation and historical observations
        to derive the orbit solution.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Determine the engine from user input via the drop down menu. The
        # recognizing text ought to be case insensitive, makes life easier.
        input_engine_name = self.ui.combo_box_ephemeris_engine.currentText()
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
            for index in range(len(self.opihi_solution_list)):
                if not isinstance(
                    self.opihi_solution_list[index], opihiexarata.OpihiSolution
                ):
                    # There is nothing to solve.
                    continue
                try:
                    self.opihi_solution_list[index].solve_ephemeris(
                        solver_engine=engine,
                        overwrite=True,
                        raise_on_error=True,
                        vehicle_args=vehicle_args,
                    )
                except Exception as _e:
                    print("warn", _e)
            # Finally updating all of the needed information.
            self.draw_opihi_image()
            self.refresh_dynamic_label_text()
            self.save_all_fits_files()
            # All done.
            return None

        ephemeris_thread = threading.Thread(target=ephemeris_solving_function)
        ephemeris_thread.start()
        # All done.
        return None

    def __connect_push_button_ephemeris_results_update_tcs_rates(self) -> None:
        """A routine to update the non-sidereal rates of the TCS as provided
        by the ephemeritic solution.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no ephemeris solution, there is nothing to be done.
        primary_solution = self.opihi_solution_list[self.primary_file_index]
        if not (
            isinstance(primary_solution, opihiexarata.OpihiSolution)
            and isinstance(primary_solution.ephemeritics, ephemeris.EphemeriticSolution)
        ):
            return None

        # We use the ephemeritic solution rates to update the TCS, the
        # function provided already converts the values as needed
        # so we can provide the units as per convention.
        # We do not care about the response for now.
        __ = library.tcs.t3io_tcs_ns_rate(
            ra_velocity=primary_solution.ephemeritics.ra_velocity,
            dec_velocity=primary_solution.ephemeritics.dec_velocity,
        )

        # All done.
        return None

    def __connect_push_button_ephemeris_forward_solve(self) -> None:
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
        primary_solution = self.opihi_solution_list[self.primary_file_index]
        if not (
            isinstance(primary_solution, opihiexarata.OpihiSolution)
            and isinstance(primary_solution.ephemeritics, ephemeris.EphemeriticSolution)
        ):
            return None

        # Get the time and date from the user input.
        datetime_input = self.ui.combo_box_ephemeris_forward_datetime.dateTime()
        # Getting the timezone, as the ephemeris requires UTC/JD time, a
        # conversion is needed. Qt uses IANA timezone IDs so we convert from
        # the human readable ones to it. We only deal with current timezones.
        timezone_input = self.ui.combo_box_ephemeris_forward_timezone.currentText()
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
        ra_deg, dec_deg = primary_solution.ephemeritics.forward_ephemeris(
            future_time=julian_day_input
        )
        ra_sex, dec_sex = library.conversion.degrees_to_sexagesimal_ra_dec(
            ra_deg=ra_deg, dec_deg=dec_deg, precision=2
        )
        # Updating the RA and DEC values.
        self.ui.label_dynamic_ephemeris_forward_ra.setText(ra_sex)
        self.ui.label_dynamic_ephemeris_forward_dec.setText(dec_sex)

        # All done.
        return None

    def __connect_push_button_solve_propagation(self) -> None:
        """A routine to use the current observation and historical observations
        to derive the propagation solution.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Determine the engine from user input via the drop down menu. The
        # recognizing text ought to be case insensitive, makes life easier.
        input_engine_name = self.ui.combo_box_propagate_engine.currentText()
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
            """The function to solve the orbit and refresh the plots."""
            for index in range(len(self.opihi_solution_list)):
                if not isinstance(
                    self.opihi_solution_list[index], opihiexarata.OpihiSolution
                ):
                    # There is nothing to solve.
                    continue
                try:
                    # The histories provided in the classes are not as complete
                    # as they should be. We can add the supplemental
                    # information to the orbit solvers.
                    replacing_history = (
                        self.load_target_history_archive()
                        + self.get_target_history_current()
                    )
                    replacing_history = library.mpcrecord.clean_minor_planet_record(
                        records=replacing_history
                    )
                    # Replacing the history.
                    self.opihi_solution_list[index].asteroid_history = replacing_history

                    self.opihi_solution_list[index].solve_propagate(
                        solver_engine=engine,
                        overwrite=True,
                        raise_on_error=True,
                        vehicle_args=vehicle_args,
                    )
                except Exception as _e:
                    print("warn", _e)
            # Finally updating all of the needed information.
            self.draw_opihi_image()
            self.refresh_dynamic_label_text()
            self.save_all_fits_files()
            # All done.
            return None

        propagate_thread = threading.Thread(target=propagate_solving_function)
        propagate_thread.start()
        # All done.
        return None

    def __connect_push_button_propagate_results_update_tcs_rates(self) -> None:
        """A routine to update the non-sidereal rates of the TCS as provided
        by the propagation solution.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no propagation solution, there is nothing to be done.
        primary_solution = self.opihi_solution_list[self.primary_file_index]
        if not (
            isinstance(primary_solution, opihiexarata.OpihiSolution)
            and isinstance(primary_solution.ephemeritics, propagate.PropagativeSolution)
        ):
            return None

        # We use the propagative solution rates to update the TCS, the
        # function provided already converts the values as needed
        # so we can provide the units as per convention.
        # We do not care about the response for now.
        __ = library.tcs.t3io_tcs_ns_rate(
            ra_velocity=primary_solution.propagatives.ra_velocity,
            dec_velocity=primary_solution.propagatives.dec_velocity,
        )

        # All done.
        return None

    def __connect_push_button_propagate_forward_solve(self) -> None:
        """Solving for the location of the target through propagation based
        on the time and date provided by the user.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no propagation solution, there is nothing to be done.
        primary_solution = self.opihi_solution_list[self.primary_file_index]
        if not (
            isinstance(primary_solution, opihiexarata.OpihiSolution)
            and isinstance(primary_solution.ephemeritics, propagate.PropagativeSolution)
        ):
            return None

        # Get the time and date from the user input.
        datetime_input = self.ui.combo_box_propagate_forward_datetime.dateTime()
        # Getting the timezone, as the ephemeris requires UTC/JD time, a
        # conversion is needed. Qt uses IANA timezone IDs so we convert from
        # the human readable ones to it. We only deal with current timezones.
        timezone_input = self.ui.combo_box_propagate_forward_timezone.currentText()
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
        ra_deg, dec_deg = primary_solution.propagatives.forward_propagate(
            future_time=julian_day_input
        )
        ra_sex, dec_sex = library.conversion.degrees_to_sexagesimal_ra_dec(
            ra_deg=ra_deg, dec_deg=dec_deg, precision=2
        )
        # Updating the RA and DEC values.
        self.ui.label_dynamic_propagate_forward_ra.setText(ra_sex)
        self.ui.label_dynamic_propagate_forward_dec.setText(dec_sex)

        # All done.
        return None

    def _get_target_selector_reference_filename(self, current_filename: int) -> str:
        """This function gets what the reference filename ought to be based
        on the current filename provided.

        This function prioritizes using the first image, then the last image
        as the reference images, cycling through until something is found.
        If none of said images exist, then None is returned.

        Parameters
        ----------
        current_filename : str
            The "current filename" of which is the filename which is used to
            determine the location of the target for the target selector.
            The reference filename cannot be the same file as this filename.

        Returns
        -------
        reference_filename : str
            The reference filename to send to the target selector.
        """
        # Using a hard copy, just in case.
        search_filename_list = copy.deepcopy(self.fits_filename_list)

        # We search through all of the files to find one which works properly.
        # We get the order here, this is hard coded on the order assumption and
        # having the origin item.
        ordered_search_filename_list = (
            search_filename_list[1:2] + search_filename_list[:1:-1]
        )
        reference_filename = None
        for filedex in ordered_search_filename_list:
            if current_filename == filedex:
                # The current file and the reference file should not be the
                # same file.
                continue
            if not isinstance(filedex, str):
                # The potential file is not even a path string, it cannot be
                # used as a reference file.
                continue
            if not os.path.isfile(filedex):
                # The path provided by the filename does not lead to a file,
                # so there is FITS file for it to refer to be used as a
                # reference file.
                continue
            # If it passed all of the above checks, then we found a valid
            # reference filename. We can stop.
            reference_filename = filedex
            break

        # All done
        return reference_filename

    def _get_target_set_name_guess(self) -> str:
        """This function attempts to guess the target name from multiple
        sources in the order of authority.

        The primary file index is preferred, then the order of the files in
        progressive order. The chain of priority (within each file) goes as:
        GUI input, OpihiExarata solution, FITS object, Filename.

        Parameters
        ----------
        None

        Returns
        -------
        guess_target_set_name : str
            The target set name that this function has found to be the best
            guess based on the hierarchy.
        """
        # Prioritize the primary file before the other files then go in order.
        file_order_index = [self.primary_file_index] + list(
            range(len(self.fits_filename_list))
        )

        # Going through all of the files by the order and then searching
        # for a good name based on the chain of priority.
        for index in file_order_index:
            # For the sake of order, even if we are cycling through all of the
            # indexes and this would not change with index changes. We pull
            # from the GUI's interface.
            guess_target_set_name = self.ui.line_edit_detected_target_name.text()
            if (
                isinstance(guess_target_set_name, str)
                and len(guess_target_set_name) != 0
            ):
                # The GUI has a valid target name, we use it.
                return guess_target_set_name

            # Next we try the solutions.
            solution = self.opihi_solution_list[index]
            if not isinstance(solution, opihiexarata.OpihiSolution):
                # There is no solution to derive it from.
                pass 
            else:
                # See if it is a valid name.
                guess_target_set_name = solution.asteroid_name
                if isinstance(guess_target_set_name, str) and len(guess_target_set_name) != 0:
                    return guess_target_set_name

            # Next, we try to find the target name based on the FITS file
            # header.
            filename = self.fits_filename_list[index]
            # Try and load the FITS file and extract the target name.
            try:
                header, __ = library.fits.read_fits_image_file(filename=filename)
                guess_target_set_name = header.get("OBJECT", None)
            except Exception:
                # The FITS file could not be properly read, so a guess cannot
                # be determined.
                pass
            else:
                # Check if the guess target set name guess is completely
                # valid.
                if (
                    isinstance(guess_target_set_name, str)
                    and len(guess_target_set_name) != 0
                ):
                    # The GUI has a valid target name, we use it.
                    return guess_target_set_name

            # Next, we try and extract it from the filename based on the
            # hardcoded assumptions of the filenames.
            # The filename is an absolute path usually, we only need the name
            # of the file itself.
            try:
                basename = library.path.get_filename_with_extension(pathname=filename)
            except Exception:
                # Extracting the basename cannot be done.
                pass
            else:
                # The filename conventions of the Opihi telescope have dots as
                # subject delimiters. The extension should not be a part of
                # this.
                basename_parts = basename.split(".")
                guess_target_set_name = basename_parts[3]
                # Check the guess.
                if (
                    isinstance(guess_target_set_name, str)
                    and len(guess_target_set_name) != 0
                ):
                    # The GUI has a valid target name, we use it.
                    return guess_target_set_name

        # If the code has reached here, it means that no guess target name
        # could be derived. We just use a weird default.
        guess_target_set_name = library.config.GUI_MANUAL_DEFAULT_TARGET_SET_NAME
        return guess_target_set_name

    def _get_mpcrecord_archive_filename(self) -> str:
        """This is a function which gets the MPC record archive filename
        from naming conventions and the current fits file name.

        Parameters
        ----------
        None

        Returns
        -------
        mpc_record_filename : str
            The filename of the MPC record for this object/image.
        """
        if self.target_set_name is None:
            raise error.SequentialOrderError(
                    "There is no target/asteroid name to get the MPC record filename"
                    " from. Moreover, deriving it from the provided file(s) failed."
                )
        else:
            if isinstance(self.target_set_name, str):
                # All is well and good.
                pass
            else:
                raise error.InputError(
                    "The target set name provided is not a valid string."
                )

        suffix = str(library.config.GUI_MANUAL_DEFAULT_MPC_RECORD_SAVING_SUFFIX)
        mpc_record_filename = self.target_set_name + suffix
        # Search the same directory as the primary fits file for this
        # information as that is currently the expected location.
        # Preferring the preprocessed filename if it exists, have a fall back.
        primary_fits_file = self._get_primary_fits_filename()
        fits_directory = None
        if isinstance(primary_fits_file, str) and os.path.isfile(primary_fits_file):
            fits_directory = library.path.get_directory(pathname=primary_fits_file)
        else:
            # We just cycle through the filenames in order to figure out what 
            # we can use.
            for filedex in self.fits_filename_list:
                if isinstance(filedex, str):
                    fits_directory = library.path.get_directory(
                pathname=filedex
            )
            # If no FITS directory has been determined by this point, then 
            # we cannot really derive the MPC record filename without the 
            # directory component.
            if fits_directory is None:
                raise error.DirectoryError("No FITS filename provided can provide a directory for which to derive the MPC record filename.")
            elif isinstance(fits_directory, str) and os.path.isdir(fits_directory):
                # All good, one has been determined.
                pass
            else:
                # The code should never reach here.
                raise error.LogicFlowError("The FITS directory variable should have been covered by other cases by this point.")

        mpc_record_filename = library.path.merge_pathname(
            directory=fits_directory, filename=mpc_record_filename, extension="txt"
        )
        return mpc_record_filename

    def _get_primary_fits_filename(self) -> str:
        """This function gets the FITS filename of the primary file as
        determined by the GUI radio buttons.

        Parameters
        ----------
        None

        Returns
        -------
        primary_fits_filename : str
            The primary fits filename. If the selected primary FITS file
            does not exist, this is None.
        """
        # Extracting it straight from the list.
        primary_fits_filename = self.fits_filename_list[self.primary_file_index]

        # If the raws are also not a valid filename, then there is None
        # chosen.
        if not isinstance(primary_fits_filename, str):
            primary_fits_filename = None
        elif os.path.isfile(primary_fits_filename):
            primary_fits_filename = None
        else:
            # It is all good.
            primary_fits_filename = primary_fits_filename

        # All done.
        return primary_fits_filename

    def get_target_history_current(self) -> list[str]:
        """This function gets the current entries for the target history from
        the OpihiSolutions and the current data loaded into the GUI.

        Parameters
        ----------
        None

        Returns
        -------
        target_history_current : list
            The current history, based off of the results from the solutions
            provided.
        """
        # We add the current history derived from our data to the data of the
        # MPC record.
        target_history_current = []
        for solutiondex in self.opihi_solution_list:
            if not isinstance(solutiondex, opihiexarata.OpihiSolution):
                # There is no solution to get the record from.
                continue
            # Try and extract the MPC record row.
            try:
                record_row = solutiondex.mpc_record_row()
            except error.PracticalityError:
                # It is likely that there is no astrometric solution with this 
                # observation so a record row really cannot be meaningfully 
                # defined.
                continue
            else:
                target_history_current.append(record_row)
        
        # Cleaning up the history.
        target_history_current = library.mpcrecord.clean_minor_planet_record(
            records=target_history_current
        )
        return target_history_current

    def load_fits_file(self, fits_filename: str) -> hint.OpihiSolution:
        """This loads a FITS file and returns an OpihiSolution class.

        Parameters
        ----------
        fits_filename : str
            The fits filename which will be loaded.

        Returns
        -------
        opihi_solution : OpihiSolution
            The solution wrapper class for the provided FITS filename.
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

        # The name of the asteroid determined either by the file or the
        # summary.
        if isinstance(self.target_set_name, str):
            asteroid_name = self.target_set_name
        else:
            # Derive it from the file(s).
            asteroid_name = self._get_target_set_name_guess()

        # We bring in the target selector to determine the location of the
        # asteroid.
        reference_fits_file = self._get_target_selector_reference_filename(
            current_filename=fits_filename
        )
        asteroid_location = gui.selector.ask_user_target_selector_window(
            current_fits_filename=fits_filename,
            reference_fits_filename=reference_fits_file,
        )

        asteroid_history = self.load_target_history_archive()

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
        return opihi_solution

    def load_target_history_archive(self, archive_filename: str = None) -> list[str]:
        """This loads the target/asteroid history archive file and allows it
        to be used by the solution classes of all of the other solutions.

        Parameters
        ----------
        archive_filename : str, default = None
            The filename of the archive to load. If it is None, the default
            one is derived from the target name.

        Returns
        -------
        target_history : list
            The target history in a 80-column MPC format.
        """
        # Determining the archive filename.
        if archive_filename is not None:
            archive_filename = archive_filename
        else:
            archive_filename = self._get_mpcrecord_archive_filename()

        # If the file does not exist, there is nothing to load so a blank
        # history is returned.
        if not os.path.isfile(archive_filename):
            print("warn")
            target_history = []
        else:
            # Read the historical data.
            with open(archive_filename, "r") as mpcfile:
                raw_lines = mpcfile.readlines()
                # The files have new line characters on them, they need
                # to be removed to have the normal 80 characters.
                target_history = [linedex.removesuffix("\n") for linedex in raw_lines]
        # All done.
        return target_history

    def save_target_history_archive(self, archive_filename: str = None) -> None:
        """This saves the target history archive into a file which contains
        all of the history of the asteroid/target observations, both past and
        the present ones solved for.

        Parameters
        ----------
        archive_filename : str, default = None
            The filename of the archive to load. If it is None, the default
            one is derived from the target name.

        Returns
        -------
        None
        """
        # Determining the archive filename.
        if archive_filename is not None:
            archive_filename = archive_filename
        else:
            try:
                archive_filename = self._get_mpcrecord_archive_filename()
            except Exception:
                print("warn")
                archive_filename = None
        # An archive filename cannot be determined, we cannot save the 
        # observational history. There is no point in continuing.
        if not isinstance(archive_filename, str):
            print("warn")
            return None

        # Loading the old history.
        archive_history = self.load_target_history_archive(
            archive_filename=archive_filename
        )

        # Combining the current history with those from archive.
        current_history = self.get_target_history_current()
        total_history = archive_history + current_history

        # The MPC record history ought to be cleaned and sorted. As there are
        # many sources from which the information is coming from, and there
        # may be duplicates.
        clean_total_history = library.mpcrecord.clean_minor_planet_record(
            records=total_history
        )

        # Saving the history to the file.
        # Adding the new line character as write lines do not do this
        # to make the multi-rowed file.
        mpc_record = [rowdex + "\n" for rowdex in clean_total_history]
        # If the record file already exists, replace our information with
        # it. We can do this because the archive history already contains this
        # information.
        with open(archive_filename, "w") as mpcfile:
            mpcfile.writelines(mpc_record)

        # All done.
        return None

    def save_all_fits_files(self) -> None:
        """This function saves all of the FITS files into their respective
        default locations and configurations.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Saving all of the FITS files.
        for index in range(len(self.opihi_solution_list)):
            self.save_index_fits_file(index=index)
        # All done.
        return None

    def save_index_fits_file(self, index) -> None:
        """This function executes the saving of the FITS file based on the
        provided index.

        Parameters
        ----------
        index : int
            The file index of the OpihiSolution to be saved to a FITS file.

        Returns
        -------
        None
        """
        # The filenames and solutions.
        try:
            filename = self.fits_filename_list[index]
            solution = self.opihi_solution_list[index]
        except IndexError:
            raise error.InputError(
                "The file index provided is outside of the range of possible file"
                " indexes which this GUI can allow."
            )

        if not isinstance(filename, str):
            # The FITS file path is not even a string path, the location of the
            # file cannot be determined.
            return None
        if not os.path.exists(filename):
            # The FITS file does not exist. There is nothing to save.
            return None
        if not isinstance(solution, opihiexarata.OpihiSolution):
            # The solution is not actually an OpihiExarata solution, a
            # FITS file cannot be created to save.
            return None

        # We determine the saving filename based on the suffix conventions.
        # Constructing the filename using the suffix methodology.
        file_dir, file_base, file_ext = library.path.split_pathname(pathname=filename)
        OX_SUFFIX = library.config.GUI_MANUAL_DEFAULT_FITS_SAVING_SUFFIX
        saving_filename = library.path.merge_pathname(
            directory=file_dir,
            filename=file_base + OX_SUFFIX,
            extension=file_ext,
        )

        # Saving the FITS file.
        solution.save_to_fits_file(filename=saving_filename, overwrite=True)

        # All done.
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
        # Extracting all of the values from the text. These are all strings.
        smax_val = self.ui.line_edit_orbit_results_semimajor_axis_value.text().strip()
        ecci_val = self.ui.line_edit_orbit_results_eccentricity_value.text().strip()
        incl_val = self.ui.line_edit_orbit_results_inclination_value.text().strip()
        asnd_val = self.ui.line_edit_orbit_results_ascending_node_value.text().strip()
        prhe_val = self.ui.line_edit_orbit_results_perihelion_value.text().strip()
        mnan_val = self.ui.line_edit_orbit_results_mean_anomaly_value.text().strip()
        epch_val = self.ui.line_edit_orbit_results_epoch_value.text().strip()
        # And the errors.
        smax_err = self.ui.line_edit_orbit_results_semimajor_axis_error.text().strip()
        ecci_err = self.ui.line_edit_orbit_results_eccentricity_error.text().strip()
        incl_err = self.ui.line_edit_orbit_results_inclination_error.text().strip()
        asnd_err = self.ui.line_edit_orbit_results_ascending_node_error.text().strip()
        prhe_err = self.ui.line_edit_orbit_results_perihelion_error.text().strip()
        mnan_err = self.ui.line_edit_orbit_results_mean_anomaly_error.text().strip()

        # Making them numbers, values which actual math can be done on them.
        smax_val = float(smax_val)
        ecci_val = float(ecci_val)
        incl_val = float(incl_val)
        asnd_val = float(asnd_val)
        prhe_val = float(prhe_val)
        mnan_val = float(mnan_val)
        epch_val = float(epch_val)
        smax_err = float(smax_err)
        ecci_err = float(ecci_err)
        incl_err = float(incl_err)
        asnd_err = float(asnd_err)
        prhe_err = float(prhe_err)
        mnan_err = float(mnan_err)

        # The orbital element dictionary which would be used for a custom
        # orbit.
        orbital_elements = {
            "semimajor_axis": smax_val,
            "semimajor_axis_error": smax_err,
            "eccentricity": ecci_val,
            "eccentricity_error": ecci_err,
            "inclination": incl_val,
            "inclination_error": incl_err,
            "longitude_ascending_node": asnd_val,
            "longitude_ascending_node_error": asnd_err,
            "argument_perihelion": prhe_val,
            "argument_perihelion_error": prhe_err,
            "mean_anomaly": mnan_val,
            "mean_anomaly_error": mnan_err,
            "epoch_julian_day": epch_val,
        }
        # All done.
        return orbital_elements

    def reset_all(self) -> None:
        """This function completely resets the GUI into its initial state.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        # Clearing all of the dynamic text.
        self.reset_dynamic_label_text(complete=True)

        # Clearing the plot.
        self.draw_nothing()

        # Removing all relevant scientific data, bringing it back to its
        # defaults.
        # Removing the filenames as the system has been reset.
        self.fits_filename_list = [error.IntentionalError, None, None, None, None]
        # Removing the solutions as well.
        self.opihi_solution_list = [error.IntentionalError, None, None, None, None]

        # All done.
        return None

    def reset_dynamic_label_text(self, complete: bool = False) -> None:
        """Reset all of the dynamic label text and other related fields,
        this is traditionally done just before a new image is going to be
        introduced.

        This resets the text back to their defaults as per the GUI builder.

        The selections on the engines do not need to be reset as they are
        just a selection criteria and do not actually provide any information.

        Parameters
        ----------
        complete : bool, default = False
            Some entries are not cleared because this function is intended for
            refreshing the GUI for a new image, but, sometimes a more complete
            reset of the text is needed.

        Returns
        -------
        None
        """

        ## Resetting File Selector information.
        #####

        # The target name and the directory the images are in should
        # not reset just because of a new image.
        self.ui.label_dynamic_filename_1.setText(
            "opi.20XXA999.YYMMDD.AAAAAAAAAA.#####.a.fits"
        )
        self.ui.label_dynamic_filename_2.setText(
            "opi.20XXA999.YYMMDD.AAAAAAAAAA.#####.a.fits"
        )
        self.ui.label_dynamic_filename_3.setText(
            "opi.20XXA999.YYMMDD.AAAAAAAAAA.#####.a.fits"
        )
        self.ui.label_dynamic_filename_4.setText(
            "opi.20XXA999.YYMMDD.AAAAAAAAAA.#####.a.fits"
        )
        # The asteroid location information.
        self.ui.label_dynamic_target_1_pixel_location.setText("(XXXX, YYYY)")
        self.ui.label_dynamic_target_2_pixel_location.setText("(XXXX, YYYY)")
        self.ui.label_dynamic_target_3_pixel_location.setText("(XXXX, YYYY)")
        self.ui.label_dynamic_target_4_pixel_location.setText("(XXXX, YYYY)")

        ## Resetting Summary information.
        #####
        # A full reset is best for changing the asteroid or target name.
        if complete:
            self.ui.line_edit_detected_target_name.setText("")

        ## Resetting Astrometry information.
        #####
        self.ui.label_dynamic_astrometry_file_1_center_ra.setText("HH:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_1_center_dec.setText("+DD:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_2_center_ra.setText("HH:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_2_center_dec.setText("+DD:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_3_center_ra.setText("HH:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_3_center_dec.setText("+DD:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_4_center_ra.setText("HH:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_4_center_dec.setText("+DD:MM:SS.SS")

        self.ui.label_dynamic_astrometry_file_1_target_ra.setText("HH:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_1_target_dec.setText("+DD:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_2_target_ra.setText("HH:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_2_target_dec.setText("+DD:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_3_target_ra.setText("HH:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_3_target_dec.setText("+DD:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_4_target_ra.setText("HH:MM:SS.SS")
        self.ui.label_dynamic_astrometry_file_4_target_dec.setText("+DD:MM:SS.SS")

        ## Resetting Photometric information.
        #####
        self.ui.label_static_photometry_results_file_1_filter_name.setText("FF")
        self.ui.label_static_photometry_results_file_1_zero_point.setText(
            "ZZ.ZZZ + E.EEE"
        )
        self.ui.label_static_photometry_results_file_1_magnitude.setText(
            "MM.MMM + E.EEE"
        )

        self.ui.label_static_photometry_results_file_2_filter_name.setText("FF")
        self.ui.label_static_photometry_results_file_2_zero_point.setText(
            "ZZ.ZZZ + E.EEE"
        )
        self.ui.label_static_photometry_results_file_2_magnitude.setText(
            "MM.MMM + E.EEE"
        )

        self.ui.label_static_photometry_results_file_3_filter_name.setText("FF")
        self.ui.label_static_photometry_results_file_3_zero_point.setText(
            "ZZ.ZZZ + E.EEE"
        )
        self.ui.label_static_photometry_results_file_3_magnitude.setText(
            "MM.MMM + E.EEE"
        )

        self.ui.label_static_photometry_results_file_4_filter_name.setText("FF")
        self.ui.label_static_photometry_results_file_4_zero_point.setText(
            "ZZ.ZZZ + E.EEE"
        )
        self.ui.label_static_photometry_results_file_4_magnitude.setText(
            "MM.MMM + E.EEE"
        )

        ## Resetting Orbit information.
        #####
        # We only reset the orbit if the user wanted a complete reset.
        if complete:

            self.ui.line_edit_orbit_results_semimajor_axis_value.setText("VV.VVV")
            self.ui.line_edit_orbit_results_semimajor_axis_error.setText("EE.EEE")
            self.ui.line_edit_orbit_results_eccentricity_value.setText("VV.VVV")
            self.ui.line_edit_orbit_results_eccentricity_error.setText("EE.EEE")
            self.ui.line_edit_orbit_results_inclination_value.setText("VV.VVV")
            self.ui.line_edit_orbit_results_inclination_error.setText("EE.EEE")
            self.ui.line_edit_orbit_results_ascending_node_value.setText("VV.VVV")
            self.ui.line_edit_orbit_results_ascending_node_error.setText("EE.EEE")
            self.ui.line_edit_orbit_results_perihelion_value.setText("VV.VVV")
            self.ui.line_edit_orbit_results_perihelion_error.setText("EE.EEE")
            self.ui.line_edit_orbit_results_mean_anomaly_value.setText("VV.VVV")
            self.ui.line_edit_orbit_results_mean_anomaly_error.setText("EE.EEE")
            self.ui.line_edit_orbit_results_epoch_value.setText("EEEEEEE.EEEEE")

        ## Resetting Ephemeris information.
        #####
        self.ui.label_dynamic_ephemeris_results_first_order_ra_rate.setText("+VV.VVV")
        self.ui.label_dynamic_ephemeris_results_first_order_ra_error.setText("+EE.EEEE")
        self.ui.label_dynamic_ephemeris_results_first_order_dec_rate.setText("+VV.VVV")
        self.ui.label_dynamic_ephemeris_results_first_order_dec_error.setText(
            "+EE.EEEE"
        )

        self.ui.label_dynamic_ephemeris_results_second_order_ra_rate.setText("+AA.AAA")
        self.ui.label_dynamic_ephemeris_results_second_order_ra_error.setText(
            "+EE.EEEE"
        )
        self.ui.label_dynamic_ephemeris_results_second_order_dec_rate.setText("+AA.AAA")
        self.ui.label_dynamic_ephemeris_results_second_order_dec_error.setText(
            "+EE.EEEE"
        )
        # Keeping the timezone and time information for convenience, unless
        # a complete clear is needed.
        if complete:
            default_epoch = QtCore.QDateTime(1900, 1, 1, 0, 0, 0)
            self.ui.combo_box_ephemeris_forward_datetime.setDateTime(default_epoch)
            self.ui.combo_box_ephemeris_forward_timezone.setCurrentIndex(0)
        self.ui.label_dynamic_ephemeris_forward_ra.setText("HH:MM:SS.SS")
        self.ui.label_dynamic_ephemeris_forward_dec.setText("+DD:MM:SS.SS")

        ## Resetting Propagate information.
        #####
        self.ui.label_dynamic_propagate_results_first_order_ra_rate.setText("+VV.VVV")
        self.ui.label_dynamic_propagate_results_first_order_ra_error.setText("+EE.EEEE")
        self.ui.label_dynamic_propagate_results_first_order_dec_rate.setText("+VV.VVV")
        self.ui.label_dynamic_propagate_results_first_order_dec_error.setText(
            "+EE.EEEE"
        )

        self.ui.label_dynamic_propagate_results_second_order_ra_rate.setText("+AA.AAA")
        self.ui.label_dynamic_propagate_results_second_order_ra_error.setText(
            "+EE.EEEE"
        )
        self.ui.label_dynamic_propagate_results_second_order_dec_rate.setText("+AA.AAA")
        self.ui.label_dynamic_propagate_results_second_order_dec_error.setText(
            "+EE.EEEE"
        )
        # Keeping the timezone and time information for convenience, unless
        # a complete clear is needed.
        if complete:
            default_epoch = QtCore.QDateTime(1900, 1, 1, 0, 0, 0)
            self.ui.combo_box_propagate_forward_datetime.setDateTime(default_epoch)
            self.ui.combo_box_propagate_forward_timezone.setCurrentIndex(0)
        self.ui.label_dynamic_propagate_forward_ra.setText("HH:MM:SS.SS")
        self.ui.label_dynamic_propagate_forward_dec.setText("+DD:MM:SS.SS")

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
        self.__refresh_dynamic_label_text_file_selector()
        self.__refresh_dynamic_label_text_astrometry()
        self.__refresh_dynamic_label_text_photometry()
        self.__refresh_dynamic_label_text_orbit()
        self.__refresh_dynamic_label_text_ephemeris()
        self.__refresh_dynamic_label_text_propagate()

        # All done.
        return None

    def __refresh_dynamic_label_text_file_selector(self) -> None:
        """Refresh all of the dynamic label text for the file selector.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # The filenames, in order. We do not need the directory path in this
        # area.
        def _basename_only(pathname: str) -> str:
            """This function makes sure that only the basename is returned. The
            path provided is not a valid string, then a blank string is
            returned."""
            if isinstance(pathname, str):
                return library.path.get_filename_with_extension(pathname=pathname)
            else:
                return "opi.20XXA999.YYMMDD.AAAAAAAAAA.#####.a.fits"

        self.ui.label_dynamic_filename_1.setText(
            _basename_only(pathname=self.fits_filename_list[1])
        )
        self.ui.label_dynamic_filename_2.setText(
            _basename_only(pathname=self.fits_filename_list[2])
        )
        self.ui.label_dynamic_filename_3.setText(
            _basename_only(pathname=self.fits_filename_list[3])
        )
        self.ui.label_dynamic_filename_4.setText(
            _basename_only(pathname=self.fits_filename_list[4])
        )

        # The target locations, if they exist. We do not need mutability for
        # this so going by indexes themselves are inconvenient.
        target_location_strings = {}
        for index, solutiondex in enumerate(self.opihi_solution_list):
            # Check that the solution itself actually is a valid solution class.
            if not isinstance(solutiondex, opihiexarata.OpihiSolution):
                # Using the GUI defaults.
                target_location_strings[index] = "(XXXX, YYYY)"
            else:
                # Parse the asteroid location into a string.
                if solutiondex.asteroid_location is None:
                    target_location_strings[index] = "(NaN, NaN)"
                else:
                    target_location_strings[index] = "({x}, {y})".format(
                        x=solutiondex.asteroid_location[0],
                        y=solutiondex.asteroid_location[1],
                    )
        # Displaying the information.
        self.ui.label_dynamic_target_1_pixel_location.setText(
            target_location_strings[1]
        )
        self.ui.label_dynamic_target_2_pixel_location.setText(
            target_location_strings[2]
        )
        self.ui.label_dynamic_target_3_pixel_location.setText(
            target_location_strings[3]
        )
        self.ui.label_dynamic_target_4_pixel_location.setText(
            target_location_strings[4]
        )

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
        if self.target_set_name is not None:
            self.ui.line_edit_detected_target_name.setText(str(self.target_set_name))

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
        # We cycle through all of the possible solutions to derive the
        # needed information.
        cen_ra_str = {}
        cen_dec_str = {}
        trg_ra_str = {}
        trg_dec_str = {}

        # Finding and solving for the astrometry. We do not need mutability for
        # this so going by indexes themselves are inconvenient.
        for index, solutiondex in enumerate(self.opihi_solution_list):
            # Check that the solution itself actually is a valid solution class.
            if not isinstance(solutiondex, opihiexarata.OpihiSolution):
                # It is not, using the default values.
                cen_ra_str[index] = "HH:MM:SS.SS"
                cen_dec_str[index] = "+DD:MM:SS.SS"
                trg_ra_str[index] = "HH:MM:SS.SS"
                trg_dec_str[index] = "+DD:MM:SS.SS"
            # Check that the solution itself actually is a valid solution class.
            elif not (isinstance(solutiondex.astrometrics, astrometry.AstrometricSolution) and solutiondex.astrometrics_status):
                # It is not, using values to indicate that some solving went 
                # wrong.
                cen_ra_str[index] = "NaN"
                cen_dec_str[index] = "NaN"
                trg_ra_str[index] = "NaN"
                trg_dec_str[index] = "NaN"
            else:
                # Find the center pixel location of the image and solve for the
                # RA and DEC of it.
                cen_x, cen_y = [side / 2 for side in solutiondex.data.shape]
                cen_ra, cen_dec = solutiondex.astrometrics.pixel_to_sky_coordinates(
                    x=cen_x, y=cen_y
                )
                (
                    cen_ra_sex,
                    cen_dec_sex,
                ) = library.conversion.degrees_to_sexagesimal_ra_dec(
                    ra_deg=cen_ra, dec_deg=cen_dec, precision=2
                )
                # Saving.
                cen_ra_str[index] = cen_ra_sex
                cen_dec_str[index] = cen_dec_sex

                # Find the asteroid's location, if it exists.
                if solutiondex.asteroid_location is None:
                    # There is no asteroid location to find the coordinates
                    # for.
                    trg_ra_str[index] = "NaN"
                    trg_dec_str[index] = "NaN"
                else:
                    # Get the location and solve it.
                    trg_x, trg_y = solutiondex.asteroid_location
                    trg_ra, trg_dec = solutiondex.astrometrics.pixel_to_sky_coordinates(
                        x=trg_x, y=trg_y
                    )
                    (
                        trg_ra_sex,
                        trg_dec_sex,
                    ) = library.conversion.degrees_to_sexagesimal_ra_dec(
                        ra_deg=trg_ra, dec_deg=trg_dec, precision=2
                    )
                    # Recording it.
                    trg_ra_str[index] = trg_ra_sex
                    trg_dec_str[index] = trg_dec_sex

        # Recording it from the dictionaries.
        self.ui.label_dynamic_astrometry_file_1_center_ra.setText(cen_ra_str[1])
        self.ui.label_dynamic_astrometry_file_1_center_dec.setText(cen_dec_str[1])
        self.ui.label_dynamic_astrometry_file_2_center_ra.setText(cen_ra_str[2])
        self.ui.label_dynamic_astrometry_file_2_center_dec.setText(cen_dec_str[2])
        self.ui.label_dynamic_astrometry_file_3_center_ra.setText(cen_ra_str[3])
        self.ui.label_dynamic_astrometry_file_3_center_dec.setText(cen_dec_str[3])
        self.ui.label_dynamic_astrometry_file_4_center_ra.setText(cen_ra_str[4])
        self.ui.label_dynamic_astrometry_file_4_center_dec.setText(cen_dec_str[4])

        self.ui.label_dynamic_astrometry_file_1_target_ra.setText(trg_ra_str[1])
        self.ui.label_dynamic_astrometry_file_1_target_dec.setText(trg_dec_str[1])
        self.ui.label_dynamic_astrometry_file_2_target_ra.setText(trg_ra_str[2])
        self.ui.label_dynamic_astrometry_file_2_target_dec.setText(trg_dec_str[2])
        self.ui.label_dynamic_astrometry_file_3_target_ra.setText(trg_ra_str[3])
        self.ui.label_dynamic_astrometry_file_3_target_dec.setText(trg_dec_str[3])
        self.ui.label_dynamic_astrometry_file_4_target_ra.setText(trg_ra_str[4])
        self.ui.label_dynamic_astrometry_file_4_target_dec.setText(trg_dec_str[4])

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
        # We cycle through all of the possible solutions to derive the
        # needed information.
        flt_name = {}
        zp_str = {}
        mag_str = {}

        # The plus minus symbol for errors.
        pm_sym = "\u00B1"

        # Finding and solving for the photometry. We do not need mutability for
        # this so going by indexes themselves are inconvenient.
        for index, solutiondex in enumerate(self.opihi_solution_list):
            # Check that the solution itself actually is a valid solution class.
            if not isinstance(solutiondex, opihiexarata.OpihiSolution):
                # There is nothing to derive, we print the GUI defaults as 
                # there is nothing to do.
                flt_name[index] = "FF"
                zp_str[index] = "ZZ.ZZZ {pm} E.EEE".format(pm=pm_sym)
                mag_str[index] = "MM.MMM {pm} E.EEE".format(pm=pm_sym)
                continue
            
            # The filter names actually do not really require a photometric 
            # solution.
            flt_name[index] = solutiondex.filter_name

            # Checking if a valid photometry solution exists.
            if not (isinstance(solutiondex.photometrics, photometry.PhotometricSolution) and solutiondex.photometrics_status):
                # It is not, using the same dummy values.
                zp_str[index] = "NaN {pm} NaN".format(pm=pm_sym)
                mag_str[index] = "NaN {pm} NaN".format(pm=pm_sym)
            else:
                # Extracting the photometry information.
                flt_name[index] = solutiondex.photometrics.filter_name
                # Extracting the zero point information.
                zp = round(solutiondex.photometrics.zero_point, 3)
                zpe = round(solutiondex.photometrics.zero_point_error, 4)
                zp_str[index] = "{v} {pm} {e}".format(v=zp, pm=pm_sym, e=zpe)
                # Extracting the target's magnitude, if possible.
                if solutiondex.asteroid_location is not None:
                    magnitude, magnitude_error = solutiondex.compute_asteroid_magnitude(
                        asteroid_location=solutiondex.asteroid_location, overwrite=False
                    )
                    mag = round(magnitude, 4)
                    mage = round(magnitude_error, 4)
                    mag_str[index] = "{v} {pm} {e}".format(v=mag, pm=pm_sym, e=mage)
                else:
                    mag_str[index] = "NaN {pm} NaN".format(pm=pm_sym)

        # Applying the values.
        self.ui.label_static_photometry_results_file_1_filter_name.setText(flt_name[1])
        self.ui.label_static_photometry_results_file_2_filter_name.setText(flt_name[2])
        self.ui.label_static_photometry_results_file_3_filter_name.setText(flt_name[3])
        self.ui.label_static_photometry_results_file_4_filter_name.setText(flt_name[4])
        self.ui.label_static_photometry_results_file_1_zero_point.setText(zp_str[1])
        self.ui.label_static_photometry_results_file_2_zero_point.setText(zp_str[2])
        self.ui.label_static_photometry_results_file_3_zero_point.setText(zp_str[3])
        self.ui.label_static_photometry_results_file_4_zero_point.setText(zp_str[4])
        self.ui.label_static_photometry_results_file_1_magnitude.setText(mag_str[1])
        self.ui.label_static_photometry_results_file_2_magnitude.setText(mag_str[2])
        self.ui.label_static_photometry_results_file_3_magnitude.setText(mag_str[3])
        self.ui.label_static_photometry_results_file_4_magnitude.setText(mag_str[4])

        # All done.
        return None

    def __refresh_dynamic_label_text_orbit(self) -> None:
        """Refresh all of the dynamic label text for orbit.
        This fills out the information based on the current primary solution
        available and solved.

        An orbital solution must exist.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no orbit solution, there is nothing to be done.
        primary_solution = self.opihi_solution_list[self.primary_file_index]
        if not (
            isinstance(primary_solution, opihiexarata.OpihiSolution)
            and isinstance(primary_solution.orbitals, orbit.OrbitalSolution)
        ):
            return None

        # Refreshing the values of the Keplerian orbital elements.
        # The orbital elements' values and errors should be reported. We define
        # the string formatting here.
        def vsf(val: float) -> str:
            """Unified string formatting for orbital element values and errors."""
            # Rounding values to sensible values.
            return "{input:.5f}".format(input=val)

        # Using the above function to derive the display strings for all of the
        # elements.
        self.ui.line_edit_orbit_results_semimajor_axis_value.setText(
            vsf(primary_solution.orbitals.semimajor_axis)
        )
        self.ui.line_edit_orbit_results_semimajor_axis_error.setText(
            vsf(primary_solution.orbitals.semimajor_axis_error)
        )

        self.ui.line_edit_orbit_results_eccentricity_value.setText(
            vsf(primary_solution.orbitals.eccentricity)
        )
        self.ui.line_edit_orbit_results_eccentricity_error.setText(
            vsf(primary_solution.orbitals.eccentricity_error)
        )

        self.ui.line_edit_orbit_results_inclination_value.setText(
            vsf(primary_solution.orbitals.inclination)
        )
        self.ui.line_edit_orbit_results_inclination_error.setText(
            vsf(primary_solution.orbitals.inclination_error)
        )

        self.ui.line_edit_orbit_results_ascending_node_value.setText(
            vsf(primary_solution.orbitals.longitude_ascending_node)
        )
        self.ui.line_edit_orbit_results_ascending_node_error.setText(
            vsf(primary_solution.orbitals.longitude_ascending_node_error)
        )

        self.ui.line_edit_orbit_results_perihelion_value.setText(
            vsf(primary_solution.orbitals.argument_perihelion)
        )
        self.ui.line_edit_orbit_results_perihelion_error.setText(
            vsf(primary_solution.orbitals.argument_perihelion_error)
        )

        self.ui.line_edit_orbit_results_mean_anomaly_value.setText(
            vsf(primary_solution.orbitals.mean_anomaly)
        )
        self.ui.line_edit_orbit_results_mean_anomaly_error.setText(
            vsf(primary_solution.orbitals.mean_anomaly_error)
        )

        # Maximum precision on the epoch Julian day is desired however.
        julian_day_string = str(primary_solution.orbitals.epoch_julian_day)
        self.ui.line_edit_orbit_results_epoch_value.setText(julian_day_string)

        # All done.
        return None

    def __refresh_dynamic_label_text_ephemeris(self) -> None:
        """Refresh all of the dynamic label text for ephemerides.
        This fills out the information based on the current primary solution
        available and solved.

        An ephemeritic solution must exist.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # If there is no ephemeris solution, there is nothing to be done.
        primary_solution = self.opihi_solution_list[self.primary_file_index]
        if not (
            isinstance(primary_solution, opihiexarata.OpihiSolution)
            and isinstance(primary_solution.ephemeritics, ephemeris.EphemeriticSolution)
        ):
            return None

        # Update the rate text with the velocity terms provided by the
        # propagation solution. The propagation solution provides rates as
        # degrees per second.
        ra_v_deg = primary_solution.ephemeritics.ra_velocity
        dec_v_deg = primary_solution.ephemeritics.dec_velocity
        # And acceleration, as degrees per second squared.
        ra_a_deg = primary_solution.ephemeritics.ra_acceleration
        dec_a_deg = primary_solution.ephemeritics.dec_acceleration
        # Converting to the more familiar arcsec/s from deg/s along with
        # arcsec/s/s from deg/s/s. Round after and prepare to make it a
        # string for the GUI.
        def vel_dg_to_as_str(degree: float) -> str:
            """Converting to arcseconds per second then formatting."""
            arcsecond = library.conversion.degrees_per_second_to_arcsec_per_second(
                degree_per_second=degree
            )
            return "{vel:.3f}".format(vel=arcsecond)

        def acc_dg_to_as_str(degree: float) -> str:
            """Converting to arcseconds per second squared then formatting.
            Accelerations are usually a lot less and thus should have
            scientific notation."""
            # The extra second factor doesn't matter.
            arcsecond = library.conversion.degrees_per_second_to_arcsec_per_second(
                degree_per_second=degree
            )
            return "{acc:.4e}".format(acc=arcsecond)

        ra_v_arcsec_str = vel_dg_to_as_str(ra_v_deg)
        dec_v_arcsec_str = vel_dg_to_as_str(dec_v_deg)
        ra_a_arcsec_str = acc_dg_to_as_str(ra_a_deg)
        dec_a_arcsec_str = acc_dg_to_as_str(dec_a_deg)
        # Update the dynamic text.
        self.ui.label_dynamic_ephemeris_results_first_order_ra_rate.setText(
            ra_v_arcsec_str
        )
        self.ui.label_dynamic_ephemeris_results_first_order_dec_rate.setText(
            dec_v_arcsec_str
        )
        self.ui.label_dynamic_ephemeris_results_second_order_ra_rate.setText(
            ra_a_arcsec_str
        )
        self.ui.label_dynamic_ephemeris_results_second_order_dec_rate.setText(
            dec_a_arcsec_str
        )

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
        # If there is no ephemeris solution, there is nothing to be done.
        primary_solution = self.opihi_solution_list[self.primary_file_index]
        if not (
            isinstance(primary_solution, opihiexarata.OpihiSolution)
            and isinstance(primary_solution.propagatives, propagate.PropagativeSolution)
        ):
            return None

        # Update the rate text with the velocity terms provided by the
        # propagation solution. The propagation solution provides rates as
        # degrees per second.
        ra_v_deg = primary_solution.propagatives.ra_velocity
        dec_v_deg = primary_solution.propagatives.dec_velocity
        # And acceleration, as degrees per second squared.
        ra_a_deg = primary_solution.propagatives.ra_acceleration
        dec_a_deg = primary_solution.propagatives.dec_acceleration
        # Converting to the more familiar arcsec/s from deg/s along with
        # arcsec/s/s from deg/s/s. Round after and prepare to make it a
        # string for the GUI.
        def vel_dg_to_as_str(degree: float) -> str:
            """Converting to arcseconds per second then formatting."""
            arcsecond = library.conversion.degrees_per_second_to_arcsec_per_second(
                degree_per_second=degree
            )
            return "{vel:.3f}".format(vel=arcsecond)

        def acc_dg_to_as_str(degree: float) -> str:
            """Converting to arcseconds per second squared then formatting.
            Accelerations are usually a lot less and thus should have
            scientific notation."""
            # The extra second factor doesn't matter.
            arcsecond = library.conversion.degrees_per_second_to_arcsec_per_second(
                degree_per_second=degree
            )
            return "{acc:.4e}".format(acc=arcsecond)

        ra_v_arcsec_str = vel_dg_to_as_str(ra_v_deg)
        dec_v_arcsec_str = vel_dg_to_as_str(dec_v_deg)
        ra_a_arcsec_str = acc_dg_to_as_str(ra_a_deg)
        dec_a_arcsec_str = acc_dg_to_as_str(dec_a_deg)
        # Update the dynamic text.
        self.ui.label_dynamic_propagate_results_first_order_ra_rate.setText(
            ra_v_arcsec_str
        )
        self.ui.label_dynamic_propagate_results_first_order_dec_rate.setText(
            dec_v_arcsec_str
        )
        self.ui.label_dynamic_propagate_results_second_order_ra_rate.setText(
            ra_a_arcsec_str
        )
        self.ui.label_dynamic_propagate_results_second_order_dec_rate.setText(
            dec_a_arcsec_str
        )

        # All done.
        return None

    def draw_nothing(self) -> None:
        """This function clears the plot completely and assigns no data to it.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Clear the plot.
        self.opihi_axes.clear()
        self.opihi_canvas.draw()
        # All done.
        return None

    def draw_opihi_image(self) -> None:
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
        self.draw_nothing()

        # This is a function which allows for the disabling of other axes
        # formatting their data values and messing with the formatter class.
        def empty_string(string: str) -> str:
            return str()

        # We plot based on the primary solution as everything which is worth
        # plotting comes from the primary solution.
        primary_solution = self.opihi_solution_list[self.primary_file_index]
        if not isinstance(primary_solution, opihiexarata.OpihiSolution):
            return None

        # These are points in future time which will be used to plot the
        # ephemeris and propagation solutions, if they exist. However,
        # as the time step is in seconds, and the standard time of this
        # system is in Julian days, we convert.
        if isinstance(primary_solution.observing_time, (int, float)):
            # We can only do this if we know the time that the image was taken
            # at.
            TIMESTEP_JD = (
                library.config.GUI_MANUAL_FUTURE_TIME_PLOT_TIMESTEP_SECONDS / 86400
            )
            N_POINTS = library.config.GUI_MANUAL_FUTURE_TIME_PLOT_STEP_COUNT
            # Numpy says linspace is more stable for decimal non-integer steps.
            future_time_plot = np.linspace(
                primary_solution.observing_time,
                primary_solution.observing_time + TIMESTEP_JD * N_POINTS,
                N_POINTS,
                endpoint=True,
            )

        # The data that will be plotted.
        plotting_data = primary_solution.data
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
            target_x, target_y = primary_solution.asteroid_location
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
        if isinstance(primary_solution.ephemeritics, ephemeris.EphemeriticSolution):
            # The astrometric solution is also needed to convert it back to
            # pixel coordinates. As the ephemeritic solution requires the
            # astrometric solution, this is fine.
            astrometrics = primary_solution.astrometrics
            ephemeritics = primary_solution.ephemeritics
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
        if isinstance(primary_solution.propagatives, propagate.PropagativeSolution):
            # The astrometric solution is also needed to convert it back to
            # pixel coordinates. As the ephemeritic solution requires the
            # astrometric solution, this is fine.
            astrometrics = primary_solution.astrometrics
            propagatives = primary_solution.propagatives
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
            self.draw_nothing()
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

        # This is a function which allows for the disabling of other axes
        # formatting their data values and messing with the formatter class.
        def empty_string(string: str) -> str:
            return str()

        # We load the busy image.
        busy_image = gui.functions.get_busy_image_array()

        # Determining the width/height shape of the image.
        busy_height, busy_width, __ = busy_image.shape
        # From the shape of the image, and the shape of the array, we pin the
        # origin of the image. We desired a centered image.
        # We take it from the primary image's shape.
        primary_solution = self.opihi_solution_list[self.primary_file_index]
        if isinstance(primary_solution, opihiexarata.OpihiSolution):
            data_height, data_width = primary_solution.data.shape
        else:
            # A rough approximation is good enough.
            data_height, data_width = (2048, 2048)

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
        image = self.opihi_axes.imshow(
            busy_image,
            aspect="equal",
            alpha=transparency,
            extent=(left_extent, right_extent, bottom_extent, top_extent),
            zorder=10,
        )
        # Disable their formatting in favor of ours.
        image.format_cursor_data = empty_string
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
        # We ju
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
