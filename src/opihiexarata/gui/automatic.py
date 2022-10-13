"""This is where the automatic mode window is implemented."""

import sys
import os
import copy
import threading
import time
import random

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
    working_fits_filename : string
        The filename of the fits file which is being worked on, or will be
        worked on.
    results_fits_filename : string
        The filename of the fits file which has already been solved. The
        results of which is posted.
    working_opihi_solution : OpihiSolution
        The OpihiSolution of the current working fits file. The results fits
        file solution, when determined to be solved, should be saved to disk
        automatically.
    results_opihi_solution : OpihiSolution
        The OpihiSolution of the current working fits file. The results fits
        file solution, when determined to be solved, should be saved to disk
        automatically.
    active_status : bool
        The flag which determines if the software is still considered in
        automatic mode and should be still solving images. If True, the process
        assumes that it is still active.
    operational_status_flag : string
        The status flag. This is similar to the active status, but this tracks
        for issues related to the operational state, not the loop itself.
        It primarily contains...

            - normal : Everything is working normally.
            - trigger : An image is being solved by a manual trigger command.
            - failed : An image failed to solve.
            - halted : The automatic mode stopped, but it was not done by the
            active status flag, but a file halt.
    zero_point_database : OpihiZeroPointDatabaseSolution
        If a zero point database is going to be constructed, as per the
        configuration file, this is the instance which manages the database.
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
        self.working_fits_filename = None
        self.results_fits_filename = None
        self.working_opihi_solution = None
        self.results_opihi_solution = None
        self.active_status = False
        self.operational_status_flag = "normal"

        # The configuration file has a default fits fetch directory.
        AF_DIR = library.config.GUI_AUTOMATIC_INITIAL_AUTOMATIC_IMAGE_FETCHING_DIRECTORY
        if os.path.isdir(AF_DIR):
            self.fits_fetch_directory = AF_DIR
        else:
            self.fits_fetch_directory = None

        # Preparing the buttons, GUI, and other functionality.
        self.__init_gui_connections()

        # Preparing the zero point database if the user desired the database
        # to record observations.
        if library.config.GUI_AUTOMATIC_DATABASE_SAVE_OBSERVATIONS:
            database = opihiexarata.OpihiZeroPointDatabaseSolution(
                database_directory=library.config.MONITOR_DATABASE_DIRECTORY
            )
        else:
            database = None
        self.zero_point_database = database

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
        self.active_status = True
        # Start the automatic loop.
        self.automatic_triggering()
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
        self.active_status = False
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
        self.operational_status_flag = "trigger"
        self.refresh_window()
        # We just call the trigger itself. We still thread it out as to not
        # completely freeze the GUI.
        trigger_solving_thread = threading.Thread(target=self.trigger_next_image_solve)
        trigger_solving_thread.start()
        return None

    def automatic_triggering(self) -> None:
        """This function executes the continuous running automatic mode loop.

        All of the stops are checked before a new trigger is executed.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # In order for the infinite loop from the automatic triggering to not
        # also freeze the GUI (as to disallow the user to stop the loop), it
        # should be executed in a separate thread.
        infinite_solving_thread = threading.Thread(
            target=self._automatic_triggering_infinite_loop
        )
        # Starting the infinite loop.
        infinite_solving_thread.start()

        # All done.
        return None

    def _automatic_triggering_infinite_loop(self) -> None:
        """This is where the actual infinite loop is done.

        All of the stops are checked before a new trigger is executed.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Just to check if there is already a reason to stop.
        stop_check = self._automatic_triggering_check_stops()
        self.refresh_window()

        # Automatic triggering is an infinite loop as we want to do it
        # until stopped via the stop checks.
        while True:
            # See if we are to stop.
            stop_check = self._automatic_triggering_check_stops()
            if stop_check:
                # There is an instruction to stop, we do so.
                break
            else:
                # Continuing to executing the next trigger.
                self.trigger_next_image_solve()
                # We take a little break to ensure that, in the case of no new
                # file from the trigger, we are not hammering the disk too hard.
                COOLDOWN = (
                    library.config.GUI_AUTOMATIC_SOLVE_LOOP_COOLDOWN_DELAY_SECONDS
                )
                time.sleep(COOLDOWN)

        # The loop has been broken and likely this is because the stop check
        # signified to stop. Either way, the automatic loop is no longer
        # active.
        self.active_status = not stop_check
        self.refresh_window()
        # All done.
        return None

    def _automatic_triggering_check_stops(self) -> bool:
        """This function checks for the stops to stop the automatic triggering
        of the next image.

        Parameters
        ----------
        None

        Returns
        -------
        stop_check : bool
            This is the flag which signifies if the triggering should stop or
            not. If True, the triggering should stop.
        """
        # Assume we keep on going.
        stop_check = False

        # Check if internally the GUI stop flag was made. If the status is
        # flagged to be stopped, then so the loop should be.
        if self.active_status:
            stop_check = False
        else:
            stop_check = True

        # Check if a stop file was placed in the directory where the automatic
        # files are being retrieved from. As this is a manual file intervention
        # the program is considered halted rather than stopped.
        stop_directory = self.fits_fetch_directory
        stop_filename = "opihiexarata_automatic"
        stop_extension = "stop"
        stop_pathname = library.path.merge_pathname(
            directory=stop_directory, filename=stop_filename, extension=stop_extension
        )
        if os.path.exists(stop_pathname):
            self.operational_status_flag = "halted"
            stop_check = True

        # All done.
        return stop_check

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
                exclude_opihiexarata_output_files=True,
            )
        except ValueError:
            # There is likely no actual matching file in the directory.
            fetched_filename = None
        else:
            # Absolute paths are generally much easier to work with.
            fetched_filename = os.path.abspath(fetched_filename)
        return fetched_filename

    def solve_astrometry_photometry_single_image(
        self, filename: str
    ) -> hint.OpihiSolution:
        """This solves for the astrometric and photometric solutions of a
        provided file. The engines are provided based on the dropdown menus.

        Note this calculation does not affect the `opihi_solution` instance of
        the class. That is a job for a different function.

        Parameters
        ----------
        filename : string
            The filename of the fits file to be solved.

        Returns
        -------
        opihi_solution : OpihiSolution
            The solution with the astrometry and photometry engines solved.
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

        # Determine the astrometry engine from user input via the drop down
        # menu. The recognizing text ought to be case insensitive.
        astrometry_engine_name = self.ui.combo_box_astrometry_engine.currentText()
        astrometry_engine_name = astrometry_engine_name.casefold()
        # Search programed engines for the one specified.
        astrometry_engine = opihiexarata.gui.functions.pick_engine_class_from_name(
            engine_name=astrometry_engine_name,
            engine_type=library.engine.AstrometryEngine,
        )
        astrometry_vehicle_args = {}

        # Determine the photometry engine from user input via the drop down
        # menu. The recognizing text ought to be case insensitive, makes
        # life easier.
        photometry_engine_name = self.ui.combo_box_photometry_engine.currentText()
        photometry_engine_name = photometry_engine_name.casefold()
        # Search programed engines for the one specified.
        photometry_engine = opihiexarata.gui.functions.pick_engine_class_from_name(
            engine_name=photometry_engine_name,
            engine_type=library.engine.PhotometryEngine,
        )
        photometry_vehicle_args = {}

        # Given the engines, solve for both the astrometry and photometry.
        # We rely on the error handling of the OpihiSolution solving itself.
        __, astrometry_solve_status = opihi_solution.solve_astrometry(
            solver_engine=astrometry_engine,
            overwrite=True,
            raise_on_error=False,
            vehicle_args=astrometry_vehicle_args,
        )
        # If the astrometry failed, there is no photometry to do.
        if not astrometry_solve_status:
            __, photometry_solve_status = opihi_solution.solve_photometry(
                solver_engine=photometry_engine,
                overwrite=True,
                raise_on_error=False,
                vehicle_args=photometry_vehicle_args,
            )
        else:
            photometry_solve_status = None

        # Check that the filter compatibility. If the photometry failed, this
        # may be one of the reasons so it is something to warn about.
        if not photometry_solve_status:
            if filter_name not in opihi_solution.photometrics.available_filters:
                print("warn")

        # Saving the file.
        # Extracting the entire path from the current name, we are saving it
        # to the same location.
        directory, basename, extension = library.path.split_pathname(pathname=filename)
        # We are just adding the suffix to the filename.
        suffix = str(library.config.GUI_AUTOMATIC_DEFAULT_FITS_SAVING_SUFFIX)
        new_basename = basename + suffix
        # Recombining the path.
        saving_fits_filename = library.path.merge_pathname(
            directory=directory, filename=new_basename, extension=extension
        )
        opihi_solution.save_to_fits_file(filename=saving_fits_filename, overwrite=True)

        # We attempt to write a zero point record to the database, the wrapper
        # writing function checks if writing to the database is a valid
        # operation. We work on a copy of the solution just in case.
        opihi_solution_copy = copy.deepcopy(opihi_solution)
        # We thread it away.
        write_database_thread = threading.Thread(
            target=self.__write_zero_point_record_to_database,
            kwargs={"opihi_solution": opihi_solution_copy},
        )
        write_database_thread.start()

        # All done.
        return opihi_solution

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
        self.zero_point_database.create_plotly_monitoring_html_plot_via_configuration()

        # All done.
        return None

    def trigger_next_image_solve(self) -> None:
        """This function triggers the next iteration of the automatic solving
        loop.

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
        fetched_filename = self.fetch_new_filename()

        # Test to see if we have already processed this file and currently
        # have information about it. This prevents doing too much work.
        def _is_same_file(file_1: str, file_2: str) -> bool:
            """A small inner function to see if two files are the same
            for the purposes of fetching files."""
            # Assume false, they are not the same file.
            file_1 = file_1 if isinstance(file_1, str) else ""
            file_2 = file_2 if isinstance(file_2, str) else ""
            # If they are the same...
            if file_1 == file_2:
                return True
            # If neither exists...
            if not os.path.isfile(file_1) and not os.path.isfile(file_2):
                return True
            # If they are the same file...
            try:
                return bool(os.path.samefile(file_1, file_2))
            except FileNotFoundError:
                pass
            # All done; as no check says they are the same file, they are not.
            return False

        # Checking if the files are the same...
        if _is_same_file(file_1=fetched_filename, file_2=self.results_fits_filename):
            # The new fetched file is the same one that is already solved. It
            # would be silly to solve it again, there is no point in continuing.
            return None
        elif _is_same_file(file_1=fetched_filename, file_2=self.working_fits_filename):
            # Same principle, this new file is the same as the working file.
            # We need to be patient.
            return None
        else:
            # This new file becomes our working file.
            self.working_fits_filename = fetched_filename
            # Keeping the GUI up to date while in the loop.
            self.refresh_window()

        # With this new working fits file, we attempt to solve it.
        working_opihi_solution = self.solve_astrometry_photometry_single_image(
            filename=self.working_fits_filename
        )
        self.working_opihi_solution = working_opihi_solution

        # If the solve failed, as detected by the status flags, then it cannot
        # be a result.
        if (
            self.working_opihi_solution.astrometrics_status
            and self.working_opihi_solution.photometrics_status
        ):
            # The solving likely worked alright. It is good enough to
            # consider this as a "results" class. A copy is desired so that
            # it does not get mixed up.
            self.operational_status_flag = "normal"
            self.results_fits_filename = copy.deepcopy(self.working_fits_filename)
            self.results_opihi_solution = copy.deepcopy(self.working_opihi_solution)
        elif isinstance(self.working_opihi_solution, opihiexarata.OpihiSolution):
            # The operational status is considered failed. However, there is
            # no reason to stop the loop, but the GUI must be updated.
            self.operational_status_flag = "failed"
        else:
            # The code should not go here, as it should otherwise have been
            # caught by the first two cases as they should be the only valid
            # ones.
            raise error.LogicFlowError(
                "The results of the automatic solving of a single image is either None"
                " or the OpihiSolution class itself. But, neither case was found to be"
                " the case, something is wrong."
            )
        # The GUI should be refreshed with either case.
        self.refresh_window()

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
            pm_sym = "\u00B1"
            zero_point_str = "{zp:.3f} {pm} {zpe:3.f}".format(
                zp=zero_point, pm=pm_sym, zpe=zero_point_error
            )
            filter_name = str(filter_name)
            self.ui.label_dynamic_zero_point.setText(zero_point_str)
            self.ui.label_dynamic_filter.setText(filter_name)
        else:
            # There is no OpihiSolution to pull information from.
            pass
            # For testing.
            self.ui.label_dynamic_time.setText(
                str(library.conversion.current_utc_to_julian_day())
            )

        # Refreshing the operational status.
        operational_status_flag = self.operational_status_flag.casefold()
        if operational_status_flag == "normal":
            # Everything is normal, so the status string can be based on the
            # active status of the system loop.
            if self.active_status:
                status_string = "Running"
            else:
                status_string = "Stopped"
        elif operational_status_flag == "trigger":
            # A manual trigger has been specified.
            status_string = "Triggered"
        elif operational_status_flag == "failed":
            # The solving engines failed to solve.
            status_string = "Failed"
        elif operational_status_flag == "halted":
            # The loop failed to terminate on its own or manual stop file has
            # been made to force the stop of the loop.
            status_string = "Halted"
        else:
            status_string = "Default"
            raise error.DevelopmentError(
                "The operational status flag is `{oflag}`. There is no string refresh"
                " case built to handle this flag. It must be implemented."
            )
        # Setting the string.
        self.ui.label_dynamic_operational_status.setText(status_string)

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
