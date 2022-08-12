"""The main solution class for propagations.
"""
import numpy as np


import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

import opihiexarata.propagate as propagate


class PropagativeSolution(library.engine.ExarataSolution):
    """The general solution class for asteroid propagation.

    This uses the recent past location of asteroids to determine their
    future location. For determination based on orbital elements and
    ephemerids, use the OrbitalSolution and EphemeriticSolution classes
    respectively.

    Attributes
    ----------
    ra_array : array-like
            The array of right ascensions used fit and extrapolate to,
            in degrees.
    dec_array : array-like
            The array of declinations used fit and extrapolate to, in degrees.
    obs_time_array : array-like
            An array of observation times which the RA and DEC measurements
            were taken at. The values are in Julian days.
    raw_ra_velocity : float
        The right ascension angular velocity of the target, in degrees per
        second. These values are derived straight from the data and not the
        propagation engine.
    raw_dec_velocity : float
        The declination angular velocity of the target, in degrees per
        second. These values are derived straight from the data and not the
        propagation engine.
    raw_ra_acceleration : float
        The right ascension angular acceleration of the target, in degrees per
        second squared. These values are derived straight from the data and
        not the propagation engine.
    raw_dec_acceleration : float
        The declination angular acceleration of the target, in degrees per
        second squared. These values are derived straight from the data
        and not the propagation engine.
    ra_velocity : float
        The right ascension angular velocity of the target, in degrees per
        second. These values are derived from the engine.
    dec_velocity : float
        The declination angular velocity of the target, in degrees per
        second. These values are derived from the engine.
    ra_acceleration : float
        The right ascension angular acceleration of the target, in degrees per
        second squared. These values are derived from the engine.
    dec_acceleration : float
        The declination angular acceleration of the target, in degrees per
        second squared. These values are derived from the engine.
    """

    def __init__(
        self,
        ra: hint.array,
        dec: hint.array,
        obs_time: list,
        solver_engine: hint.PropagationEngine,
        vehicle_args: dict = {},
    ):
        """The instantiation of the propagation solution.

        Parameters
        ----------
        ra : array-like
            An array of right ascensions to fit and extrapolate to, must be in
            degrees.
        dec : array-like
            An array of declinations to fit and extrapolate to, must be in
            degrees.
        obs_time : array-like
            An array of observation times which the RA and DEC measurements
            were taken at. Must be Julian days.
        solver_engine : PropagationEngine
            The propagation solver engine class that will be used to compute
            the propagation solution.
        vehicle_args : dictionary
            If the vehicle function for the provided solver engine needs
            extra parameters not otherwise provided by the standard input,
            they are given here.

        Returns
        -------
        None
        """
        # Saving the sent values.
        self.ra_array = np.asarray(ra, dtype=float)
        self.dec_array = np.asarray(dec, dtype=float)
        self.obs_time_array = np.asarray(obs_time, dtype=float)

        # Check that the solver engine is a valid submission, that is is an
        # expected engine class.
        if isinstance(solver_engine, library.engine.PropagationEngine):
            raise error.EngineError(
                "The propagation solver engine provided should be the engine class"
                " itself, not an instance thereof."
            )
        elif issubclass(solver_engine, library.engine.PropagationEngine):
            # It is fine, the user submitted a valid orbit engine.
            pass
        else:
            raise error.EngineError(
                "The provided propagation engine is not a valid engine which can be"
                " used for propagation solutions."
            )

        # Derive the propagation values using the proper vehicle function for
        # the desired engine is that is to be used.
        if issubclass(solver_engine, propagate.LinearPropagationEngine):
            # The propagation results.
            raw_propagate_results = _vehicle_linear_propagation(
                ra_array=self.ra_array,
                dec_array=self.dec_array,
                obs_time_array=self.obs_time_array,
            )
        elif issubclass(solver_engine, propagate.QuadraticPropagationEngine):
            # The propagation results.
            raw_propagate_results = _vehicle_quadratic_propagation(
                ra_array=self.ra_array,
                dec_array=self.dec_array,
                obs_time_array=self.obs_time_array,
            )
        else:
            # There is no vehicle function, the engine is not supported.
            raise error.EngineError(
                "The provided orbit engine `{eng}` is not supported, there is no"
                " associated vehicle function for it.".format(eng=str(solver_engine))
            )
        # Get the results of the solution. If the engine did not provide all of
        # the needed values, then the engine is deficient.
        try:
            # The original information.
            self._propagation_function = raw_propagate_results["propagation_function"]
        except KeyError:
            raise error.EngineError(
                "The engine results provided are insufficient for this propagation"
                " solver. Either the engine cannot be used because it cannot provide"
                " the needed results, or the vehicle function does not pull the"
                " required results from the engine."
            )

        # Deriving the rates from the raw data. They should be similar to the
        # propagation but no test shall be done. Here the rates are calculated
        # from the three most recent points.
        r_ra_v, r_dc_v, r_ra_a, r_dc_a = self.__init_compute_raw_motion(
            ra_array=self.ra_array,
            dec_array=self.dec_array,
            obs_time_array=self.obs_time_array,
        )
        self.raw_ra_velocity = r_ra_v
        self.raw_ra_acceleration = r_ra_a
        self.raw_dec_velocity = r_dc_v
        self.raw_dec_acceleration = r_dc_a

        # Deriving the rates from the propagation function.
        p_ra_v, p_dc_v, p_ra_a, p_dc_a = self.__init_compute_propagation_motion(
            obs_time_array=self.obs_time_array
        )
        self.ra_velocity = p_ra_v
        self.ra_acceleration = p_ra_a
        self.dec_velocity = p_dc_v
        self.dec_acceleration = p_dc_a

        # All done.
        return None

    def __init_compute_raw_motion(
        self,
        ra_array: hint.array,
        dec_array: hint.array,
        obs_time_array: hint.array,
    ) -> tuple[float, float, float, float]:
        """Compute the raw velocities and accelerations of RA and DEC.

        This function prioritizes calculating the raw motion using the most
        recent observations only.

        Parameters
        ----------
        ra_array : array-like
            The array of right ascensions used fit and extrapolate to,
            in degrees.
        dec_array : array-like
            The array of declinations used fit and extrapolate to, in degrees.
        obs_time_array : array-like
            An array of observation times which the RA and DEC measurements
            were taken at. The values are in Julian days.

        Returns
        -------
        raw_ra_velocity : float
            The raw right ascension angular velocity of the target, in degrees
            per second.
        raw_dec_velocity : float
            The raw declination angular velocity of the target, in degrees per
            second.
        raw_ra_acceleration : float
            The raw right ascension angular acceleration of the target, in
            degrees per second squared.
            propagation engine.
        raw_dec_acceleration : float
            The raw declination angular acceleration of the target, in
            degrees per second squared.
        """
        # As the observing time is in Julian days, but as our rates are going
        # to be in seconds, it is easier to just transform our units to
        # seconds via UNIX time.
        unix_obs_time_array = library.conversion.julian_day_to_unix_time(
            jd=obs_time_array
        )

        # Computing the differences.
        delta_ra = ra_array[1:] - ra_array[:-1]
        delta_dec = dec_array[1:] - dec_array[:-1]
        delta_time = unix_obs_time_array[1:] - unix_obs_time_array[:-1]
        # First difference is velocity, using the most recent measure to get
        # the velocity.
        raw_ra_velocity = delta_ra[-1] / delta_time[-1]
        raw_dec_velocity = delta_dec[-1] / delta_time[-1]
        # The second difference is acceleration. We use midpoint time
        # differences to determine the time difference between three
        # observations.
        if unix_obs_time_array.size > 2:
            # There are more than two observations, acceleration can be
            # calculated.
            delta2_ra = delta_ra[1:] - delta_ra[:-1]
            delta2_dec = delta_dec[1:] - delta_dec[:-1]
            delta2_time = (unix_obs_time_array[2:] - unix_obs_time_array[:-2]) / 2
            raw_ra_acceleration = delta2_ra[-1] / delta2_time[-1]
            raw_dec_acceleration = delta2_dec[-1] / delta2_time[-1]
        else:
            # A true raw acceleration cannot be calculated so we assume zero.
            raw_ra_acceleration = 0
            raw_dec_acceleration = 0
        # All done.
        return (
            raw_ra_velocity,
            raw_dec_velocity,
            raw_ra_acceleration,
            raw_dec_acceleration,
        )

    def __init_compute_propagation_motion(
        self,
        obs_time_array: hint.array,
    ) -> tuple[float, float, float, float]:
        """Compute the raw velocities and accelerations of RA and DEC.

        This function prioritizes calculating the raw motion using the most
        recent observations only.

        Parameters
        ----------
        obs_time_array : array-like
            An array of observation times which the RA and DEC measurements
            were taken at. The values are in Julian days.

        Returns
        -------
        propagate_ra_velocity : float
            The propagative right ascension angular velocity of the target, in degrees
            per second.
        propagate_dec_velocity : float
            The propagative declination angular velocity of the target, in degrees per
            second.
        propagate_ra_acceleration : float
            The propagative right ascension angular acceleration of the target, in
            degrees per second squared.
            propagation engine.
        propagate_dec_acceleration : float
            The propagative declination angular acceleration of the target, in
            degrees per second squared.
        """
        # From the propagation methods, calculate the expected locations
        # of the target based on propagation. Although this is forward
        # propagation, deriving rates from non-present times is not really
        # helpful.
        ra_array, dec_array = self.forward_propagate(future_time=obs_time_array)

        # As the observing time is in Julian days, but as our rates are going
        # to be in seconds, it is easier to just transform our units to
        # seconds via UNIX time.
        unix_obs_time_array = library.conversion.julian_day_to_unix_time(
            jd=obs_time_array
        )

        # Computing the differences.
        delta_ra = ra_array[1:] - ra_array[:-1]
        delta_dec = dec_array[1:] - dec_array[:-1]
        delta_time = unix_obs_time_array[1:] - unix_obs_time_array[:-1]
        # First difference is velocity, using the most recent measure to get
        # the velocity.
        propagate_ra_velocity = delta_ra[-1] / delta_time[-1]
        propagate_dec_velocity = delta_dec[-1] / delta_time[-1]
        # The second difference is acceleration. We use midpoint time
        # differences to determine the time difference between three
        # observations.
        if unix_obs_time_array.size > 2:
            # There are more than two observations, acceleration can be
            # calculated.
            delta2_ra = delta_ra[1:] - delta_ra[:-1]
            delta2_dec = delta_dec[1:] - delta_dec[:-1]
            delta2_time = (unix_obs_time_array[2:] - unix_obs_time_array[:-2]) / 2
            propagate_ra_acceleration = delta2_ra[-1] / delta2_time[-1]
            propagate_dec_acceleration = delta2_dec[-1] / delta2_time[-1]
        else:
            # A true raw acceleration cannot be calculated so we assume zero.
            propagate_ra_acceleration = 0
            propagate_dec_acceleration = 0
        # All done.
        return (
            propagate_ra_velocity,
            propagate_dec_velocity,
            propagate_ra_acceleration,
            propagate_dec_acceleration,
        )

    def forward_propagate(
        self, future_time: hint.array
    ) -> tuple[hint.array, hint.array]:
        """A wrapper call around the engine's propagation function. This
        allows the computation of future positions at a future time using
        propagation.

        Parameters
        ----------
        future_time : array-like
            The set of future times which to derive new RA and DEC coordinates.
            The time must be in Julian days.

        Returns
        -------
        future_ra : ndarray
            The set of right ascensions that corresponds to the future times,
            in degrees.
        future_dec : ndarray
            The set of declinations that corresponds to the future times, in
            degrees.
        """
        future_ra, future_dec = self._propagation_function(future_time)
        return future_ra, future_dec


def _vehicle_linear_propagation(
    ra_array: hint.array, dec_array: hint.array, obs_time_array: hint.array
) -> dict:
    """Derive the propagation from 1st order polynomial extrapolation methods.

    Parameters
    ----------
    ra_array : array-like
        The array of right ascensions used fit and extrapolate to,
        in degrees.
    dec_array : array-like
        The array of declinations used fit and extrapolate to, in degrees.
    obs_time_array : array-like
        An array of observation times which the RA and DEC measurements
        were taken at. The values are in Julian days.

    Returns
    -------
    solution_results : dictionary
        The results of the propagation engine which then gets integrated into
        the solution.
    """
    # Instantiate the propagation engine.
    polyprop = propagate.LinearPropagationEngine(
        ra=ra_array, dec=dec_array, obs_time=obs_time_array
    )
    # Check that the system uses quadratics, otherwise this section needs to
    # be double checked.
    if polyprop.ra_poly_param.shape != (2,) or polyprop.dec_poly_param.shape != (2,):
        raise error.DevelopmentError(
            "The polynomial engine does not use quadratics. This engine function needs"
            " to be revised to ensure that it is returning the correct values."
        )
    # The propagation function.
    propagation_function = lambda t: polyprop.forward_propagate(future_time=t)

    # The dictionary that holds the results.
    solution_results = {
        "propagation_function": propagation_function,
    }
    # All done.
    return solution_results


def _vehicle_quadratic_propagation(
    ra_array: hint.array, dec_array: hint.array, obs_time_array: hint.array
) -> dict:
    """Derive the propagation from 2nd order polynomial extrapolation methods.

    Parameters
    ----------
    ra_array : array-like
        The array of right ascensions used fit and extrapolate to,
        in degrees.
    dec_array : array-like
        The array of declinations used fit and extrapolate to, in degrees.
    obs_time_array : array-like
        An array of observation times which the RA and DEC measurements
        were taken at. The values are in Julian days.

    Returns
    -------
    solution_results : dictionary
        The results of the propagation engine which then gets integrated into
        the solution.
    """
    # Instantiate the propagation engine.
    polyprop = propagate.QuadraticPropagationEngine(
        ra=ra_array, dec=dec_array, obs_time=obs_time_array
    )
    # Check that the system uses quadratics, otherwise this section needs to
    # be double checked.
    if polyprop.ra_poly_param.shape != (3,) or polyprop.dec_poly_param.shape != (3,):
        raise error.DevelopmentError(
            "The quadratic engine does not use quadratics. This engine function needs"
            " to be revised to ensure that it is returning the correct values."
        )
    # The propagation function.
    propagation_function = lambda t: polyprop.forward_propagate(future_time=t)

    # The dictionary that holds the results.
    solution_results = {
        "propagation_function": propagation_function,
    }
    # All done.
    return solution_results
