"""This is the class for a collection of solutions which the GUI interacts
with and acts as the complete solver. There is not engine as it just shuffles
the solutions."""

import copy
import numpy as np

import opihiexarata.library as library
from opihiexarata.library import conversion
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

import opihiexarata.astrometry as astrometry
import opihiexarata.photometry as photometry
import opihiexarata.propagate as propagate
import opihiexarata.orbit as orbit
import opihiexarata.ephemeris as ephemeris


class OpihiSolution(library.engine.ExarataSolution):
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
        The time of observation, this is in Julian days.
    asteroid_name : str
        The name of the asteroid. This is used to group similar observations
        and to also retrieve data from the MPC.
    asteroid_location : tuple
        The pixel location of the asteroid. (Usually determined by a centroid
        around a user specified location.) If this is None, then asteroid
        calculations are disabled as there is no asteroid.
    asteroid_radius : float
        The pixel radius of the asteroid. This is used for aperture photometry.
    asteroid_history : list
        The total observational history of the asteroid provided. This includes
        previous observations done by Opihi and processed by OpihiExarata, but
        does not include the current data. This is the 80-column text file
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

    asteroid_magnitude : float
        The magnitude of the asteroid as determined by aperture photometry
        using the photometric solution. If there is no photometric solution,
        this is None.
    asteroid_magnitude_error : float
        The error of the magnitude, as propagated. If there is no photometric
        solution, this is None.


    astrometrics : AstrometricSolution
        The astrometric solution; if it has not been solved yet, this is None.
    photometrics : PhotometricSolution
        The photometric solution; if it has not been solved yet, this is None.
    orbitals : OrbitalSolution
        The orbit solution; if it has not been solved yet, this is None.
    ephemeritics : EphemeriticSolution
        The ephemeris solution; if it has not been solved yet, this is None.
    propagatives : PropagativeSolution
        The propagation solution; if it has not been solved yet, this is None.
    astrometrics_status : bool
        The status of the solving of the astrometric solution. It is True or
        False based on the success of the solve, None if a solve has not
        been attempted.
    photometrics_status : bool
        The status of the solving of the photometric solution. It is True or
        False based on the success of the solve, None if a solve has not
        been attempted.
    orbitals_status : bool
        The status of the solving of the orbital solution. It is True or
        False based on the success of the solve, None if a solve has not
        been attempted.
    ephemeritics_status : bool
        The status of the solving of the ephemeris solution. It is True or
        False based on the success of the solve, None if a solve has not
        been attempted.
    propagatives_status : bool
        The status of the solving of the propagative solution. It is True or
        False based on the success of the solve, None if a solve has not
        been attempted.
    astrometrics_engine_class : ExarataEngine
        The engine class used for the solving of the astrometric solution.
    photometrics_engine_class : ExarataEngine
        The engine class used for the solving of the photometric solution.
    orbitals_engine_class : ExarataEngine
        The engine class used for the solving of the orbital solution.
    ephemeritics_engine_class : ExarataEngine
        The engine class used for the solving of the ephemeritic solution.
    propagatives_engine_class : ExarataEngine
        The engine class used for the solving of the propagative solution.
    """

    # https://www.adsabs.harvard.edu/full/1895PA......3...17S

    def __init__(
        self,
        fits_filename: str,
        filter_name: str = None,
        exposure_time: float = None,
        observing_time: float = None,
        asteroid_name: str = None,
        asteroid_location: tuple[float, float] = None,
        asteroid_radius: float = None,
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
            The fits filename of which is the image which this solution is
            solving.
        filter_name : string, default=None
            The filter_name of the image which is contained within the data
            array. If None, we attempt to pull the value from the fits file.
        exposure_time : float, default=None
            The exposure time of the image, in seconds.
            If None, we attempt to pull the value from the fits file.
        observing_time : float, default=None
            The time of observation, this time must in Julian day.
            If None, we attempt to pull the value from the fits file.
        asteroid_name : str, default = None
            The name of the asteroid.
        asteroid_location : tuple, default = None
            The pixel location of the asteroid.
        asteroid_radius : float
            The pixel radius of the asteroid. This is used for aperture photometry.
        asteroid_history : list, default = None
            The history of observations of an asteroid written in a standard
            80-column MPC record.
        """
        # Collecting the initial instantiation data.
        self.fits_filename = fits_filename
        # Loading the fits file to record its data.
        header, data = library.fits.read_fits_image_file(filename=fits_filename)
        self.header = header
        self.data = data

        # If none of the metadata are provided, we try and get it from the
        # header file.
        if filter_name is None:
            filter_header_string = str(header["FWHL"])
            self.filter_name = library.conversion.filter_header_string_to_filter_name(
                header_string=filter_header_string
            )
        else:
            self.filter_name = filter_name
        if exposure_time is None:
            self.exposure_time = header["ITIME"]
        else:
            self.exposure_time = exposure_time
        if observing_time is None:
            self.observing_time = library.conversion.modified_julian_day_to_julian_day(
                mjd=header["MJD_OBS"]
            )
        else:
            self.observing_time = observing_time

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
        # Formatting the radius of the asteroid or the target in general.
        try:
            self.asteroid_radius = asteroid_radius
        except Exception:
            self.asteroid_radius = None
        # Formatting the historical locations of the asteroid or the target
        # in general.
        try:
            self.asteroid_history = asteroid_history
        except Exception:
            self.asteroid_history = None

        # Dummy values for asteroid photometry.
        self.asteroid_magnitude = None
        self.asteroid_magnitude_error = None

        # Just creating the initial placeholders for the solution.
        self.astrometrics = None
        self.photometrics = None
        self.orbitals = None
        self.ephemeritics = None
        self.propagatives = None
        # Status.
        self.astrometrics_status = None
        self.photometrics_status = None
        self.orbitals_status = None
        self.ephemeritics_status = None
        self.propagatives_status = None
        # Engines.
        self.astrometrics_engine_class = None
        self.photometrics_engine_class = None
        self.orbitals_engine_class = None
        self.ephemeritics_engine_class = None
        self.propagatives_engine_class = None
        return None

    # Asteroid observations table is based solely on the asteroid observation
    # list. If the list ever changes, so too does the observation table.
    def __get_asteroid_observations(self) -> hint.Table:
        """Property: get asteroid observation table.
        We derive the observation table from the asteroid history data.

        Parameters
        ----------
        None

        Returns
        -------
        asteroid_observations : Table
            The Astropy table which is a copy of the data in asteroid history.
        """
        # Deriving the observations from the table.
        try:
            asteroid_observations = library.mpcrecord.minor_planet_record_to_table(
                records=self.asteroid_history
            )
        except Exception:
            # Deriving the observations from the history failed.
            asteroid_observations = None
        return asteroid_observations

    def __set_asteroid_observations(self, value: hint.Any) -> None:
        """Property: set asteroid observation table.
        You cannot set the asteroid observations directly as it is determined
        from the asteroid history.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # The observations are derived from the table, it cannot be changed.
        raise error.ReadOnlyError(
            "The asteroid observation table is derived from the asteroid history"
            " attribute. The observation table itself cannot be changed unless the"
            " asteroid history list is changed."
        )
        return None

    def __del_asteroid_observations(self) -> None:
        """Property: delete asteroid observation table.
        The table cannot be deleted.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        raise error.ReadOnlyError(
            "The asteroid observation table is derived from the asteroid history"
            " attribute, it cannot be deleted."
        )
        return None

    asteroid_observations = property(
        __get_asteroid_observations,
        __set_asteroid_observations,
        __del_asteroid_observations,
    )

    def solve_astrometry(
        self,
        solver_engine: hint.AstrometryEngine,
        overwrite: bool = True,
        raise_on_error: bool = False,
        vehicle_args: dict = {},
    ) -> tuple[hint.AstrometricSolution, bool]:
        """Solve the image astrometry by using an astrometric engine.

        Parameters
        ----------
        solver_engine : AstrometryEngine
            The astrometric engine which the astrometry solver will use.
        overwrite : bool, default = True
            Overwrite and replace the information of this class with the new
            values. If False, the returned solution is not also applied.
        raise_on_error : bool, default = False
            If True, this disables the error handing and allows for errors from
            the solving engines/solutions to be propagated out.
        vehicle_args : dictionary, default = {}
            If the vehicle function for the provided solver engine needs
            extra parameters not otherwise provided by the standard input,
            they are given here.

        Returns
        -------
        astrometric_solution : AstrometricSolution
            The astrometry solution for the image.
        solve_status : bool
            The status of the solve. If True, the solving was successful.
        """
        try:
            astrometry_solution = astrometry.AstrometricSolution(
                fits_filename=self.fits_filename,
                solver_engine=solver_engine,
                vehicle_args=vehicle_args,
            )
        except Exception as _exception:
            # The solving failed.
            astrometry_solution = None
            solve_status = False
            # If the user wants a re-raised exception.
            if raise_on_error:
                raise _exception
        else:
            # The solving passed.
            solve_status = True
        finally:
            # Check if the solution should overwrite the current one.
            if overwrite:
                self.astrometrics = astrometry_solution
                self.astrometrics_status = solve_status
                self.astrometrics_engine_class = solver_engine
        return astrometry_solution, solve_status

    def solve_photometry(
        self,
        solver_engine: hint.PhotometryEngine,
        overwrite: bool = True,
        raise_on_error: bool = False,
        filter_name: str = None,
        exposure_time: float = None,
        vehicle_args: dict = {},
    ) -> tuple[hint.PhotometricSolution, bool]:
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
        raise_on_error : bool, default = False
            If True, this disables the error handing and allows for errors from
            the solving engines/solutions to be propagated out.
        vehicle_args : dictionary, default = {}
            If the vehicle function for the provided solver engine needs
            extra parameters not otherwise provided by the standard input,
            they are given here.

        Returns
        -------
        photometric_solution : PhotometrySolution
            The photometry solution for the image.
        solve_status : bool
            The status of the solve. If True, the solving was successful.

        Warning ..
            This requires that the astrometric solution be computed
            before-hand. It will not be precomputed automatically; without it
            being called explicitly, this will instead raise an error.
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
        try:
            photometric_solution = photometry.PhotometricSolution(
                fits_filename=self.fits_filename,
                solver_engine=solver_engine,
                astrometrics=self.astrometrics,
                filter_name=filter_name,
                exposure_time=exposure_time,
                vehicle_args=vehicle_args,
            )
        except Exception as _exception:
            # The solving failed.
            photometric_solution = None
            solve_status = False
            # If the user wants a re-raised exception.
            if raise_on_error:
                raise _exception
        else:
            # The solving passed.
            solve_status = True
        finally:
            # Check if the solution should overwrite the current one.
            if overwrite:
                # Overwriting the photometrics.
                self.photometrics = photometric_solution
                self.photometrics_status = solve_status
                self.photometrics_engine_class = solver_engine

        # If the solving completed properly, then we can attempt to solve for
        # the photometric magnitude of the target/asteroid. We do the
        # overwrite check here for simplicity. Of course, this only applies
        # if we have an asteroid location.
        if solve_status and self.asteroid_location is not None:
            __ = self.compute_asteroid_magnitude(overwrite=True)

        return photometric_solution, solve_status

    def solve_orbit(
        self,
        solver_engine: hint.OrbitEngine,
        overwrite: bool = True,
        raise_on_error: bool = False,
        asteroid_location: tuple = None,
        vehicle_args: dict = {},
    ) -> tuple[hint.OrbitalSolution, bool]:
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
        raise_on_error : bool, default = False
            If True, this disables the error handing and allows for errors from
            the solving engines/solutions to be propagated out.
        vehicle_args : dictionary, default = {}
            If the vehicle function for the provided solver engine needs
            extra parameters not otherwise provided by the standard input,
            they are given here.

        Returns
        -------
        orbital_solution : OrbitalSolution
            The orbit solution for the asteroid and image.
        solve_status : bool
            The status of the solve. If True, the solving was successful.

        Warning ..
            This requires that the astrometric solution be computed
            before-hand. It will not be precomputed automatically; without it
            being called explicitly, this will instead raise an error.
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

        # Check that the proper asteroid information has been provided. If
        # the orbit defined is custom however, these checks should be skipped.
        if issubclass(solver_engine, orbit.CustomOrbitEngine):
            asteroid_name = "custom"
            asteroid_history = []
        else:
            # Ensuring there is no unintentional modification to the name
            # or history.
            asteroid_name = copy.deepcopy(self.asteroid_name)
            asteroid_history = copy.deepcopy(self.asteroid_history)
        # If asteroid information is not provided, then nothing can be solved.
        # As there is no information.
        if asteroid_name is None:
            raise error.InputError(
                "The orbit of an asteroid cannot be solved as no asteroid name has been"
                " provided by which to fill in the MPC record."
            )
        if asteroid_history is None:
            raise error.InputError(
                "The orbit of an asteroid cannot be solved as no history of the orbit"
                " of the asteroid has been provided."
            )

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
            # Splitting is nicer on the notational side.
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
        # Adding the magnitude entry, because why not.
        if isinstance(self.asteroid_magnitude, (int, float)):
            mpc_table_row["magnitude"] = self.asteroid_magnitude
            mpc_table_row["bandpass"] = self.filter_name

        # Convert this entry to a standard MPC record which to add to
        # historical data.
        current_mpc_record = library.mpcrecord.minor_planet_table_to_record(
            table=mpc_table_row
        )
        asteroid_record = asteroid_history + current_mpc_record
        # Clean up the record.
        asteroid_record = library.mpcrecord.clean_minor_planet_record(records=asteroid_record)

        # Solve for the orbital solution.
        try:
            orbital_solution = orbit.OrbitalSolution(
                observation_record=asteroid_record,
                solver_engine=solver_engine,
                vehicle_args=vehicle_args,
            )
        except Exception as _exception:
            # The solve failed.
            orbital_solution = None
            solve_status = False
            # If the user wants a re-raised exception.
            if raise_on_error:
                raise _exception
        else:
            # The solve worked okay.
            solve_status = True
        finally:
            # Check if the solution should overwrite the current one.
            if overwrite:
                self.orbitals = orbital_solution
                self.orbitals_status = solve_status
                self.orbitals_engine_class = solver_engine
        return orbital_solution, solve_status

    def solve_ephemeris(
        self,
        solver_engine: hint.EphemerisEngine,
        overwrite: bool = True,
        raise_on_error: bool = False,
        vehicle_args: dict = {},
    ) -> tuple[hint.EphemeriticSolution, bool]:
        """Solve for the ephemeris solution an asteroid using previous
        observations and derived orbital elements.

        Parameters
        ----------
        solver_engine : EphemerisEngine
            The ephemeris engine which the ephemeris solver will use.
        overwrite : bool, default = True
            Overwrite and replace the information of this class with the new
            values. If False, the returned solution is not also applied.
        raise_on_error : bool, default = False
            If True, this disables the error handing and allows for errors from
            the solving engines/solutions to be propagated out.
        vehicle_args : dictionary, default = {}
            If the vehicle function for the provided solver engine needs
            extra parameters not otherwise provided by the standard input,
            they are given here.

        Returns
        -------
        ephemeritics_solution : EphemeriticSolution
            The orbit solution for the asteroid and image.
        solve_status : bool
            The status of the solve. If True, the solving was successful.

        Warning ..
            This requires that the orbital solution be computed
            before-hand. It will not be precomputed automatically; without it
            being called explicitly, this will instead raise an error.
        """
        # The propagation solution requires the astrometric solution to be
        # computed first.
        if not isinstance(self.orbitals, orbit.OrbitalSolution):
            raise error.SequentialOrderError(
                "The ephemeris solution requires an orbital solution. The"
                " orbital solution needs to be called and run first."
            )

        # Computing the ephemeris solution provided the engine that the
        # user wants to use.
        try:
            ephemeritics_solution = ephemeris.EphemeriticSolution(
                orbitals=self.orbitals,
                solver_engine=solver_engine,
                vehicle_args=vehicle_args,
            )
        except Exception as _exception:
            # The solve failed.
            ephemeritics_solution = None
            solve_status = False
            # If the user wants a re-raised exception.
            if raise_on_error:
                raise _exception
        else:
            # The solve passed file.
            solve_status = True
        finally:
            # Check if the solution should overwrite the current one.
            if overwrite:
                self.ephemeritics = ephemeritics_solution
                self.ephemeritics_status = solve_status
                self.ephemeritics_engine_class = solver_engine
        # All done.
        return ephemeritics_solution, solve_status

    def solve_propagate(
        self,
        solver_engine: hint.PropagationEngine,
        overwrite: bool = True,
        raise_on_error: bool = False,
        asteroid_location: tuple[float, float] = None,
        vehicle_args: dict = {},
    ) -> tuple[hint.PropagativeSolution, bool]:
        """Solve for the location of an asteroid using a method of propagation.

        Parameters
        ----------
        solver_engine : PropagationEngine
            The propagative engine which the propagation solver will use.
        overwrite : bool, default = True
            Overwrite and replace the information of this class with the new
            values. If False, the returned solution is not also applied.
        asteroid_location : tuple, default = None
            The pixel location of the asteroid in the image. Defaults to the
            value provided at instantiation.
        raise_on_error : bool, default = False
            If True, this disables the error handing and allows for errors from
            the solving engines/solutions to be propagated out.
        vehicle_args : dictionary, default = {}
            If the vehicle function for the provided solver engine needs
            extra parameters not otherwise provided by the standard input,
            they are given here.

        Returns
        -------
        propagative_solution : PropagativeSolution
            The propagation solution for the asteroid and image.
        solve_status : bool
            The status of the solve. If True, the solving was successful.

        Warning ..
            This requires that the astrometric solution be computed
            before-hand. It will not be precomputed automatically; without it
            being called explicitly, this will instead raise an error.
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
            # Splitting it up is easier notionally.
            asteroid_x, asteroid_y = asteroid_location
            # The location of the asteroid needs to be transformed to RA and DEC.
            asteroid_ra, asteroid_dec = self.astrometrics.pixel_to_sky_coordinates(
                x=asteroid_x, y=asteroid_y
            )

        # Extracting historical information from which to calculate the
        # propagation from.
        past_asteroid_ra = self.asteroid_observations["ra"]
        past_asteroid_dec = self.asteroid_observations["dec"]
        # Converting the decimal days to the required Julian day time. This
        # function seems to be vectorized to handle arrays.
        past_asteroid_time = library.conversion.decimal_day_to_julian_day(
            year=self.asteroid_observations["year"],
            month=self.asteroid_observations["month"],
            day=self.asteroid_observations["day"],
        )
        # As arrays.
        past_asteroid_ra = np.asarray(past_asteroid_ra, dtype=float)
        past_asteroid_dec = np.asarray(past_asteroid_dec, dtype=float)
        past_asteroid_time = np.asarray(past_asteroid_time, dtype=float)
        # Propagation only works with really recent observations so we only
        # include those done within some number of hours. The Julian day system
        # is in days.
        EXPIRE_HOURS = (
            library.config.OPIHISOLUTION_PROPAGATION_OBSERVATION_EXPIRATION_HOURS
        )
        EXPIRE_DAYS = EXPIRE_HOURS / 24
        valid_observation_index = np.where(
            (asteroid_time - past_asteroid_time) <= EXPIRE_DAYS, True, False
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

        # Computing the propagation solution.
        try:
            propagative_solution = propagate.PropagativeSolution(
                ra=asteroid_ra,
                dec=asteroid_dec,
                obs_time=asteroid_time,
                solver_engine=solver_engine,
                vehicle_args=vehicle_args,
            )
        except Exception as _exception:
            # The solving failed.
            propagative_solution = None
            solve_status = False
            # If the user wants a re-raised exception.
            if raise_on_error:
                raise _exception
        else:
            # The solving was completed.
            solve_status = True
        finally:
            # See if the current propagation solution should be replaced.
            if overwrite:
                self.propagatives = propagative_solution
                self.propagatives_status = solve_status
                self.propagatives_engine_class = solver_engine
        # All done.
        return propagative_solution, solve_status

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
        mpc_table = library.mpcrecord.blank_minor_planet_table()
        current_data = {}

        # If this system is going to deal with provisional numbers is currently
        # beyond the design scope. May change in the future.
        current_data["minor_planet_number"] = ""

        # Assuming the name is the MPC provisional number as is common.
        current_data["provisional_number"] = (
            self.asteroid_name if self.asteroid_name is not None else ""
        )

        # It is practically guaranteed that this observation is not the
        # discovery observation.
        current_data["discovery"] = False

        # Unknown publishing note, leaving it blank in lew of a better
        # solution.
        current_data["publishable_note"] = ""
        current_data["observing_note"] = ""

        # The data can be extracted from the Julian day time of observation.
        year, month, day = library.conversion.julian_day_to_decimal_day(
            jd=self.observing_time
        )
        current_data["year"] = year
        current_data["month"] = month
        current_data["day"] = day

        # RA and DEC are in degrees for both the table and the record so we
        # can just take it straight if the astrometric solution exists.
        if isinstance(self.astrometrics, astrometry.AstrometricSolution):
            if self.asteroid_location is not None:
                # Splitting it up is easier on the notation.
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
                " solution being solved first. An observation cannot be recorded"
                " without an astrometric solution."
            )

        # This is a blank region according to the specification. Although it
        # seems that some use it for something. Sparrow does not know what so
        # for now we will leave it blank.
        current_data["blank_1"] = ""

        # If there is photometric data, we can add that to the data record.
        if isinstance(self.photometrics, photometry.PhotometricSolution):
            magnitude = self.asteroid_magnitude
            bandpass = self.photometrics.filter_name
        else:
            # There is no photometric solution so we cannot provide photometric
            # information.
            magnitude = np.nan
            bandpass = ""
        current_data["magnitude"] = magnitude
        current_data["bandpass"] = bandpass

        # This is another blank region according to the specification. Some
        # people use it; Sparrow does not know what to do with it.
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

    def mpc_record_full(self) -> list[str]:
        """This creates a full MPC record from all observations, including the
        history and this current observation.

        Parameters
        ----------
        None

        Returns
        -------
        mpc_record : list
            The MPC record as a list where each entry is a row.
        """
        # Extract the historical information that was picked up. We do not
        # want to mess up the history itself just in case.
        if self.asteroid_history is None:
            # No history has been provided, but the current record may still
            # exist to give results.
            asteroid_history = []
        else:
            asteroid_history = copy.deepcopy(self.asteroid_history)
        # Extracting the current observational record.
        try:
            asteroid_current = [self.mpc_record_row()]
        except error.PracticalityError:
            # The MPC row could not be derived because the lack of data
            # (typically the lack of an astrometric solution.)
            asteroid_current = []

        # Combining the two.
        mpc_record = asteroid_history + asteroid_current
        return mpc_record

    def compute_asteroid_magnitude(
        self, asteroid_location: tuple = None, overwrite: bool = True
    ) -> tuple[float, float]:
        """This function computes the asteroid magnitude provided the location
        of the asteroid. This requires an asteroid location and a
        PhotometricSolution.

        Parameters
        ----------
        asteroid_location : tuple, default = None
            The pixel location of the asteroid. If None, we default to using
            the current asteroid location stored in this instance.
        overwrite : bool, default = True
            Overwrite and replace the information of this class with the new
            values. If False, we only return the values and do not overwrite
            the data in this class.

        Returns
        -------
        magnitude, float
            The magnitude of the asteroid as computed by the photometric
            solution.
        magnitude_error, float
            The magnitude error of the asteroid as computed by the photometric
            solution.
        """
        # We need to determine which set of asteroid locations to use.
        if asteroid_location is not None:
            asteroid_location = asteroid_location
        else:
            # No information was provided, using the instances's own.
            if self.asteroid_location is not None:
                asteroid_location = self.asteroid_location
            else:
                raise error.InputError(
                    "No asteroid location has been provided and there is no asteroid"
                    " location in this instance. A magnitude cannot be computed."
                )
        # Determine if we even have the photometric solution to do it.
        if self.photometrics_status and isinstance(
            self.photometrics, photometry.PhotometricSolution
        ):
            # All good.
            pass
        else:
            raise error.SequentialOrderError(
                "In order to determine the magnitude of an asteroid, a photometric"
                " solution must exist. None currently does."
            )

        # Using the photometric solution and the asteroid location...
        asteroid_x, asteroid_y = self.asteroid_location
        (
            magnitude,
            magnitude_error,
        ) = self.photometrics.calculate_star_aperture_magnitude(
            pixel_x=asteroid_x, pixel_y=asteroid_y
        )
        # If the user wanted us to overwrite the data.
        if overwrite:
            self.asteroid_magnitude = magnitude
            self.asteroid_magnitude_error = magnitude_error
        return magnitude, magnitude_error

    def save_to_fits_file(self, filename: str, overwrite: bool = False) -> None:
        """We save all of the information that we can from this solution to
        a FITS file.

        Parameters
        ----------
        filename : string
            The name of the fits file to save all of this data to.
        overwrite : bool, default = False
            If True, this overwrites the file if there is a conflict.

        Returns
        -------
        None
        """
        # The data and the header to save the data as.
        raw_header = self.header
        data = self.data

        # Information which is contained within the solutions of OpihiExarata
        # should also be save via the header file. We extract the parameters
        # where we are able to.
        try:
            available_entries = self._generate_opihiexarata_fits_entries_dictionary()
            updated_header = library.fits.update_opihiexarata_fits_header(
                header=raw_header, entries=available_entries
            )
        except error.InputError:
            raise error.DevelopmentError(
                "The OpihiSolution generated FITS header dictionary does not conform to"
                " the standards expected by the OpihiExarata FITS library function."
                " Something out of sync."
            )

        # Applying the WCS solution. The WCS obeys specific header keyword 
        # conventions so we cannot process it as an OpihiExarata FITS entry
        # but we still group it so it is still within the OX set.
        if isinstance(self.astrometrics, astrometry.AstrometricSolution):
            wcs_header = self.astrometrics.wcs.to_header()
            for carddex in wcs_header.cards:
                updated_header.insert("OXW__END", carddex, after=False)

        # Saving the file.
        library.fits.write_fits_image_file(
            filename=filename, header=updated_header, data=data, overwrite=overwrite
        )
        # All done.
        return None

    def _generate_opihiexarata_fits_entries_dictionary(self):
        """We determine the OpihiExarata header entries here. We follow the
        specification for the OpihiExarata FITS header. We only add values
        which we have proper data for to the dictionary.

        Parameters
        ----------
        None

        Returns
        -------
        available_entries : dict
            The available entries which there exists
        """
        # Initial beginning.
        available_entries = {}

        # We are processing the data.
        available_entries["OX_BEGIN"] = True

        # Target/asteroid information.
        if self.asteroid_name is not None:
            # If the name was provided.
            available_entries["OXT_NAME"] = self.asteroid_name
        if self.asteroid_location is not None:
            # The pixel location.
            target_x, target_y = self.asteroid_location
            available_entries["OXT_PX_X"] = target_x
            available_entries["OXT_PX_Y"] = target_y
            # If a valid astrometric solution exists, we can also get the
            # RA and DEC.
            if self.astrometrics_status and isinstance(
                self.astrometrics, astrometry.AstrometricSolution
            ):
                (
                    target_ra_deg,
                    target_dec_deg,
                ) = self.astrometrics.pixel_to_sky_coordinates(x=target_x, y=target_y)
                # Converting to sexagesimal as is typical for FITS files.
                (
                    target_ra_sex,
                    target_dec_sex,
                ) = library.conversion.degrees_to_sexagesimal_ra_dec(
                    ra_deg=target_ra_deg, dec_deg=target_dec_deg
                )
                available_entries["OXT___RA"] = target_ra_sex
                available_entries["OXT__DEC"] = target_dec_sex

            # The magnitude and error of the target, as determined by a
            # photometric solution. Requires the asteroid location and a
            # photometric solution.
            if self.photometrics_status and isinstance(
                self.photometrics, photometry.PhotometricSolution
            ):
                # The photometric solution exists and the magnitude and error
                # has likely been calculated. However, sometimes the
                # magnitude was not properly calculated because of the
                # asteroid location.
                if np.isfinite(self.asteroid_magnitude) and np.isfinite(
                    self.asteroid_magnitude_error
                ):
                    available_entries["OXT__MAG"] = self.asteroid_magnitude
                    available_entries["OXT_MAGE"] = self.asteroid_magnitude_error
                else:
                    # The target magnitude was improperly calculated.
                    available_entries["OXT__MAG"] = None
                    available_entries["OXT_MAGE"] = None

        # Metadata information.
        available_entries["OXM_ORFN"] = library.path.get_filename_with_extension(
            pathname=self.fits_filename
        )
        # We can never know if this was preprocessed or not.

        # Astrometric information.
        available_entries["OXA_SLVD"] = self.astrometrics_status
        if self.astrometrics_status and isinstance(
            self.astrometrics, astrometry.AstrometricSolution
        ):
            # The engine.
            available_entries["OXA__ENG"] = self.astrometrics_engine_class.__name__
            # And the results.
            (
                center_ra_sex,
                center_dec_sex,
            ) = library.conversion.degrees_to_sexagesimal_ra_dec(
                ra_deg=self.astrometrics.ra, dec_deg=self.astrometrics.dec
            )
            available_entries["OXA___RA"] = center_ra_sex
            available_entries["OXA__DEC"] = center_dec_sex
            available_entries["OXA_ANGL"] = self.astrometrics.orientation
            available_entries["OXA_RADI"] = self.astrometrics.radius
            available_entries["OXA_PXSC"] = self.astrometrics.pixel_scale

        # Photometric information.
        available_entries["OXP_SLVD"] = self.photometrics_status
        if self.photometrics_status and isinstance(
            self.photometrics, photometry.PhotometricSolution
        ):
            # The engine.
            available_entries["OXP__ENG"] = self.photometrics_engine_class.__name__
            # And the results.
            available_entries["OXPSKYCT"] = self.photometrics.sky_counts
            available_entries["OXP_APTR"] = self.photometrics.aperture_radius
            available_entries["OXP_ZP_M"] = self.photometrics.zero_point
            available_entries["OXP_ZP_E"] = self.photometrics.zero_point_error
        # These do not depend on a photometric solution itself but it is
        # photometrically related.
        available_entries["OXP_FILT"] = self.filter_name

        # Orbital element information.
        available_entries["OXO_SLVD"] = self.orbitals_status
        if self.orbitals_status and isinstance(self.orbitals, orbit.OrbitalSolution):
            # The engine.
            available_entries["OXO__ENG"] = self.orbitals_engine_class.__name__
            # The solved or derived values.
            available_entries["OXO_SM_S"] = self.orbitals.semimajor_axis
            available_entries["OXO_EC_S"] = self.orbitals.eccentricity
            available_entries["OXO_IN_S"] = self.orbitals.inclination
            available_entries["OXO_AN_S"] = self.orbitals.longitude_ascending_node
            available_entries["OXO_PH_S"] = self.orbitals.argument_perihelion
            available_entries["OXO_MA_S"] = self.orbitals.mean_anomaly
            available_entries["OXO_EA_D"] = self.orbitals.eccentric_anomaly
            available_entries["OXO_TA_D"] = self.orbitals.true_anomaly
            # ...and their errors.
            available_entries["OXO_SM_E"] = self.orbitals.semimajor_axis_error
            available_entries["OXO_EC_E"] = self.orbitals.eccentricity_error
            available_entries["OXO_IN_E"] = self.orbitals.inclination_error
            available_entries["OXO_AN_E"] = self.orbitals.longitude_ascending_node_error
            available_entries["OXO_PH_E"] = self.orbitals.argument_perihelion_error
            available_entries["OXO_MA_E"] = self.orbitals.mean_anomaly_error
            available_entries["OXO_EA_E"] = self.orbitals.eccentric_anomaly_error
            available_entries["OXO_TA_E"] = self.orbitals.true_anomaly_error
            # The epoch.
            available_entries["OXO_EPCH"] = self.orbitals.epoch_julian_day

        # Ephemeris information.
        available_entries["OXE_SLVD"] = self.ephemeritics_status
        if self.ephemeritics_status and isinstance(
            self.ephemeritics, ephemeris.EphemeriticSolution
        ):
            # The engine.
            available_entries["OXE__ENG"] = self.ephemeritics_engine_class.__name__
            # The results, and a function to convert between the two,
            # shorthanded. This works for both because the unit of time is the
            # same for both conversions.
            deg2as = (
                lambda d: library.conversion.degrees_per_second_to_arcsec_per_second(
                    degree_per_second=d
                )
            )
            available_entries["OXE_RA_V"] = deg2as(d=self.ephemeritics.ra_velocity)
            available_entries["OXE_DECV"] = deg2as(d=self.ephemeritics.dec_velocity)
            available_entries["OXE_RA_A"] = deg2as(d=self.ephemeritics.ra_acceleration)
            available_entries["OXE_DECA"] = deg2as(d=self.ephemeritics.dec_acceleration)

        # Propagation information.
        available_entries["OXR_SLVD"] = self.propagatives_status
        if self.propagatives_status and isinstance(
            self.propagatives, propagate.PropagativeSolution
        ):
            # The engine.
            available_entries["OXR__ENG"] = self.propagatives_engine_class.__name__
            # The results, and a function to convert between the two,
            # shorthanded. This works for both because the unit of time is the
            # same for both conversions.
            deg2as = (
                lambda d: library.conversion.degrees_per_second_to_arcsec_per_second(
                    degree_per_second=d
                )
            )
            available_entries["OXR_RA_V"] = deg2as(d=self.propagatives.ra_velocity)
            available_entries["OXR_DECV"] = deg2as(d=self.propagatives.dec_velocity)
            available_entries["OXR_RA_A"] = deg2as(d=self.propagatives.ra_acceleration)
            available_entries["OXR_DECA"] = deg2as(d=self.propagatives.dec_acceleration)


        # We also add WCS header information from the astrometric solution,
        # if it exists. We have it here at the end to ensure that the 
        # many non-conventional header keys are group together and do not 
        # interfere with the more common conventional endings.
        # We use these tags to ensure its placement later.
        available_entries["OXWBEGIN"] = ""
        available_entries["OXW__END"] = ""

        # The ending part.
        available_entries["OX___END"] = True

        # All done.
        return available_entries
