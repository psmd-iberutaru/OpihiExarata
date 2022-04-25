"""This is the class for a collection of solutions which the GUI interacts
with and acts as the complete solver. There is not engine as it just shuffles
the solutions."""

import copy
import numpy as np

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

import opihiexarata.astrometry as astrometry
import opihiexarata.photometry as photometry
import opihiexarata.propagate as propagate
import opihiexarata.orbit as orbit

# from opihiexarata.ephemeris import EphemerisSolution


class OpihiSolution(hint.ExarataSolution):
    """This is the main class which acts as a collection container of
    solution classes. It facilitates the interaction between the solution
    classes and the GUI.

    Attributes
    ----------
    fits_filename : str
        The fits filename of which is the image which this solution is solving.
    filter_name : str
        The filter_name which this image is taken in.
    exposure_time : float
        The exposure time of the image, in seconds.
    observing_time : float
        The time of observation, this must be a UNIX time.
    asteroid_name : str
        The name of the asteroid. This is used to group similar observations
        and to also retrive data from the MPC.
    asteroid_location : tuple
        The pixel location of the asteroid. (Usually determined by a centroid
        around a user specified location.) If this is None, then asteroid
        calculations are disabled as there is no asteroid.
    asteroid_history : list
        The total observational history of the asteroid provided. This includes
        previous observations done by Opihi and processed by OpihiExarata, but
        does not include the current one. This is the 80-column text file
        form of a MPC record. If this is None, then asteroid calculations are
        disabled as there is no asteroid.
    asteroid_observations : table
        The total observational history of the asteroid provided. This includes
        previous observations done by Opihi and processed by OpihiExarata, but
        does not include the current data. This is the table form of a MPC
        record. If this is None, then asteroid calculations are disabled as
        there is no asteroid.

    header : Astropy Header
        The header of the fits file.
    data : array
        The image data of the fits file itself.


    astrometrics : AstrometricSolution
        The astrometric solution; if it has not been solved yet, this is None.
    photometrics : PhotometricSolution
        The photometric solution; if it has not been solved yet, this is None.
    propagatives : PropagationSolution
        The propagation solution; if it has not been solved yet, this is None.
    orbitals : OrbitSolution
        The orbit solution; if it has not been solved yet, this is None.
    ephemeritics : EphemerisSolution
        The ephemeris solution; if it has not been solved yet, this is None.
    """

    # https://www.adsabs.harvard.edu/full/1895PA......3...17S

    def __init__(
        self,
        fits_filename: str,
        filter_name: str,
        exposure_time: float,
        observing_time: float,
        asteroid_name: str = None,
        asteroid_location: tuple[float, float] = None,
        asteroid_history: list[str] = None,
    ) -> None:
        """Creating the main solution class.

        All of the data which is needed to derive the other solutions should
        be provided. The solutions, however, are only done when called.
        Overriding parameters can be applied when calling the solutions.

        If the asteroid input values are not provided, then this class will
        prohibit calculations meant for asteroids because of the lack
        of an asteroid.

        Parameters
        ----------
        fits_filename : str
            The fits filename of which is the image which this solution is solving.
        filter_name : string
            The filter_name of the image which is contained within the data array.
        exposure_time : float
            The exposure time of the image, in seconds.
        observing_time : float
            The time of observation, this must be a UNIX time.
        asteroid_name : str, default = None
            The name of the asteroid.
        asteroid_location : tuple, default = None
            The pixel location of the asteroid.
        asteroid_history : list, default = None
            The history of observations of an asteroid written in a standard
            80-column MPC record.
        """
        # Collecting the initial instantiation data.
        self.fits_filename = fits_filename
        self.filter_name = filter_name
        self.exposure_time = exposure_time
        self.observing_time = observing_time

        # Loading the fits file to record its data.
        header, data = library.fits.read_fits_image_file(filename=fits_filename)
        self.header = header
        self.data = data

        # See if asteroids are important for this image and if so, lets
        # process the input data. Try to process as much as you can.
        # Formatting the name of the asteroid or target in general.
        try:
            self.asteroid_name = asteroid_name
        except Exception:
            self.asteroid_name = None
        # Formatting the location of the asteroid or the target in general.
        try:
            self.asteroid_location = asteroid_location
        except Exception:
            self.asteroid_location = None
        # Formatting the historical locations of the asteroid or the target
        # in general.
        try:
            self.asteroid_history = asteroid_history
            # From the history, try and derive a table of asteroid observations.
            self.asteroid_observations = library.mpcrecord.minor_planet_record_to_table(
                records=asteroid_history
            )
        except Exception:
            self.asteroid_history = None
            self.asteroid_observations = None

        # Just creating the initial placeholders for the solution.
        self.astrometrics = None
        self.photometrics = None
        self.propagatives = None
        self.orbitals = None
        self.ephemeritics = None
        return None

    def solve_astrometry(
        self, solver_engine: hint.AstrometryEngine, overwrite=True
    ) -> hint.AstrometricSolution:
        """Solve the image astrometry by using an astrometric engine.

        Parameters
        ----------
        solver_engine : AstrometryEngine
            The astrometric engine which the astrometry solver will use.
        overwrite : bool, default = True
            Overwrite and replace the information of this class with the new
            values. If False, the returned solution is not also applied.

        Returns
        -------
        astrometric_solution : AstrometricSolution
            The astrometry solution for the image.
        """
        astrometry_solution = astrometry.AstrometricSolution(
            fits_filename=self.fits_filename, solver_engine=solver_engine
        )
        # Check if the solution should overwrite the current one.
        if overwrite:
            self.astrometrics = astrometry_solution
        else:
            # It should not overwrite anything.
            pass
        return astrometry_solution

    def solve_photometry(
        self,
        solver_engine: hint.PhotometryEngine,
        overwrite=True,
        filter_name=None,
        exposure_time=None,
    ) -> hint.PhotometricSolution:
        """Solve the image photometry by using a photometric engine.

        Parameters
        ----------
        solver_engine : PhotometryEngine
            The photometric engine which the photometry solver will use.
        overwrite : bool, default = True
            Overwrite and replace the information of this class with the new
            values. If False, the returned solution is not also applied.
        filter_name : string, default = None
            The filter name of the image, defaults to the value provided at
            instantiation.
        exposure_time : float, default = None
            The exposure time of the image, in seconds. Defaults to the value
            provided at instantiation.

        Returns
        -------
        photometric_solution : PhotometrySolution
            The photometry solution for the image.

        Warning ..
            This requires that the astrometry solution be computed before-hand.
            This will not precompute automatically it without it being called
            explicitly, but it will instead return an error.
        """
        # The photometric solution requires the astrometric solution to be
        # computed first.
        if not isinstance(self.astrometrics, astrometry.AstrometricSolution):
            raise error.SequentialOrderError(
                "The photometry solution requires an astrometric solution. The"
                " astrometric solution needs to be called and run first."
            )
        # Using the defaults if an overriding value was not provided.
        filter_name = self.filter_name if filter_name is None else filter_name
        exposure_time = self.exposure_time if exposure_time is None else exposure_time

        # Solving the photometric solution.
        photometric_solution = photometry.PhotometricSolution(
            fits_filename=self.fits_filename,
            solver_engine=solver_engine,
            astrometrics=self.astrometrics,
            filter_name=filter_name,
            exposure_time=exposure_time,
        )
        # Check if the solution should overwrite the current one.
        if overwrite:
            self.photometrics = photometric_solution
        else:
            # It should not overrite anything.
            pass
        return photometric_solution

    def solve_propagate(
        self,
        solver_engine: hint.PropagationEngine,
        overwrite=True,
        asteroid_location: tuple[float, float] = None,
    ) -> hint.PropagationSolution:
        """Solve for the location of an asteroid using a method of propagation.

        Parameters
        ----------
        solver_engine : PropagationEngine
            The propagative engine which the propgation solver will use.
        overwrite : bool, default = True
            Overwrite and replace the information of this class with the new
            values. If False, the returned solution is not also applied.
        asteroid_location : tuple, default = None
            The pixel location of the asteroid in the image. Defaults to the
            value provided at instantiation.

        Returns
        -------
        propagative_solution : PropagationSolution
            The propagation solution for the asteroid and image.

        Warning ..
            This requires that the astrometry solution be computed before-hand.
            This will not precompute automatically it without it being called
            explicitly, but it will instead return an error.
        """
        # The propagation solution requires the astrometric solution to be
        # computed first.
        if not isinstance(self.astrometrics, astrometry.AstrometricSolution):
            raise error.SequentialOrderError(
                "The propagation solution requires an astrometric solution. The"
                " astrometric solution needs to be called and run first."
            )
        # The observation time of this asteroid.
        asteroid_time = self.observing_time
        # Using the defaults if an overriding value was not provided.
        asteroid_location = (
            self.asteroid_location if asteroid_location is None else asteroid_location
        )

        # If asteroid information is not provided, then nothing can be solved.
        # As there is no information.
        if asteroid_location is None:
            raise error.InputError(
                "The propagation of an asteroid cannot be solved as no asteroid"
                " location parameters have been provided."
            )
        else:
            # Splitting it up is easier notationally.
            asteroid_x, asteroid_y = asteroid_location
            # The location of the asteroid needs to be transformed to RA and DEC.
            asteroid_ra, asteroid_dec = self.astrometrics.pixel_to_sky_coordinates(
                x=asteroid_x, y=asteroid_y
            )

        # Extracting historical information from which to calculate the
        # propagation from.
        past_asteroid_ra = self.asteroid_observations["ra"]
        past_asteroid_dec = self.asteroid_observations["dec"]
        # Converting the decimal days to the required unix time. This function
        # seems to be vectorized to handle arrays.
        past_asteroid_time = library.conversion.decimal_day_to_unix_time(
            year=self.asteroid_observations["year"],
            month=self.asteroid_observations["month"],
            day=self.asteroid_observations["day"],
        )
        # As arrays.
        past_asteroid_ra = np.asarray(past_asteroid_ra, dtype=float)
        past_asteroid_dec = np.asarray(past_asteroid_dec, dtype=float)
        past_asteroid_time = np.asarray(past_asteroid_time, dtype=float)
        # Propagation only works with really recent observations so we only
        # include those done within some number of hours.
        EXPIRE_HOURS = library.config.OPIHI_PROPAGATION_OBSERVATION_EXPIRATION_HOURS
        EXPIRE_SECONDS = EXPIRE_HOURS * 3600
        valid_observation_index = np.where(
            (asteroid_time - past_asteroid_time) <= EXPIRE_SECONDS, True, False
        )
        valid_past_asteroid_ra = np.asarray(
            past_asteroid_ra[valid_observation_index], dtype=float
        )
        valid_past_asteroid_dec = np.asarray(
            past_asteroid_dec[valid_observation_index], dtype=float
        )
        valid_past_asteroid_time = np.asarray(
            past_asteroid_time[valid_observation_index], dtype=float
        )

        # Add the current observation to the previous observations.
        asteroid_ra = np.append(valid_past_asteroid_ra, asteroid_ra)
        asteroid_dec = np.append(valid_past_asteroid_dec, asteroid_dec)
        asteroid_time = np.append(valid_past_asteroid_time, asteroid_time)

        # Computing the propagation solutions.
        propagative_solution = propagate.PropagationSolution(
            ra=asteroid_ra,
            dec=asteroid_dec,
            obs_time=asteroid_time,
            solver_engine=solver_engine,
        )
        # See if the current propagation solution should be replaced.
        if overwrite:
            self.propagatives = propagative_solution
        else:
            pass
        # All done.
        return propagative_solution

    def solve_orbit(
        self,
        solver_engine: hint.OrbitEngine,
        overwrite: bool = True,
        asteroid_location: tuple = None,
    ):
        """Solve for the orbital elements an asteroid using previous
        observations.

        Parameters
        ----------
        solver_engine : OrbitEngine
            The orbital engine which the orbit solver will use.
        overwrite : bool, default = True
            Overwrite and replace the information of this class with the new
            values. If False, the returned solution is not also applied.
        asteroid_location : tuple, default = None
            The pixel location of the asteroid in the image. Defaults to the
            value provided at instantiation.

        Returns
        -------
        orbital_solution : OrbitSolution
            The orbit solution for the asteroid and image.

        Warning ..
            This requires that the astrometry solution be computed before-hand.
            This will not precompute automatically it without it being called
            explicitly, but it will instead return an error.
        """
        # A lot of this code re-implements of the methods for deriving the
        # record row; but this is to allow for the submission of a custom
        # asteroid location.

        # The orbital solution requires the astrometric solution to be
        # computed first.
        if not isinstance(self.astrometrics, astrometry.AstrometricSolution):
            raise error.SequentialOrderError(
                "The orbital solution requires an astrometric solution. The"
                " astrometric solution needs to be called and run first."
            )

        # If asteroid information is not provided, then nothing can be solved.
        # As there is no information.
        if self.asteroid_name is None:
            raise error.InputError(
                "The orbit of an asteroid cannot be solved as no asteroid name has been"
                " provided by which to fill in the MPC record."
            )
        else:
            # Ensuring there is no unintentional modification to the name.
            asteroid_name = copy.deepcopy(self.asteroid_name)
        if self.asteroid_history is None:
            raise error.InputError(
                "The orbit of an asteroid cannot be solved as no history of the orbit"
                " of the asteroid has been provided."
            )
        else:
            # Ensuring that the history of the asteroid does not change for
            # some reason.
            asteroid_history = copy.deepcopy(self.asteroid_history)

        # Using the defaults if an overriding value was not provided.
        asteroid_location = (
            self.asteroid_location if asteroid_location is None else asteroid_location
        )
        if asteroid_location is None:
            raise error.InputError(
                "The orbit of an asteroid cannot be solved as no asteroid location"
                " parameters have been provided."
            )
        else:
            # Splitting it up is easier notationally.
            asteroid_x, asteroid_y = asteroid_location
            # The location of the asteroid needs to be transformed to RA and DEC.
            asteroid_ra, asteroid_dec = self.astrometrics.pixel_to_sky_coordinates(
                x=asteroid_x, y=asteroid_y
            )

        # Use the current information to override the observation as specified
        # by the table just incase.
        mpc_table_row = self.mpc_table_row()
        mpc_table_row["minor_planet_number"] = asteroid_name
        mpc_table_row["ra"] = asteroid_ra
        mpc_table_row["dec"] = asteroid_dec

        # Convert this entry to a standard MPC record which to add to
        # historical data.
        current_mpc_record = library.mpcrecord.minor_planet_table_to_record(
            table=mpc_table_row
        )
        asteroid_record = asteroid_history + current_mpc_record

        # Solve for the orbital solution.
        orbital_solution = orbit.OrbitSolution(
            observation_record=asteroid_record, solver_engine=solver_engine
        )
        # Check if the solution should overwrite the current one.
        if overwrite:
            self.orbitals = orbital_solution
        else:
            # It should not overrite anything.
            pass
        return orbital_solution

    def solve_ephemeris(self, solver_engine, overwrite: bool = True):
        """Solve for the ephemeris solution an asteroid using previous
        observations and derived orbital elements.

        Parameters
        ----------
        solver_engine : EphemerisEngine
            The ephemeris engine which the ephemeris solver will use.
        overwrite : bool, default = True
            Overwrite and replace the information of this class with the new
            values. If False, the returned solution is not also applied.

        Returns
        -------
        ephemeritics_solution : EphemerisSolution
            The orbit solution for the asteroid and image.

        Warning ..
            This requires that the orbit solution be computed before-hand.
            This will not precompute automatically it without it being called
            explicitly, but it will instead return an error.
        """
        # The propagation solution requires the astrometric solution to be
        # computed first.
        if not isinstance(self.orbitals, orbit.OrbitSolution):
            raise error.SequentialOrderError(
                "The ephemeris solution requires an orbital solution. The"
                " orbital solution needs to be called and run first."
            )

        # TODO
        raise error.DevelopmentError("Not done yet.")

        # Check if the solution should overwrite the current one.
        if overwrite:
            self.ephemeritics = ephemeritics_solution
        else:
            # It should not overrite anything.
            pass
        return ephemeritics_solution

    def mpc_table_row(self) -> hint.Table:
        """An MPC table of the current observation with information provided
        by solved solutions. This routine does not attempt to do any solutions.

        Parameters
        ----------
        None

        Returns
        -------
        table_row : Astropy Table
            The MPC table of the information. It is a single row table.
        """
        # Using the table is a much cleaner way of doing this as the formatting
        # is already handled. A dictionary is the better way to establish
        # parameters and the eventual row.
        mpc_table = library.mpcrecord.minor_planet_blank_table()
        current_data = {}

        # Assuming the name is the MPC provisional number as is common.
        current_data["provisional_number"] = (
            self.asteroid_name if self.asteroid_name is not None else ""
        )

        # If this system is going to deal with provisional numbers is currently
        # beyond the design scope. May change in the future.
        current_data["provisional_number"] = ""

        # It is practically guaranteed that this observation is not the
        # discovery observation.
        current_data["discovery"] = False

        # Unknown publishing note, leaving it blank in lew of a better
        # solution.
        current_data["publishable_note"] = ""
        current_data["observing_note"] = ""

        # The data can be extracted from the UNIX time of observation.
        year, month, day = library.conversion.unix_time_to_decimal_day(
            unix_time=self.observing_time
        )
        current_data["year"] = year
        current_data["month"] = month
        current_data["day"] = day

        # RA and DEC are in degrees for both the table and the record so we
        # can just take it straight if the astrometric solution exists.
        if isinstance(self.astrometrics, astrometry.AstrometricSolution):
            if self.asteroid_location is not None:
                # Splitting it up is easier notationally.
                asteroid_x, asteroid_y = self.asteroid_location
            else:
                raise error.InputError(
                    "There is no asteroid location provided. An observational entry for"
                    " an asteroid cannot be made without the location of the asteroid."
                )
            # The location of the asteroid needs to be transformed to RA and DEC.
            asteroid_ra, asteroid_dec = self.astrometrics.pixel_to_sky_coordinates(
                x=asteroid_x, y=asteroid_y
            )
            current_data["ra"] = asteroid_ra
            current_data["dec"] = asteroid_dec
        else:
            # The astrometric solution does not exist. Currently there does not
            # seem to any obvious reason for why the MPC row is trying to be
            # created without astrometry.
            raise error.PracticalityError(
                "A MPC table row is trying to be derived without an astrometric"
                " solution being solved first. There is no use for an observation"
                " without astrometry."
            )

        # This is a blank region according to the specification. Although it
        # seems that some use it for something. Sparrow does not know what so
        # for now we will leave it blank.
        current_data["blank_1"] = ""

        # If there is photometric data, we can add that to the data record.
        if isinstance(self.photometrics, photometry.PhotometricSolution):
            magnitude = 0
            bandpass = self.photometrics.filter_name
        else:
            # There is no photometric solution so we cannot provide photometric
            # information.
            magnitude = np.nan
            bandpass = ""
        current_data["magnitude"] = magnitude
        current_data["bandpass"] = bandpass

        # This is another blank region according to the specification. Some
        # people use it; Sparrow
        current_data["blank_2"] = ""

        # The MPC observatory code. This is something that is specified in the
        # configuration file when this whole program is loaded.
        OBSERVATORY_CODE = library.config.MPC_OBSERVATORY_CODE
        current_data["observatory_code"] = OBSERVATORY_CODE

        # Adding the information to the MPC table and then compiling it to
        # a standard 80-character record.
        mpc_table.add_row(current_data)
        # Just incase and for documentation purposes.
        table_row = copy.deepcopy(mpc_table)
        return table_row

    def mpc_record_row(self) -> str:
        """Returns an 80-character record describing the observation of this
        object assuming it is an asteroid. It only uses information
        that is provided and does not attempt to compute any solutions.

        Parameters
        ----------
        None

        Returns
        -------
        record_row : str
            The 80-character record as determined by the MPC specification.
        """
        # Converting the current table record row to the standard 80-column
        # form.
        mpc_table_row = self.mpc_table_row()
        mpc_record = library.mpcrecord.minor_planet_table_to_record(table=mpc_table_row)
        # The string record is more important here, the library encases it in a
        # list as if it were a file.
        mpc_record_row = mpc_record[0]

        # As a sanity check.
        if len(mpc_record_row) != 80:
            raise error.DevelopmentError(
                "For some reason, this MPC record row is not exactly 80-characters."
            )
        return mpc_record_row
