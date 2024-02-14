"""This is where the automatic mode window is implemented."""

import sys
import os
import copy
import threading
import time
import random
import datetime
import zoneinfo

from PySide6 import QtCore, QtWidgets, QtGui

import opihiexarata
import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

import opihiexarata.astrometry as astrometry
import opihiexarata.photometry as photometry

import opihiexarata.gui as gui


class OpihiAutomaticWindow(QtWidgets.QMainWindow):
    """The GUI that is responsible for the implementation of the automatic mode
    of Opihi, fetching images automatically based on time and solving for both
    the astrometry and photometry.

    Only non-GUI attributes are listed here.

    Attributes
    ----------
    fits_fetch_directory : string
        The directory which the fits files should be automatically pulled from.

    fetched_fits_filename : string
        The filename of the fits file which has just most recently fetched.
    working_fits_filename : string
        The filename of the fits file which is being worked on, or will be
        worked on.
    results_fits_filename : string
        The filename of the fits file which has already been solved. The
        results of which is posted.

    fetch_filename_record : list
        A list of all of the files which were fetched before and so it creates
        a record of files which not to do.

    results_opihi_solution : OpihiSolution
        The OpihiSolution of the current results fits file. The results fits
        file solution, when determined to be solved, should be saved to disk
        automatically.

    preprocess_solution : OpihiPreprocessSolution
        The preprocessing solution which is used to convert raw images to
        preprocessed files.

    zero_point_database : OpihiZeroPointDatabaseSolution
        If a zero point database is going to be constructed, as per the
        configuration file, this is the instance which manages the database.

    loop_state : string
        The loop state.
    """

    def __init__(self) -> None:
        """The automatic GUI window for OpihiExarata. This interacts with
        the user with regards to the automatic solving mode of Opihi.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Creating the GUI itself using the Qt framework and the converted
        # Qt designer files.
        super(OpihiAutomaticWindow, self).__init__()
        self.ui = gui.qtui.Ui_AutomaticWindow()
        self.ui.setupUi(self)
        # Window icon, we use the default for now.
        gui.functions.apply_window_icon(window=self, icon_path=None)

        # Establishing the defaults for all of the relevant attributes.
        self.fits_fetch_directory = None
        self.fetch_fits_filename = None
        self.working_fits_filename = None
        self.results_fits_filename = None
        self.fetch_filename_record = []
        self.fetch_opihi_solution = None
        self.results_opihi_solution = None
        self.preprocess_solution = None
        self.zero_point_database = None
        self.loop_state = "None"

        # The configuration file has a default fits fetch directory.
        AF_DIR = library.config.GUI_AUTOMATIC_INITIAL_AUTOMATIC_IMAGE_FETCHING_DIRECTORY
        if os.path.isdir(AF_DIR):
            self.fits_fetch_directory = os.path.abspath(AF_DIR)
        else:
            self.fits_fetch_directory = None

        # Preparing the buttons, GUI, and other functionality.
        self.__init_gui_connections()
        self.__init_preprocess_solution()

        # Preparing the zero point database if the user desired the database
        # to record observations.
        if library.config.GUI_AUTOMATIC_DATABASE_SAVE_OBSERVATIONS:
            database = opihiexarata.OpihiZeroPointDatabaseSolution(
                database_directory=library.config.MONITOR_DATABASE_DIRECTORY
            )
        else:
            database = None
        self.zero_point_database = database

        # Update all of the text.
        self.refresh_window()

        # All done.
        return None

    def __init_gui_connections(self) -> None:
        """Creating the function connections for the GUI interface.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # For the fetch directory.
        self.ui.push_button_change_directory.clicked.connect(
            self.__connect_push_button_change_directory
        )

        # For the start and stop buttons.
        self.ui.push_button_start.clicked.connect(self.__connect_push_button_start)
        self.ui.push_button_stop.clicked.connect(self.__connect_push_button_stop)
        self.ui.push_button_trigger.clicked.connect(self.__connect_push_button_trigger)

        # All done.
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
        except Exception as err:
            # Something failed with making the preprocess solution, a
            # configuration file issue is likely the reason.
            error.warn(
                warn_class=error.UnknownWarning,
                message=(
                    "We are not sure why the preprocess solution failed. {e}".format(
                        e=err
                    )
                ),
            )
        finally:
            self.preprocess_solution = preprocess
        # All done.
        return None

    def __connect_push_button_change_directory(self) -> None:
        """The connection for the button to change the automatic fetch
        directory.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Ask the user for the filename via a dialog.
        # We start off from the current one for some semblance of consistency.
        new_fetch_directory = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select Opihi Fetch Directory",
            dir=self.fits_fetch_directory,
            options=QtWidgets.QFileDialog.ShowDirsOnly,
        )
        # If the user did not provide a file to enter, there is nothing to be
        # changed.
        if os.path.isdir(new_fetch_directory):
            # Assign the new fits filename.
            self.fits_fetch_directory = os.path.abspath(new_fetch_directory)
        else:
            # Nothing to do.
            pass
        # Refresh the GUI information.
        self.refresh_window()
        # All done.
        return None

    def __connect_push_button_trigger(self) -> None:
        """This does one process, fetching a single image and processing it as
        normal. However, it does not trigger the automatic mode loop as it is
        built for a single image only.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # As we instigated a manual trigger, update the GUI/status.
        self.loop_state = "trigger"
        self.refresh_window()
        # We just call the trigger itself. We still thread it out as to not
        # completely freeze the GUI.
        self.threaded_trigger_opihi_image_solve()
        return None

    def __connect_push_button_start(self) -> None:
        """This enables the automatic active mode by changing the flag and
        starting the process.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Enable the flag.
        self.loop_state = "running"
        # Start the automatic loop.
        self.threaded_automatic_opihi_image_solve()
        self.refresh_window()
        # All done.
        return None

    def __connect_push_button_stop(self) -> None:
        """This disables the automatic active mode by changing the flag. The
        loop itself should detect that the flag has changed. It finishes the
        current process but does not fetch any more.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Enable the flag.
        self.loop_state = "stopped"
        self.refresh_window()
        # All done.
        return None

    def fetch_new_filename(self) -> str:
        """This function fetches a new fits filename based on the most recent
        filename within the automatic fetching directory.

        Parameters
        ----------
        None

        Returns
        -------
        fetched_filename : string
            The filename that was fetched. It is the most recent file added to
            the automatic fetching directory.
        """
        # We are looking for only fits files.
        try:
            fits_extension = "fits"
            fetched_filename = library.path.get_most_recent_filename_in_directory(
                directory=self.fits_fetch_directory,
                extension=fits_extension,
                recursive=True,
                exclude_opihiexarata_output_files=True,
            )
        except ValueError:
            # There is likely no actual matching file in the directory.
            fetched_filename = None
        else:
            # Absolute paths are generally much easier to work with.
            fetched_filename = os.path.abspath(fetched_filename)
        return fetched_filename

    def verify_new_filename(self, filename: str) -> bool:
        """This function verifies a filename. Basically, it checks that the
        file exists and has not already been done before.

        Parameters
        ----------
        filename : string
            The filename to verify.

        Returns
        -------
        verification : bool
            If the filename is good, it it True.
        """
        # We assume the filename is good.
        verification = True

        # Initial check.
        if filename is None:
            # There is no filename.
            verification = False
            return verification
        else:
            # Absolute paths are easier to work with.
            filename = os.path.abspath(str(filename))

        # We first need to test if the file even exits.
        if not os.path.isfile(filename):
            # The file does not exist so it fails verification.
            verification = False

        # If the file is the same as the results file, it
        # has already been done.
        working_fits_filename = str(copy.deepcopy(self.working_fits_filename))
        results_fits_filename = str(copy.deepcopy(self.results_fits_filename))
        if os.path.isfile(working_fits_filename) and os.path.samefile(
            filename, working_fits_filename
        ):
            verification = False
        if os.path.isfile(results_fits_filename) and os.path.samefile(
            filename, results_fits_filename
        ):
            verification = False

        # If the file is already a processed file.
        if library.config.PREPROCESS_DEFAULT_SAVING_SUFFIX in filename:
            verification = False
        if library.config.GUI_AUTOMATIC_DEFAULT_FITS_SAVING_SUFFIX in filename:
            verification = False

        # If there exists processed versions of the file.
        file_dir, file_base, file_ext = library.path.split_pathname(pathname=filename)
        proposed_preprocess_filename = library.path.merge_pathname(
            directory=file_dir,
            filename=file_base + library.config.PREPROCESS_DEFAULT_SAVING_SUFFIX,
            extension=file_ext,
        )
        proposed_solved_filename = library.path.merge_pathname(
            directory=file_dir,
            filename=file_base
            + library.config.GUI_AUTOMATIC_DEFAULT_FITS_SAVING_SUFFIX,
            extension=file_ext,
        )
        proposed_preprocess_solved_filename = library.path.merge_pathname(
            directory=file_dir,
            filename=file_base
            + library.config.PREPROCESS_DEFAULT_SAVING_SUFFIX
            + library.config.GUI_AUTOMATIC_DEFAULT_FITS_SAVING_SUFFIX,
            extension=file_ext,
        )
        if os.path.isfile(proposed_preprocess_filename):
            verification = False
        if os.path.isfile(proposed_solved_filename):
            verification = False
        if os.path.isfile(proposed_preprocess_solved_filename):
            verification = False

        # We do an early exit check here to save processing time.
        if not verification:
            return verification

        # Now we check based on all previously fetched files.
        for filedex in copy.deepcopy(self.fetch_filename_record):
            if filename == filedex:
                verification = False

        return bool(verification)

    def trigger_opihi_image_solve(self) -> None:
        """This function does a single instance of the automatic solving.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # It is always good to have a refresh of the information.
        self.refresh_window()

        # A new image is to be solved. We fetch the new image.
        self.fetch_fits_filename = self.fetch_new_filename()
        self.refresh_window()
        # We need to verify the filename before doing anything.
        if not self.verify_new_filename(filename=self.fetch_fits_filename):
            # The file cannot be verified to be a good file so we do nothing.
            return None

        # The filename is officially a working filename now.
        working_fits_filename = copy.deepcopy(self.fetch_fits_filename)
        self.working_fits_filename = copy.deepcopy(working_fits_filename)
        self.refresh_window()
        # We add it to the record.
        self.fetch_filename_record.append(working_fits_filename)

        # We have a new file, however, in the unlikely event that this
        # file is still being written and is locked under permissions because
        # it is mid-write, we wait a little bit.
        library.http.api_request_sleep(seconds=1)

        # If we have a preprocessing solution, we can preprocess the data first.
        if isinstance(self.preprocess_solution, opihiexarata.OpihiPreprocessSolution):
            preprocess_filename = self.preprocess_opihi_image(
                filename=working_fits_filename
            )
        else:
            # No preprocessing done.
            preprocess_filename = working_fits_filename

        # We need to determine the engines which we will be using to solve
        # this image.
        astrometry_engine_name = self.ui.combo_box_astrometry_engine.currentText()
        astrometry_engine_name = astrometry_engine_name.casefold()
        photometry_engine_name = self.ui.combo_box_photometry_engine.currentText()
        photometry_engine_name = photometry_engine_name.casefold()
        astrometry_engine = opihiexarata.gui.functions.pick_engine_class_from_name(
            engine_name=astrometry_engine_name,
            engine_type=library.engine.AstrometryEngine,
        )
        photometry_engine = opihiexarata.gui.functions.pick_engine_class_from_name(
            engine_name=photometry_engine_name,
            engine_type=library.engine.PhotometryEngine,
        )

        # Now, we try and solve the image.
        opihi_solution = self.solve_opihi_image(
            filename=preprocess_filename,
            astrometry_engine=astrometry_engine,
            photometry_engine=photometry_engine,
        )

        # Refreshing any data.
        self.refresh_window()

        # We attempt to write a zero point record to the database, the wrapper
        # writing function checks if writing to the database is a valid
        # operation. We work on a copy of the solution just in case.
        self.write_zero_point_record_to_database(opihi_solution=opihi_solution)

        # Finally, we try and save the image.
        # Extracting the entire path from the current name, we are saving it
        # to the same location.
        directory, basename, extension = library.path.split_pathname(
            pathname=preprocess_filename
        )
        # We are just adding the suffix to the filename.
        new_basename = (
            basename + library.config.GUI_AUTOMATIC_DEFAULT_FITS_SAVING_SUFFIX
        )
        # Recombining the path.
        saving_fits_filename = library.path.merge_pathname(
            directory=directory, filename=new_basename, extension=extension
        )
        opihi_solution.save_to_fits_file(filename=saving_fits_filename, overwrite=True)

        # The solution is now the most recent results solution.
        self.results_fits_filename = copy.deepcopy(saving_fits_filename)
        self.results_opihi_solution = copy.deepcopy(opihi_solution)

        # Refreshing any data.
        self.refresh_window()

        # All done.
        return None

    def threaded_trigger_opihi_image_solve(self) -> None:
        """This function is just a wrapper around the original function to
        allow for threading.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # We just call the trigger itself. We still thread it out as to not
        # completely freeze the GUI.
        trigger_solving_thread = threading.Thread(target=self.trigger_opihi_image_solve)
        trigger_solving_thread.start()

    def automatic_opihi_image_solve(self) -> None:
        """This function contains the loop which runs to do automatic solving.

        We just model automatic mode as repeatedly clicking the trigger button.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Just to check if there is already a reason to stop.
        stop = self.check_automatic_stops()
        self.refresh_window()
        if stop:
            # We should not even try to do the loop, we are stopped.
            return None

        # Automatic triggering is an infinite loop as we want to do it
        # until stopped via the stop checks.
        while not stop:
            # See if we are to stop; if so, we stop.
            stop = self.check_automatic_stops()
            if stop:
                break

            # We take a little break to ensure that, in the case of no new
            # file from the trigger, we are not hammering the disk too hard.
            __ = library.http.api_request_sleep(
                seconds=library.config.GUI_AUTOMATIC_SOLVE_LOOP_COOLDOWN_DELAY_SECONDS
            )

            # We attempt to do another trigger solve.
            self.threaded_trigger_opihi_image_solve()

            # Refreshing the window.
            self.refresh_window()

        # The loop has been broken and likely this is because the stop check
        # signified to stop. Either way, the automatic loop is no longer
        # active.
        stop = True
        self.loop_state = "stopped"
        self.refresh_window()
        # All done.
        self.refresh_window()

    def threaded_automatic_opihi_image_solve(self) -> None:
        """This function is just a wrapper around the original function to
        allow for threading.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # We just call the trigger itself. We still thread it out as to not
        # completely freeze the GUI.
        automatic_solving_thread = threading.Thread(
            target=self.automatic_opihi_image_solve
        )
        automatic_solving_thread.start()

    def check_automatic_stops(self) -> bool:
        """This function checks for the stops to stop the automatic triggering
        of the next image.

        Parameters
        ----------
        None

        Returns
        -------
        stop : bool
            This is the flag which signifies if the triggering should stop or
            not. If True, the triggering should stop.
        """
        try:
            # Assume we keep on going.
            stop = False

            # Check if internally the GUI stop flag was made.
            if self.loop_state == "running":
                stop = False
            else:
                stop = True

            # The automatic mode should not be running during the day. We set
            # this time as a "good enough" always-daytime limit. This also serves
            # to stop it.
            # We get the timezone we are checking, this is important as the
            # configuration values are local time.
            if library.config.GUI_AUTOMATIC_DAYTIME_BREAK_TIMEZONE is None:
                local_timezone = "Etc/UTC"
            else:
                local_timezone = library.config.GUI_AUTOMATIC_DAYTIME_BREAK_TIMEZONE
            local_time = datetime.datetime.now(zoneinfo.ZoneInfo(local_timezone))
            local_hour = local_time.hour
            # Configuration based Hardcoded "daytime hours".
            if (
                library.config.GUI_AUTOMATIC_DAYTIME_BREAK_LOWER_HOUR
                <= local_hour
                <= library.config.GUI_AUTOMATIC_DAYTIME_BREAK_UPPER_HOUR
            ):
                stop = True

            # Check if a stop file was placed in the directory where the automatic
            # files are being retrieved from. As this is a manual file intervention
            # the program is considered halted rather than stopped.
            stop_file_dir = self.fits_fetch_directory
            stop_file_fname = "opihiexarata"
            stop_file_ext = "stop"
            stop_file_pathname = library.path.merge_pathname(
                directory=stop_file_dir,
                filename=stop_file_fname,
                extension=stop_file_ext,
            )
            if os.path.exists(stop_file_pathname):
                self.loop_state = "halted"
                stop = True

        except Exception as err:
            # For some reason, one of the stop checks could not be done
            # properly, we stop.
            stop = True

        # All done.
        return stop

    def preprocess_opihi_image(self, filename: str) -> str:
        """This function preprocess an Opihi image, where available and
        returns the filename of the preprocessed file.

        Parameters
        ----------
        filename : string
            The filename of file which will be preprocessed.

        Returns
        -------
        preprocess_filename : string
            The filename of the file which has been preprocessed with the
            preprocessed solution of this class instance.
        """
        # We first need to check that we have a preprocess solution.
        if not isinstance(
            self.preprocess_solution, opihiexarata.OpihiPreprocessSolution
        ):
            raise error.InputError(
                "The preprocess solution does not exist, we cannot preprocess any data."
            )

        # We check if the file was already preprocessed.
        header, __ = library.fits.read_fits_image_file(filename=filename)
        is_preprocessed = header.get("OXM_REDU", False)
        if is_preprocessed:
            # The file is already preprocessed, nothing to do.
            return filename

        # Deriving the preprocessed filename.
        file_dir, file_base, file_ext = library.path.split_pathname(pathname=filename)
        preprocess_filename = library.path.merge_pathname(
            directory=file_dir,
            filename=file_base + library.config.PREPROCESS_DEFAULT_SAVING_SUFFIX,
            extension=file_ext,
        )

        # Finally, we attempt to preprocess the data.
        try:
            self.preprocess_solution.preprocess_fits_file(
                raw_filename=filename,
                out_filename=preprocess_filename,
                overwrite=True,
            )
        except Exception as err:
            # Sending out a warning.
            error.warn(
                warn_class=error.UnknownWarning,
                message=(
                    "The data could not be preprocessed, an error was thrown: {e}".format(
                        e=err
                    )
                ),
            )
            # For some reason, the preprocessing failed. Reverting.
            preprocess_filename = filename
        # All done.
        return preprocess_filename

    @staticmethod
    def solve_opihi_image(
        filename: str,
        astrometry_engine: hint.AstrometryEngine,
        photometry_engine: hint.PhotometryEngine,
    ) -> hint.OpihiSolution:
        """This function solves the Opihi image provided by the filename.

        We use a static method here to be a little more thread safe.

        Parameters
        ----------
        filename : string
            The filename to load and solve.
        astrometry_engine : AstrometryEngine
            The astrometry engine to use.
        photometry_engine : PhotometryEngine
            The photometry engine to use.

        Returns
        -------
        opihi_solution : OpihiSolution
            The solution class of the Opihi image after it has been solved
            (or at least attempted to be).
        """
        # Extracting the header of this fits file to get the observing
        # metadata from it.
        header, __ = library.fits.read_fits_image_file(filename=filename)
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
        # From this filename, create the Opihi solution. There is no asteroid
        # information as the automatic mode does not take asteroids into
        # account.
        opihi_solution = opihiexarata.OpihiSolution(
            fits_filename=filename,
            filter_name=filter_name,
            exposure_time=exposure_time,
            observing_time=observing_time,
        )

        # Given the engines, solve for both the astrometry and photometry.
        # We rely on the error handling of the OpihiSolution solving itself.

        try:
            __, __ = opihi_solution.solve_astrometry(
                solver_engine=astrometry_engine,
                overwrite=True,
                raise_on_error=True,
                vehicle_args={},
            )
            __, __ = opihi_solution.solve_photometry(
                solver_engine=photometry_engine,
                overwrite=True,
                raise_on_error=True,
                vehicle_args={},
            )

        except error.ExarataException as err:
            # Something went wrong with the solving. We do nothing more.
            error.warn(
                warn_class=error.InputWarning,
                message="The filename {f} failed to solve with the error {e}".format(
                    f=filename, e=err
                ),
            )

        # All done.
        return opihi_solution

    def write_zero_point_record_to_database(
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
        if not library.config.GUI_AUTOMATIC_DATABASE_SAVE_OBSERVATIONS:
            return None

        # Because many files are being written to the database, we do not
        # want to try and busy the database with cleaning itself up every time
        # we want to write to it so we do it randomly.
        CLEAN_RATE = library.config.GUI_AUTOMATIC_DATABASE_CLEAN_FILE_RATE
        will_clean_record_file = random.random() <= CLEAN_RATE

        # We write the record based on the information from the solution.
        self.zero_point_database.write_zero_point_record_julian_day(
            jd=opihi_solution.observing_time,
            zero_point=opihi_solution.photometrics.zero_point,
            zero_point_error=opihi_solution.photometrics.zero_point_error,
            filter_name=opihi_solution.filter_name,
            clean_file=will_clean_record_file,
        )

        # We additionally create a new figure for the monitoring webpage.
        self.zero_point_database.create_plotly_zero_point_html_plot_via_configuration()

        # All done.
        return None

    def refresh_window(self) -> None:
        """Refreshes the GUI window with new information where available.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Refreshing text.
        self.__refresh_dynamic_label_text()

        # All done.
        return None

    def __refresh_dynamic_label_text(self) -> None:
        """Refreshes the GUI window's dynamic text.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Refreshing the directory text.
        self.ui.label_dynamic_fits_directory.setText(self.fits_fetch_directory)

        # Refreshing the filename text, we do not need the directory part.
        # If the filenames have not been provided, then we just highlight that
        # they have not been provided (which is different from the default
        # filler names).
        if isinstance(self.fetch_fits_filename, str):
            fetch_basename = library.path.get_filename_with_extension(
                pathname=self.fetch_fits_filename
            )
            self.ui.label_dynamic_fetch_filename.setText(fetch_basename)
        else:
            self.ui.label_dynamic_fetch_filename.setText("None")
        if isinstance(self.working_fits_filename, str):
            working_basename = library.path.get_filename_with_extension(
                pathname=self.working_fits_filename
            )
            self.ui.label_dynamic_working_filename.setText(working_basename)
        else:
            self.ui.label_dynamic_working_filename.setText("None")
        if isinstance(self.results_fits_filename, str):
            results_basename = library.path.get_filename_with_extension(
                pathname=self.results_fits_filename
            )
            self.ui.label_dynamic_results_filename.setText(results_basename)
        else:
            self.ui.label_dynamic_results_filename.setText("None")

        # If there is no resulting Opihi solution, then there is no data to be
        # extracted for results. The results solution should also be always
        # solved so we do not need to check for it. We also need to make sure
        # that the astrometric solution and photometric solution was valid.
        if (
            isinstance(self.results_opihi_solution, opihiexarata.OpihiSolution)
            and self.results_opihi_solution.astrometrics_status
            and self.results_opihi_solution.photometrics_status
        ):
            # Obtaining the observing time.
            observing_time_jd = self.results_opihi_solution.observing_time
            (
                year_int,
                moth_int,
                days_int,
                hour_int,
                mint_int,
                secs_float,
            ) = library.conversion.julian_day_to_full_date(jd=observing_time_jd)
            # Allowing for padded zeros for ISO 8601 (like) compatibility,
            # because it is a more unambiguous format.
            date_string = "{y:04d}-{m:02d}-{d:02d}".format(
                y=year_int, m=moth_int, d=days_int
            )
            time_string = "{h:02d}:{m:02d}:{s:04.1f}".format(
                h=hour_int, m=mint_int, s=secs_float
            )
            self.ui.label_dynamic_date.setText(date_string)
            self.ui.label_dynamic_time.setText(time_string)

            # Refreshing the astrometry results.
            ra_deg = self.results_opihi_solution.astrometrics.ra
            dec_deg = self.results_opihi_solution.astrometrics.dec
            # To sexagesimal as it is easier to read, the results provided are
            # in degrees.
            ra_sex, dec_sex = library.conversion.degrees_to_sexagesimal_ra_dec(
                ra_deg=ra_deg, dec_deg=dec_deg, precision=3
            )
            self.ui.label_dynamic_ra.setText(ra_sex)
            self.ui.label_dynamic_dec.setText(dec_sex)

            # Refreshing photometry results.
            zero_point = self.results_opihi_solution.photometrics.zero_point
            zero_point_error = self.results_opihi_solution.photometrics.zero_point_error
            filter_name = self.results_opihi_solution.photometrics.filter_name
            # Formatting the information as a string.
            pm_sym = "\u00b1"
            zero_point_str = "{zp:.3f} {pm} {zpe:.3f}".format(
                zp=zero_point, pm=pm_sym, zpe=zero_point_error
            )
            filter_name = str(filter_name)
            self.ui.label_dynamic_zero_point.setText(zero_point_str)
            self.ui.label_dynamic_filter.setText(filter_name)
        else:
            # There is no OpihiSolution to pull information from.
            pass

        # Refreshing the operational status.
        loop_state = self.loop_state.casefold()
        if loop_state == "none":
            loop_state_string = "None"
        elif loop_state == "trigger":
            loop_state_string = "Trigger"
        elif loop_state == "running":
            loop_state_string = "Running"
        elif loop_state == "stopped":
            loop_state_string = "Stopped"
        elif loop_state == "halted":
            loop_state_string = "Halted"
        else:
            loop_state_string = "Default"
            raise error.DevelopmentError(
                "The operational status flag is `{oflag}`. There is no string refresh"
                " case built to handle this flag. It must be implemented."
            )
        # Setting the string.
        self.ui.label_dynamic_operational_status.setText(loop_state_string)

        # All done.
        return None

    def reset_window(self) -> None:
        """This function resets the window to the default values or
        parameters

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Resetting all of the text to their defaults.
        # Directory.
        self.ui.label_dynamic_fits_directory.setText("/path/to/fits/directory/")
        # Filenames.
        self.ui.label_dynamic_fetch_filename.setText(
            "opi.20XXA999.YYMMDD.AAAAAAAAA.00001.a.fits"
        )
        self.ui.label_dynamic_working_filename.setText(
            "opi.20XXA999.YYMMDD.AAAAAAAAA.00001.a.fits"
        )
        self.ui.label_dynamic_results_filename.setText(
            "opi.20XXA999.YYMMDD.AAAAAAAAA.00001.b.fits"
        )
        # Astrometric coordinates and results.
        self.ui.label_dynamic_ra.setText("RR:RR:RR.RRR")
        self.ui.label_dynamic_dec.setText("+DD:DD:DD.DDD")
        # Photometric results.
        self.ui.label_dynamic_zero_point.setText("ZZZ.ZZZ + EE.EEE")
        self.ui.label_dynamic_filter.setText("FF")
        # Operational status.
        self.ui.label_dynamic_operational_status.setText("Default")

        # All done.
        return None

    def closeEvent(self, event) -> None:
        """We override the original Qt close event to take into account the
        automatic loop.

        Parameters
        ----------
        event : ?
            The event that occurs.

        Returns
        -------
        None
        """
        # We just need to stop the loop, if it is going on.
        self.loop_state = "halted"
        # We can close now.
        event.accept()
        # All done.
        return None


def start_automatic_window() -> None:
    """This is the function to create the automatic window for usage.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    # Creating the application and its infrastructure.
    app = QtWidgets.QApplication([])
    # The automatic GUI window.
    automatic_window = OpihiAutomaticWindow()
    automatic_window.show()
    # Closing out of the window.
    sys.exit(app.exec())
    # All done.
    return None


if __name__ == "__main__":
    start_automatic_window()
