"""This contains the Python wrapper class around Orbfit, assuming the 
installation procedure was followed."""

import glob
import os
import platform
import shutil
import subprocess

import astropy as ap
import astropy.table as ap_table
import numpy as np

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

# Handling Windows installs are a little more involved so this flag determines
# if it is needed.
_IS_WINDOWS_OPERATING_SYSTEM = (
    True if platform.system().casefold() == "windows" else False
)


class OrbfitOrbitDeterminerEngine(library.engine.OrbitEngine):
    """Uses the Orbfit package to determine the orbital elements of an astroid
    provided observations. This assumes that the installation instructions
    provided were followed.

    Attributes
    ----------
    orbital_elements : dict
        The six Keplarian orbital elements.
    orbital_elements_errors : dict
        The errors of the orbital elements.
    """

    def __init__(self) -> None:
        """Instantiation of the orbfit package.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Ensure that the installation is actually valid; otherwise this
        # entire class would be useless.
        self.__check_installation()

        # Operating in the temporary directory would clutter it unnecessarily.
        # Instead, we work in a subdirectory of it.
        self.ORBFIT_OPERATING_DIR = os.path.abspath(
            os.path.join(library.config.TEMPORARY_DIRECTORY, "operate_orbfit")
        )
        # Preparing the directory for orbfit to work in.
        self._prepare_orbfit_files()
        # Pre-cleaning of the directory in the event some files were leftover.
        self._clean_orbfit_files()

        return None

    @classmethod
    def __check_installation(cls, no_raise: bool = False) -> bool:
        """Check if the installation was completed according to the
        documentation provided. This functions only checks for the existence
        of the template files.

        Parameters
        ----------
        no_raise : bool, default = False
            By default, an invalid install will raise. Set this if a False
            return without interrupting the flow of the program is desired.

        Returns
        -------
        valid_install : bool
            If the installation is detected to be valid, then this returns True.
        """
        # By default, we assume the installation was wrong.
        valid_install = False
        # If the user wants this to run without raising, then catching all of
        # the raises that would have happened anyways is a easy solution.
        if no_raise:
            try:
                valid_install = cls.__check_installation(no_raise=False)
            except error.InstallError:
                valid_install = False
            finally:
                return valid_install
        else:
            # Otherwise... Let the program stop on a bad install... continuing.
            pass

        ORBFIT_PATH = library.config.ORBFIT_DIRECTORY
        ORBFIT_BIN_PATH = library.config.ORBFIT_BINARY_EXECUTABLE_DIRECTORY
        # Defined by the install process.
        ORBFIT_TEMPLATE_PATH = os.path.join(ORBFIT_PATH, "exarata")
        # These paths are defined by the assumptions made in the install
        # process. If these do not exist, it is highly likely the installation
        # step for this was not done and it is known that this class will not
        # do anything.
        INP_FILE_PATHNAME = library.path.merge_pathname(
            directory=ORBFIT_TEMPLATE_PATH, filename="exarata", extension="inp"
        )
        OBS_FILE_PATHNAME = library.path.merge_pathname(
            directory=ORBFIT_TEMPLATE_PATH, filename="exarata", extension="obs"
        )
        OOP_FILE_PATHNAME = library.path.merge_pathname(
            directory=ORBFIT_TEMPLATE_PATH, filename="exarata", extension="oop"
        )
        ORBFIT_EXECUTABLE = library.path.merge_pathname(
            directory=[ORBFIT_PATH, "bin"], filename="orbfit", extension="x"
        )
        # Test if the files exist.
        if not os.path.exists(INP_FILE_PATHNAME):
            raise error.InstallError(
                "The input file which should contain the name of their targets does not"
                " exist. Please follow the instructions on setting up the OpihiExarata"
                " template files."
            )
        if not os.path.exists(OBS_FILE_PATHNAME):
            raise error.InstallError(
                "The observational file which should contain the name of their targets"
                " does not exist. Please follow the instructions on setting up "
                " the OpihiExarata template files."
            )
        if not os.path.exists(OOP_FILE_PATHNAME):
            raise error.InstallError(
                "The operations file which should contain the name of their targets"
                " does not exist. Please follow the instructions on setting up "
                " the OpihiExarata template files."
            )
        if not os.path.exists(ORBFIT_EXECUTABLE):
            raise error.InstallError(
                "The orbfit compiled executable does not exist in the expected binary"
                " directory. This is indicative of a bad install of OrbFit. Please"
                " reinstall Orbfit."
            )

        # An additional check is needed if the system is Windows; the
        # Powershell method uses Linux root pathnames for the mounted drive.
        # For a Linux system however, the additional handling is not needed.
        if _IS_WINDOWS_OPERATING_SYSTEM:
            # Special handling must be used for the path because the path
            # provided by the configuration file is an absolute path and
            # path join cuts off the preceding paths.
            test_binary_dir = os.path.join(
                *[R"\\wsl$", "Ubuntu/", ORBFIT_BIN_PATH.removeprefix("/")]
            )
        else:
            test_binary_dir = ORBFIT_BIN_PATH
        test_binary_path = library.path.merge_pathname(
            directory=test_binary_dir, filename="orbfit", extension="x"
        )
        if not os.path.exists(test_binary_path):
            raise error.InstallError(
                "The orbfit compiled executable does not exist in the expected"
                " directory as per the install instructions. However, it was found in a"
                " previous check using the orbfit directory. Check your configuration"
                " file that the binary executable directory entry is correct."
            )

        # If it passed without raising any errors, then the install is likely
        # fine.
        valid_install = True
        return valid_install

    def _prepare_orbfit_files(self) -> None:
        """This function prepares the operational directory for Orbfit inside
        of the temporary directory. This allows for files to be generated for
        useage by the binary orbfit.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # The paths which hold the needed files.
        ORBFIT_BIN = library.config.ORBFIT_BINARY_EXECUTABLE_DIRECTORY
        ORBFIT_DIR = library.config.ORBFIT_DIRECTORY
        ORBFIT_TEM = os.path.join(ORBFIT_DIR, "exarata")

        # The environment which Orbfit will run needs to be prepared first.
        ORBFIT_OPERATING_DIR = self.ORBFIT_OPERATING_DIR
        if os.path.isdir(ORBFIT_OPERATING_DIR):
            # It probably already exists because this was run before.
            pass
        else:
            os.makedirs(ORBFIT_OPERATING_DIR)
        # Copying the template files.
        orbfit_list = glob.glob(
            library.path.merge_pathname(
                directory=ORBFIT_TEM, filename="*", extension="*"
            )
        )
        for filedex in orbfit_list:
            shutil.copy(filedex, ORBFIT_OPERATING_DIR)
        return None

    def _clean_orbfit_files(self) -> None:
        """This function cleans up the operational directory of Orbfit.
        If there are leftover files, the program may try to use them in a
        manner which is not desired. It is usually better to start from
        scratch each time to avoid these issues.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # The operational directory.
        ORBFIT_OPERATING_DIR = self.ORBFIT_OPERATING_DIR
        # Removing the files which are considered the results of the orbit
        # determination; both error files and the completed files. This
        # is based off of the Makefile clean function in the tests.
        extentions_to_delete = ["pro", "clo", "odc", "oel", "olg", "oep", "rwo", "err"]
        # Delete the files.
        for extdex in extentions_to_delete:
            matching_files = glob.glob(
                library.path.merge_pathname(
                    directory=ORBFIT_OPERATING_DIR, filename="*", extension=extdex
                )
            )
            # Removing the files which match the extension pattern.
            for filedex in matching_files:
                os.remove(filedex)

        # Resetting the observation file. Although the writing of the file
        # should overwrite it, this is a fall back just in case.
        obs_filename = library.path.merge_pathname(
            directory=ORBFIT_OPERATING_DIR, filename="exarata", extension="obs"
        )
        os.remove(obs_filename)
        with open(obs_filename, "w"):
            pass

        # All done.
        return None

    def _solve_single_orbit(
        self, observation_table: hint.Table
    ) -> tuple[dict, dict, float]:
        """This uses the Orbfit program to an orbit provided a record of
        observations. If it cannot be solved, an error is raised.

        This function is not intended to solve an entire set of observations,
        but instead a subset of them. The rational being that orbfit tends to
        fail on larger sets; averaging the values of smaller sets is a little
        more robust against failure. Use the non-hidden function to compute
        orbital elements for a full range of observations.

        Parameters
        ----------
        observation_table : Astropy Table
            The table of observations; this will be converted to the
            required formats for processing.

        Returns
        -------
        kepler_elements : dict
            The Keplarian orbital elements.
        kepler_error : dict
            The error on the Keplarian orbital elements.
        modified_julian_date : float
            The modified Julian date corresponding to the osculating orbit and
            the Keplerian orbital parameters provided.
        """
        # The paths which hold the needed files.
        ORBFIT_BIN = library.config.ORBFIT_BINARY_EXECUTABLE_DIRECTORY
        ORBFIT_DIR = library.config.ORBFIT_DIRECTORY
        ORBFIT_TEM = os.path.join(ORBFIT_DIR, "exarata")
        ORBFIT_OPERATING_DIR = self.ORBFIT_OPERATING_DIR

        # Convert the table into the needed 80-column format.
        obs_record = library.mpcrecord.minor_planet_table_to_record(
            table=observation_table
        )
        # Creating the observation file.
        obs_file = library.path.merge_pathname(
            directory=ORBFIT_OPERATING_DIR, filename="exarata", extension="obs"
        )
        with open(obs_file, "w") as file:
            # Because for some reason, newlines needs to be added in manually.
            file.writelines(recorddex + "\n" for recorddex in obs_record)

        # Execute the Orbfit program, this function call is operating system
        # dependnet so we need to handle both Windows and Linux.
        ORBFIT_EXE = library.path.merge_pathname(
            directory=ORBFIT_BIN, filename="orbfit", extension="x"
        )
        if _IS_WINDOWS_OPERATING_SYSTEM:
            # The Orbfit executable must use POSIX-like pathnames only as it is
            # accessed via WSL. This is a little shoddy.
            ORBFIT_EXE_WSL_PATH = ORBFIT_EXE.replace("\\", "/")
            # Leveraging Powershell and WSL.
            windows_command = (
                'powershell.exe "cd {opdir}; wsl echo exarata | wsl {orbexe}"'.format(
                    opdir=ORBFIT_OPERATING_DIR, orbexe=ORBFIT_EXE_WSL_PATH
                )
            )
            command = windows_command
        else:
            # Standard Linux.
            linux_command = "cd {opdir}; echo exarata | {orbexe}".format(
                opdir=ORBFIT_OPERATING_DIR, orbexe=ORBFIT_EXE
            )
            command = linux_command
        # Run the command and complete the orbital elements via the Orbfit
        # executable.
        __ = subprocess.run(command, shell=True)

        # Process the output. The results, if successful are stored in an
        # orbital elements file which needs to be processed and read in.
        # Otherwise, if it failed, then orbfit uses a file flag.
        orbit_file_path = library.path.merge_pathname(
            directory=ORBFIT_OPERATING_DIR, filename="exarata", extension="oel"
        )
        error_file_path = library.path.merge_pathname(
            directory=ORBFIT_OPERATING_DIR, filename="exarata", extension="err"
        )
        if os.path.isfile(error_file_path):
            # The orbit determincation failed, likely because the software
            # could not converge on a good fit.
            self._clean_orbfit_files()
            raise error.EngineError(
                "The orbfit software could not determine a fitting orbit solution."
            )
        elif os.path.isfile(orbit_file_path):
            # The orbit has been determined. The parameters can be extracted
            # from the orbit file.
            with open(orbit_file_path, "r") as file:
                content = file.readlines()
                # Stripping the newlines; the list itself kind of encodes this.
                content = [linedex.strip() for linedex in content]
                # Getting the Kepler orbital elements.
                kep_ele_line = str(
                    [linedex for linedex in content if "KEP" in linedex][0]
                )
                # Getting the errors on the Kepler orbital elements.
                try:
                    kep_err_line = str(
                        [linedex for linedex in content if "RMS" in linedex][0]
                    )
                except IndexError:
                    # It does not look like an error was computed; using
                    # the configuration defaults. Filling in what is the usual
                    # line in the orbit file, but with the new errors.
                    LIN_ERR_FRAC = library.config.ORBFIT_MAXIMUM_LINEAR_ERROR
                    ANG_ERR_FRAC = library.config.ORBFIT_MAXIMUM_ANGULAR_ERROR
                    kep_err_line = (
                        "! RMS    {la}   {le}   {a}   {a}   {a}   {a}".format(
                            la=float(kep_ele_line.split()[1:][0]) * LIN_ERR_FRAC,
                            le=float(kep_ele_line.split()[1:][1]) * LIN_ERR_FRAC,
                            a=360 * ANG_ERR_FRAC,
                        )
                    )
                # The modified Julian date which these elements correspond to.
                mjd_dat_line = str(
                    [linedex for linedex in content if "MJD" in linedex][0]
                )
            # Clean up the results so that it does not interfere with future
            # runs.
            self._clean_orbfit_files()
            # The order of the elements and the errors are the same; this
            # key from the file.
            kep_ele_keys = (
                "semimajor_axis",
                "eccentricity",
                "inclination",
                "longitude_ascending_node",
                "argument_perihelion",
                "mean_anomaly",
            )
            # The beginning characters, which identified the line, are not
            # needed and would mess up float conversion otherwise.
            kep_ele_values = np.array(kep_ele_line.split()[1:], dtype=float)
            kep_err_values = np.array(kep_err_line.split()[2:], dtype=float)
            mjd_dat_values = float(mjd_dat_line.split()[1:-1][0])
            # Constructing the dictionary which holds the values. The error
            # is also noted in the key to avoid confusion.
            kep_ele_dict = {
                keydex: valuedex
                for keydex, valuedex in zip(kep_ele_keys, kep_ele_values)
            }
            kep_err_dict = {
                keydex + "_error": valuedex
                for keydex, valuedex in zip(kep_ele_keys, kep_err_values)
            }
        else:
            raise error.UndiscoveredError(
                "The output from orbfit execution is unexpected. Neither an orbital"
                " elements file or an error file exists."
            )
        # For documentation naming conventions.
        kepler_elements = kep_ele_dict
        kepler_error = kep_err_dict
        modified_julian_date = mjd_dat_values
        return kepler_elements, kepler_error, modified_julian_date

    def solve_orbit(self, observation_table: hint.Table) -> tuple[dict, dict, float]:
        """Attempts to compute Keplarian orbits provided a table of observations.

        This function attempts to compute the orbit using the entire
        observation table. If it is unable to, then the observations are split
        into subsets based on the year of observations. The derived orbital
        elements are averaged and errors propagated. If no orbit is found,
        then an error is raised.

        Parameters
        ----------
        observation_record : Astropy Table
            The table of observational records; this will be converted to the
            required MPC 80 column format.

        Returns
        -------
        kepler_elements : dict
            The Keplarian orbital elements.
        kepler_error : dict
            The error on the Keplarian orbital elements.
        modified_julian_date : float
            The modified Julian date corresponding to the osculating orbit and
            the Keplerian orbital parameters provided.
        """

        # First attempt to do the entire observation table. If it works, then
        # swell.
        try:
            sng_k_ele, sng_k_err, sng_mjd_date = self._solve_single_orbit(
                observation_table=observation_table
            )
        except error.EngineError:
            # The fit failed. The observation table will be split to see if
            # the more robust option might work.
            pass
        except Exception:
            # Some other unexpected error has occurred; reraise with a higher
            # priority for development.
            raise error.UndiscoveredError
        else:
            # Using the entire observation table worked.
            # For documentation naming conventions.
            kepler_elements = sng_k_ele
            kepler_error = sng_k_err
            modified_julian_date = sng_mjd_date
            return kepler_elements, kepler_error, modified_julian_date
        finally:
            # Cleaning up for future runs.
            self._clean_orbfit_files()

        # If the code gets here, then the single attempt failed and what is
        # next is to split up the observation table.

        # Extracting the year of the observations.
        year_array = np.array(observation_table["year"])
        unique_years = set(year_array)

        # The data results.
        kep_ele_dict_list = []
        kep_err_dict_list = []
        mod_jul_date_list = []

        # We derive the observational subtables by just indexing the main table based
        # on the year.
        for uyeardex in unique_years:
            subset_rows = np.where(year_array == uyeardex)
            subset_obs_table = observation_table[subset_rows]
            # Attempt to solve for the orbital elements. If it fails, then continue on.
            try:
                ele_dict, err_dict, mjd_flot = self._solve_single_orbit(
                    observation_table=subset_obs_table
                )
            except error.EngineError:
                # The fit likely failed, this observational subtable will provide us
                # nothing.
                continue
            else:
                # Keep the results to average out later.
                kep_ele_dict_list.append(ele_dict)
                kep_err_dict_list.append(err_dict)
                mod_jul_date_list.append(mjd_flot)
            finally:
                # Clean up the current files for the next computation.
                self._clean_orbfit_files()
        # If no results actually came back and no orbit could be found, then no
        # orbital information can be extracted. It should be checked that the results
        # are all of the same length though.
        if len(kep_ele_dict_list) == len(kep_err_dict_list) == len(mod_jul_date_list):
            if len(mod_jul_date_list) == 0:
                # No results, all of the orbit solving failed.
                raise error.EngineError(
                    "No orbit could be found from the subset of the observations."
                )
            else:
                # Something exists, process it.
                pass
        else:
            # The results returned are not parallel arrays, it is unknown why this would
            # happen.
            raise error.UndiscoveredError

        # The results stored in the dictionaries, it is easier to use tables and arrays
        # despite the overhead.
        kepler_element_table = ap_table.Table(kep_ele_dict_list)
        kepler_error_table = ap_table.Table(kep_err_dict_list)
        mod_julian_date_array = np.array(mod_jul_date_list, dtype=float)

        # In order to statistically combine them, the Julian date needs to be the
        # same.
        if not np.allclose(mod_julian_date_array[:-1], mod_julian_date_array[1:]):
            raise error.InputError(
                "The modified Julian dates are not the same. The orbfit configuration"
                " file created at install should contain the same date."
            )

        # The mean of the parameters. The angles needs to be treated differently as
        # they are circular quantities. See https://en.wikipedia.org/wiki/Circular_mean
        # Wrapper functions make it easy to implement with error propagation.
        def _average_angle(ang: hint.array, err: hint.array) -> tuple[float, float]:
            """Finds the average and the propagated error of angles in degrees."""
            # Numpy trigonometric functions use radians.
            angles_rad = ang * (np.pi / 180)
            # The arctan2 variant of the circular mean is provided.
            circ_mean_rad = np.arctan2(
                np.sum(np.sin(angles_rad)), np.sum(np.cos(angles_rad))
            )
            # Back into degrees.
            circ_mean = circ_mean_rad * (180 / np.pi)
            # Sometimes the average of the angle is an equivalent negative
            # angle; seemingly by convention, the orbital parameter angles
            # should be positive.
            circ_mean = (circ_mean + 360) % 360
            # Linear errors are used because of a lack of a better method.
            lin_error = np.sqrt(np.sum(err**2)) / err.size
            # Done.
            return circ_mean, lin_error

        def _average_linear(data: hint.array, err: hint.array) -> tuple[float, float]:
            """Finds the average and the propagated error of standard linear points."""
            # Linear median; sometimes orbfit throws out some weird answers.
            lin_mean = np.median(data)
            # Linear error propagation.
            lin_error = np.sqrt(np.sum(err**2)) / err.size
            # Done.
            return lin_mean, lin_error

        # Calculating the average of all of the provided values.
        avg_semimajor_axis, err_semimajor_axis = _average_linear(
            data=kepler_element_table["semimajor_axis"],
            err=kepler_error_table["semimajor_axis_error"],
        )
        avg_eccentricity, err_eccentricity = _average_linear(
            data=kepler_element_table["eccentricity"],
            err=kepler_error_table["eccentricity_error"],
        )
        avg_inclination, err_inclination = _average_angle(
            ang=kepler_element_table["inclination"],
            err=kepler_error_table["inclination_error"],
        )
        avg_longitude, err_longitude = _average_angle(
            ang=kepler_element_table["longitude_ascending_node"],
            err=kepler_error_table["longitude_ascending_node_error"],
        )
        avg_periapsis, err_periapsis = _average_angle(
            ang=kepler_element_table["argument_perihelion"],
            err=kepler_error_table["argument_perihelion_error"],
        )
        avg_mean_anomaly, err_mean_anomaly = _average_angle(
            ang=kepler_element_table["mean_anomaly"],
            err=kepler_error_table["mean_anomaly_error"],
        )
        # This really is not needed, but it might be better than using the
        # first value
        avg_mod_julian_date = np.mean(mod_julian_date_array)

        # Assembling the elements into the proper dictionaries to return;
        # same with the errors.
        kepler_elements = {
            "semimajor_axis": avg_semimajor_axis,
            "eccentricity": avg_eccentricity,
            "inclination": avg_inclination,
            "longitude_ascending_node": avg_longitude,
            "argument_perihelion": avg_periapsis,
            "mean_anomaly": avg_mean_anomaly,
        }
        kepler_error = {
            "semimajor_axis_error": err_semimajor_axis,
            "eccentricity_error": err_eccentricity,
            "inclination_error": err_inclination,
            "longitude_ascending_node_error": err_longitude,
            "argument_perihelion_error": err_periapsis,
            "mean_anomaly_error": err_mean_anomaly,
        }
        modified_julian_date = avg_mod_julian_date
        # All done.
        return kepler_elements, kepler_error, modified_julian_date

    def solve_orbit_via_record(
        self, observation_record: list[str]
    ) -> tuple[dict, dict, float]:
        """Attempts to compute Keplarian orbits provided a standard 80-column
         record of observations.

        This function calls and depends on `solve_orbfit`.

        Parameters
        ----------
        observation_record : Astropy Table
            The record of observations in the standard 80-column format.

        Returns
        -------
        kepler_elements : dict
            The Keplarian orbital elements.
        kepler_error : dict
            The error on the Keplarian orbital elements.
        modified_julian_date : float
            The modified Julian date corresponding to the osculating orbit and
            the Keplerian orbital parameters provided.
        """
        # Convert from the record to a the table.
        obs_table = library.mpcrecord.minor_planet_record_to_table(
            records=observation_record
        )
        # Calling the primary function.
        kepler_elements, kepler_error, modified_julian_date = self.solve_orbit(
            observation_table=obs_table
        )
        return kepler_elements, kepler_error, modified_julian_date
