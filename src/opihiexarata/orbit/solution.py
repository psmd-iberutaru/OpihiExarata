"""The orbit solution class."""

import numpy as np
import scipy.optimize as sp_optimize


import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

import opihiexarata.orbit as orbit


class OrbitalSolution(library.engine.ExarataSolution):
    """This is the class which solves a record of observations to derive the
    orbital parameters of asteroids or objects in general. A record of
    observations must be provided.

    Attributes
    ----------
    semimajor_axis : float
        The semi-major axis of the orbit solved, in AU.
    semimajor_axis_error : float
        The error on the semi-major axis of the orbit solved, in AU.
    eccentricity : float
        The eccentricity of the orbit solved.
    eccentricity_error : float
        The error on the eccentricity of the orbit solved.
    inclination : float
        The angle of inclination of the orbit solved, in degrees.
    inclination_error : float
        The error on the angle of inclination of the orbit solved, in degrees.
    longitude_ascending_node : float
        The longitude of the ascending node of the orbit solved, in degrees.
    longitude_ascending_node_error : float
        The error on the longitude of the ascending node of the orbit solved, in degrees.
    argument_perihelion : float
        The argument of perihelion of the orbit solved, in degrees.
    argument_perihelion_error : float
        The error on the argument of perihelion of the orbit solved, in degrees.
    mean_anomaly : float
        The mean anomaly of the orbit solved, in degrees.
    mean_anomaly_error : float
        The error on the mean anomaly of the orbit solved, in degrees.
    true_anomaly : float
        The true anomaly of the orbit solved, in degrees. This value is
        calculated from the mean anomaly.
    true_anomaly_error : float
        The error on the true anomaly of the orbit solved, in degrees. This
        value is calculated from the error on the mean anomaly.
    epoch_julian_day : float
        The epoch where for these osculating orbital elements. This value is
        in Julian days.
    """

    def __init__(
        self,
        observation_record: list[str],
        solver_engine: hint.OrbitEngine,
        vehicle_args: dict = {},
    ) -> None:
        """The initialization function. Provided the list of observations,
        solves the orbit for the Keplarian orbits.

        Parameters
        ----------
        observation_record : list
            A list of the standard MPC 80-column observation records. Each
            element of the list should be a string representing the observation.
        solver_engine : OrbitEngine
            The engine which will be used to complete the orbital elements
            from the observation record.
        vehicle_args : dictionary
            If the vehicle function for the provided solver engine needs
            extra arguments not otherwise provided by the standard input,
            they are given here.

        Returns
        -------
        None
        """
        # Check that the solver engine is a valid submission, that is is an
        # expected engine class.
        if isinstance(solver_engine, library.engine.OrbitEngine):
            raise error.EngineError(
                "The orbit solver engine provided should be the engine class"
                " itself, not an instance thereof."
            )
        elif issubclass(solver_engine, library.engine.OrbitEngine):
            # It is fine, the user submitted a valid orbit engine.
            pass
        else:
            raise error.EngineError(
                "The provided orbit engine is not a valid engine which can be"
                " used for orbit solutions."
            )

        # Derive the orbital elements using the proper vehicle function for
        # the desired engine is that is to be used.
        if issubclass(solver_engine, orbit.OrbfitOrbitDeterminerEngine):
            # Solve using Orbfit.
            raw_orbit_results = _vehicle_orbfit_orbit_determiner(
                observation_record=observation_record
            )
        elif issubclass(solver_engine, orbit.CustomOrbitEngine):
            # A custom orbit has been desired, the vehicle function arguments
            # contain the values needed.
            raw_orbit_results = _vehicle_custom_orbit(
                observation_record=observation_record, vehicle_args=vehicle_args
            )
        else:
            # There is no vehicle function, the engine is not supported.
            raise error.EngineError(
                "The provided orbit engine `{eng}` is not supported, there is no"
                " associated vehicle function for it.".format(eng=str(solver_engine))
            )

        # Sanity check on the dictionary-like return.
        if not isinstance(raw_orbit_results, dict):
            raise error.DevelopmentError(
                "The results of the orbit engines should be a dictionary. The orbit"
                " engine used, and the subsequent vehicle function: {engtype}".format(
                    engtype=solver_engine
                )
            )
        else:
            # Quick type checking; everything should be float or at the least
            # float-convertible. This may be unneeded but it does not hurt.
            orbit_results = {
                keydex: float(valuedex)
                for keydex, valuedex in raw_orbit_results.items()
            }

        # Extract the needed values from the results of the engine.
        try:
            # Semimajor
            self.semimajor_axis = orbit_results["semimajor_axis"]
            self.semimajor_axis_error = orbit_results["semimajor_axis_error"]
            # Eccentricity
            self.eccentricity = orbit_results["eccentricity"]
            self.eccentricity_error = orbit_results["eccentricity_error"]
            # Inclination
            self.inclination = orbit_results["inclination"]
            self.inclination_error = orbit_results["inclination_error"]
            # Longitude
            self.longitude_ascending_node = orbit_results["longitude_ascending_node"]
            self.longitude_ascending_node_error = orbit_results[
                "longitude_ascending_node_error"
            ]
            # Perihelion
            self.argument_perihelion = orbit_results["argument_perihelion"]
            self.argument_perihelion_error = orbit_results["argument_perihelion_error"]
            # Mean anomaly
            self.mean_anomaly = orbit_results["mean_anomaly"]
            self.mean_anomaly_error = orbit_results["mean_anomaly_error"]
            # MJD
            self.epoch_julian_day = orbit_results["epoch_julian_day"]
        except KeyError:
            raise error.EngineError(
                "The engine results provided are insufficient for this orbit"
                " solver. Either the engine cannot be used because it cannot provide"
                " the needed results, or the vehicle function does not pull the"
                " required results from the engine."
            )

        # Calculating the eccentric anomaly and error from the provided values.
        (
            eccentric_anomaly,
            eccentric_anomaly_error,
        ) = self.__calculate_eccentric_anomaly()
        self.eccentric_anomaly = eccentric_anomaly
        self.eccentric_anomaly_error = eccentric_anomaly_error

        # Calculating the true anomaly and error from the provided values.
        true_anomaly, true_anomaly_error = self.__calculate_true_anomaly()
        self.true_anomaly = true_anomaly
        self.true_anomaly_error = true_anomaly_error

        # All done.
        return None

    def __calculate_eccentric_anomaly(self) -> tuple[float, float]:
        """Calculating the eccentric anomaly and error from the mean anomaly.

        Parameters
        ----------
        None

        Returns
        -------
        eccentric_anomaly : float
            The eccentric anomaly as derived from the mean anomaly.
        eccentric_anomaly_error : float
            The eccentric anomaly error derived as an average from the upper
            and lower ranges of the mean anomaly.
        """
        # Needed orbital values.
        eccentricity = self.eccentricity
        mean_anomaly = self.mean_anomaly
        mean_anomaly_error = self.mean_anomaly_error
        # Calculating the eccentric anomaly.
        eccentric_anomaly = _calculate_eccentric_anomaly(
            mean_anomaly=mean_anomaly, eccentricity=eccentricity
        )
        # And the error using upper and lower bound method.
        lower_eccentric_anomaly = _calculate_eccentric_anomaly(
            mean_anomaly=mean_anomaly - mean_anomaly_error, eccentricity=eccentricity
        )
        upper_eccentric_anomaly = _calculate_eccentric_anomaly(
            mean_anomaly=mean_anomaly + mean_anomaly_error, eccentricity=eccentricity
        )
        bounds_eccentric_anomaly = np.array(
            [lower_eccentric_anomaly, upper_eccentric_anomaly], dtype=float
        )
        eccentric_anomaly_error = np.mean(
            np.abs(bounds_eccentric_anomaly - eccentric_anomaly)
        )
        return eccentric_anomaly, eccentric_anomaly_error

    def __calculate_true_anomaly(self) -> tuple[float, float]:
        """Calculating the true anomaly and error from the eccentric anomaly.

        Parameters
        ----------
        None

        Returns
        -------
        true_anomaly : float
            The true anomaly as derived from the mean anomaly.
        true_anomaly_error : float
            The true anomaly error derived as an average from the upper
            and lower ranges of the eccentric anomaly.
        """
        # Needed orbital values.
        eccentricity = self.eccentricity
        eccentric_anomaly = self.eccentric_anomaly
        eccentric_anomaly_error = self.eccentric_anomaly_error
        # Calculating the eccentric anomaly.
        true_anomaly = _calculate_true_anomaly(
            eccentric_anomaly=eccentric_anomaly, eccentricity=eccentricity
        )
        # And the error using upper and lower bound method.
        lower_true_anomaly = _calculate_true_anomaly(
            eccentric_anomaly=eccentric_anomaly - eccentric_anomaly_error,
            eccentricity=eccentricity,
        )
        upper_true_anomaly = _calculate_true_anomaly(
            eccentric_anomaly=eccentric_anomaly + eccentric_anomaly_error,
            eccentricity=eccentricity,
        )
        bounds_true_anomaly = np.array(
            [lower_true_anomaly, upper_true_anomaly], dtype=float
        )
        true_anomaly_error = np.mean(np.abs(bounds_true_anomaly - true_anomaly))
        return true_anomaly, true_anomaly_error


def _calculate_eccentric_anomaly(mean_anomaly: float, eccentricity: float) -> float:
    """Calculate the eccentric anomaly from the mean anomaly and eccentricity
    of an orbit. This is found iteratively using Newton's method.

    Parameters
    ----------
    mean_anomaly : float
        The mean anomaly of the orbit, in degrees.

    Returns
    -------
    eccentric_anomaly : float
        The eccentric anomaly as derived from the mean anomaly, in degrees.
    """
    # Converting first to radians.
    radian_mean_anomaly = mean_anomaly * (np.pi / 180)
    # The main equation to solve using the root finding algorithm; as derived
    # from Kepler's equation.
    def root_kepler_equation(ecc_ano=0, mean_ano=0, eccen=0):
        return ecc_ano - eccen * np.sin(ecc_ano) - mean_ano

    def root_kepler_equation_prime(ecc_ano=0, mean_ano=0, eccen=0):
        return 1 - eccen * np.cos(ecc_ano)

    # Initial guess. High eccentricities are better served by a different
    # initial guess than the native one.
    if eccentricity <= 0.7:
        initial_guess = radian_mean_anomaly
    else:
        initial_guess = np.pi

    # Using the root finding algorithm to find the eccentric anomaly.
    root_results = sp_optimize.root_scalar(
        f=lambda ec_an: root_kepler_equation(
            ecc_ano=ec_an, mean_ano=radian_mean_anomaly, eccen=eccentricity
        ),
        fprime=lambda ec_an: root_kepler_equation_prime(
            ecc_ano=ec_an, mean_ano=radian_mean_anomaly, eccen=eccentricity
        ),
        method="newton",
        x0=initial_guess,
    )
    # Scipy gives a class back rather than just a tuple of values. Who knows
    # why.
    radian_eccentric_anomaly = root_results.root
    # Converting back to degrees.
    eccentric_anomaly = radian_eccentric_anomaly * (180 / np.pi)
    return eccentric_anomaly


def _calculate_true_anomaly(eccentric_anomaly: float, eccentricity: float) -> float:
    """Calculate the true anomaly from the mean anomaly and eccentricity
    of an orbit.

    We use the more numerically stable equation from
    https://ui.adsabs.harvard.edu/abs/1973CeMec...7..388B.

    Parameters
    ----------
    eccentric_anomaly : float
        The eccentric anomaly of the orbit, in degrees.

    Returns
    -------
    true_anomaly : float
        The true anomaly as derived from the eccentric anomaly, in degrees.
    """
    # Converting first to radians.
    radian_eccentric_anomaly = eccentric_anomaly * (np.pi / 180)
    # Using just the numerically stable tangent version. There is no
    # expectation that the eccentricity will be close enough to 1 to have
    # a numerical error.
    beta = eccentricity / (1 + np.sqrt(1 - eccentricity**2))
    radian_true_anomaly = radian_eccentric_anomaly + 2 * np.arctan2(
        beta * np.sin(radian_eccentric_anomaly),
        1 - beta * np.cos(radian_eccentric_anomaly),
    )
    # Converting back to degrees.
    true_anomaly = radian_true_anomaly * (180 / np.pi)
    return true_anomaly


def _vehicle_orbfit_orbit_determiner(observation_record: list[str]) -> dict:
    """This uses the Orbfit engine to calculate orbital elements from the
    observation record. The results are then returned to be managed by
    the main class.

    Parameters
    ----------
    observation_record : list
        The MPC standard 80-column record for observations of the asteroid
        by which the orbit shall be computed from.

    Returns
    -------
    orbit_results : dict
        The results of the orbit computation using the Orbfit engine. Namely,
        this returns the 6 classical Kepler elements, using mean anomaly.
    """
    # Creating the Orbfit class. It does an correct installation check. If
    # the installation is wrong, it is mentioned. Catching it should it fail
    # to add context as well as the stack trace should give the error
    # information.
    try:
        orbfit = orbit.OrbfitOrbitDeterminerEngine()
    except error.InstallError:
        raise error.InstallError(
            "The Orbfit engine is not properly installed; thus it cannot be used to"
            " compute the orbital elements for this solution class."
        )

    # Solving for the orbit. This engine has a record-based solution function
    # so just using it.
    kepler_elements, kepler_error, mjd_epoch = orbfit.solve_orbit_via_record(
        observation_record=observation_record
    )

    # As the Orbfit engine returns the epoch as a MJD but the overall solution
    # requires it as a Julian date, we convert here.
    epoch_julian_day = library.conversion.modified_julian_day_to_julian_day(
        mjd=mjd_epoch
    )

    # Converting the the results from this engine to the standard output
    # expected by the vehicle functions for orbit solving.
    orbit_results = {
        "semimajor_axis": kepler_elements["semimajor_axis"],
        "semimajor_axis_error": kepler_error["semimajor_axis_error"],
        "eccentricity": kepler_elements["eccentricity"],
        "eccentricity_error": kepler_error["eccentricity_error"],
        "inclination": kepler_elements["inclination"],
        "inclination_error": kepler_error["inclination_error"],
        "longitude_ascending_node": kepler_elements["longitude_ascending_node"],
        "longitude_ascending_node_error": kepler_error[
            "longitude_ascending_node_error"
        ],
        "argument_perihelion": kepler_elements["argument_perihelion"],
        "argument_perihelion_error": kepler_error["argument_perihelion_error"],
        "mean_anomaly": kepler_elements["mean_anomaly"],
        "mean_anomaly_error": kepler_error["mean_anomaly_error"],
        "epoch_julian_day": epoch_julian_day,
    }
    # All done.
    return orbit_results


def _vehicle_custom_orbit(observation_record: list[str], vehicle_args: dict) -> dict:
    """This is the vehicle function for the specification of a custom orbit.

    A check is done for the extra vehicle arguments to ensure that the orbital
    elements desired are within the arguments. The observation record is
    not of concern for this vehicle.

    Parameters
    ----------
    observation_record : list
        The MPC standard 80-column record for observations of the asteroid
        by which the orbit shall be computed from.
    vehicle_args : dict
        The arguments to be passed to the Engine class to help its creation
        and solving abilities. In this case, it is just the orbital elements
        as defined.
    """
    # We do not care about the observation record.
    __ = observation_record

    # Attempt to create the engine; if some of the values are not in the
    # vehicle, then raise an error back.
    try:
        custom_orbit = orbit.CustomOrbitEngine(**vehicle_args)
    except TypeError:
        raise error.EngineError(
            "The custom orbit engine cannot be created as the required orbital"
            " parameters have not been passed down through the vehicle arguments."
        )

    # Converting the the results from this engine to the standard output
    # expected by the vehicle functions for orbit solving. Of course, we are
    # just passing the information back up.
    orbit_results = {
        "semimajor_axis": custom_orbit.semimajor_axis,
        "semimajor_axis_error": custom_orbit.semimajor_axis_error,
        "eccentricity": custom_orbit.eccentricity,
        "eccentricity_error": custom_orbit.eccentricity_error,
        "inclination": custom_orbit.inclination,
        "inclination_error": custom_orbit.inclination_error,
        "longitude_ascending_node": custom_orbit.longitude_ascending_node,
        "longitude_ascending_node_error": custom_orbit.longitude_ascending_node_error,
        "argument_perihelion": custom_orbit.argument_perihelion,
        "argument_perihelion_error": custom_orbit.argument_perihelion_error,
        "mean_anomaly": custom_orbit.mean_anomaly,
        "mean_anomaly_error": custom_orbit.mean_anomaly_error,
        "epoch_julian_day": custom_orbit.epoch_julian_day,
    }
    # All done.
    return orbit_results
