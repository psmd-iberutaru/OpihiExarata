"""This is the class for a collection of solutions which the GUI interacts
with and acts as the complete solver. There is not engine as it just shuffles
the solutions."""

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
    observing_time : 
    asteroid_name : str
        The name of the asteroid. This is used to group similar observations
        and to also retrive data from the MPC. If this is None, then asteroid
        calculations are disabled as there is no asteroid.
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
        does include the current data. This is the table form of a MPC record.
        If this is None, then asteroid calculations are disabled as there is
        no asteroid.

    astrometrics : AstrometricSolution
        The astrometric solution; if it has not been solved yet, this is None.
    photometrics : PhotometricSolution
        The photometric solution; if it has not been solved yet, this is None.
    propagative : PropagationSolution
        The propagation solution; if it has not been solved yet, this is None.
    orbital : OrbitSolution
        The orbit solution; if it has not been solved yet, this is None.
    ephemeritic : EphemerisSolution
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
        data_array : array-like
            The image data from Opihi.
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

        # See if asteroids are important for this image and if so, lets
        # process the input data.
        if (
            asteroid_name is not None
            and asteroid_location is not None
            and asteroid_history is not None
        ):
            self.asteroid_name = asteroid_name
            self.asteroid_location = asteroid_location
            self.asteroid_history = asteroid_history
            # From the history, create the observational record table which other
            # processes use. This is the primary data that will be used.
            self.asteroid_observations = library.mpcrecord.minor_planet_record_to_table(
                records=asteroid_history
            )
        elif (
            asteroid_name is None
            or asteroid_location is None
            or asteroid_history is None
        ):
            # The proper asteroid values have not been provided. Asteroid
            # calculations are disabled.
            self.asteroid_name = None
            self.asteroid_location = None
            self.asteroid_history = None
            self.asteroid_observations = None
        else:
            raise error.LogicFlowError("The conditions for including or not including asteroid calculations were both not fulfilled. There is not third case.")

        # Just creating the initial placeholders for the solution.
        self.astrometrics = None
        self.photometrics = None
        self.propagative = None
        self.orbital = None
        self.ephemeritic = None
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
        photometric_solution : PhotometryEngine
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
        propagative_solution : PropagationEngine
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
        asteroid_x, asteroid_y = asteroid_location
        # The location of the asteroid needs to be transformed to RA and DEC.
        asteroid_ra, asteroid_dec = self.astrometrics.pixel_to_sky_coordinates(x=asteroid_x, y=asteroid_y)

        # Extracting historical information from which to calculate the 
        # propagation from.
        past_asteroid_ra = self.asteroid_observations["ra"]
        past_asteroid_dec = self.asteroid_observations["dec"]
        # Converting the decimal days to the required unix time. This function
        # seems to be vectorized to handle arrays.
        past_asteroid_time = library.conversion.decimal_day_to_unix_time(year=self.asteroid_observations["year"], month=self.asteroid_observations["month"], day=self.asteroid_observations["day"])
        # Propagation only works with really recent observations so we only 
        # include those done within some number of hours.
        EXPIRE_HOURS = library.config.OPIHI_PROPAGATION_OBSERVATION_EXPIRATION_HOURS
        EXPIRE_SECONDS = EXPIRE_HOURS * 3600
        valid_observation_index = np.where((asteroid_time - past_asteroid_time) <= EXPIRE_SECONDS, True, False)
        valid_past_asteroid_ra = past_asteroid_ra[valid_observation_index]
        valid_past_asteroid_dec = past_asteroid_dec[valid_observation_index]
        valid_past_asteroid_time = past_asteroid_time[valid_observation_index]

        # Add the current observation to the previous observations.
        asteroid_ra = np.append(valid_past_asteroid_ra, asteroid_ra)
        asteroid_dec = np.append(valid_past_asteroid_dec, asteroid_dec)
        asteroid_time = np.append(valid_past_asteroid_time, asteroid_time)

        # Computing the propagation solutions.
        propagative_solution = propagate.PropagationSolution(ra=asteroid_ra, dec=asteroid_dec, obs_time=asteroid_time, solver_engine=solver_engine)
        # See if the current propagation solution should be replaced.
        if overwrite:
            self.propagative = propagative_solution
        else:
            pass
        # All done.
        return propagative_solution
