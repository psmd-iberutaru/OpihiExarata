"""Polynomial propagation using extrapolation.

For polynomial fitting propagation, using approximations of 1st or 2nd order
terms but ignoring some spherical effects.

Although this could be easily implemented in a better method using subclassing
rather than having two classes, as having a 3rd order is not really feasible,
and for the sake of readability and stability, two separate copy-like classes
are written.
"""

# isort: split
# Import required to remove circular dependencies from type checking.
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opihiexarata.library import hint
# isort: split


import numpy as np
import scipy.optimize as sp_optimize

from opihiexarata import library
from opihiexarata.library import error


class LinearPropagationEngine(library.engine.PropagationEngine):
    """Propagate using linear extrapolation.

    A simple propagation engine which uses 1st order extrapolation of
    RA DEC points independently to determine future location.

    Attributes
    ----------
    ra_array : ndarray
        The array of right ascension measurements to extrapolate to.
    dec_array : ndarray
        The array of declinations measurements to extrapolate to.
    obs_time_array : ndarray
        The array of observation times which the RA and DEC measurements were
        taken at. The values are in Julian days.
    ra_poly_param : tuple
        The polynomial fit parameters for the RA(time) propagation.
    dec_poly_param : tuple
        The polynomial fit parameters for the DEC(time) propagation.
    ra_wrap_around : boolean
        A flag which signifies that the RA values, as given, wraps around the
        0/360 point.

    """

    def __init__(
        self: LinearPropagationEngine,
        ra: hint.array,
        dec: hint.array,
        obs_time: hint.array,
    ) -> None:
        """Instantiate the propagation engine.

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
            were taken at. This should be in Julian days.

        Returns
        -------
        None

        """
        # Must be parallel arrays.
        ra = np.asarray(ra)
        dec = np.asarray(dec)
        obs_time = np.asarray(obs_time)
        if ra.shape == dec.shape == obs_time.shape:
            # This is expected.
            pass
        else:
            raise error.InputError(
                "The RA, DEC, and observation time arrays should be parallel"
                " and be flat. They represent the observations of asteroids.",
            )

        # Saving the observational values. The UNIX time is helpful for fitting
        # to avoid numerical issues with using Julian days.s
        self.ra_array = ra
        self.dec_array = dec
        self.unix_obs_time_array = library.conversion.julian_day_to_unix_time(
            jd=obs_time,
        )
        self.obs_time_array = obs_time

        # We need to determine if the RA values loop around the angle value.
        # If so, we need to perform a transformation to and from an alternative
        # coordinate system 180 degrees offset.
        excessive_angle = 270
        if np.ptp(ra) >= excessive_angle:
            # The angles is almost guaranteed to have wrapped around.
            self.ra_wraparound = True
        else:
            self.ra_wraparound = False

        # Computing the fitting parameters. That is, the polynomial fit of both
        # RA and DEC as a function of time.
        # If there is a wraparound, we need to account for that.
        fixed_ra_array = self._right_ascension_rotation(ra=ra)
        ra_param, __ = self.__fit_polynomial_function(
            fit_x=self.unix_obs_time_array,
            fit_y=fixed_ra_array,
        )
        dec_param, __ = self.__fit_polynomial_function(
            fit_x=self.unix_obs_time_array,
            fit_y=self.dec_array,
        )
        self.ra_poly_param = ra_param
        self.dec_poly_param = dec_param

        # All done.

    @staticmethod
    def __linear_function(
        x: hint.array,
        c0: float,
        c1: float,
    ) -> hint.array:
        """Linear polynomial function that will be used.

        This function is hard coded to be a specific order on purpose. The
        order may be changed between versions if need be, but should not be
        changed via configuration.

        Parameters
        ----------
        x : array-like
            The input for computing the polynomial.
        c0 : float
            Coefficient for order 0.
        c1 : float
            Coefficient for order 1.

        Returns
        -------
        y : array-like
            The output after computing the polynomial with the provided
            coefficients.

        """
        # Computing the polynomial
        y = c0 + c1 * x**1
        return y

    def __fit_polynomial_function(
        self: hint.Self,
        fit_x: hint.array,
        fit_y: hint.array,
    ) -> tuple[tuple, tuple]:
        """Wrap class for fitting the defined specific polynomial function.

        Parameters
        ----------
        fit_x : array-like
            The x values which shall be fit.
        fit_y : array-like
            The y values which shall be fit.

        Returns
        -------
        fit_param : tuple
            The parameters of the polynomial that corresponded to the best fit.
            Determined by the order of the polynomial function.
        fit_error : tuple
            The error on the parameters of the fit.

        """
        # Ensuring that the arrays are numpy-like and can thus be handled by
        # scipy.
        fit_x = np.asarray(fit_x)
        fit_y = np.asarray(fit_y)
        # Fitting.
        polynomial_function = self.__linear_function
        max_iteration_count = int(1e6)
        try:
            # Most efficient method, but might fail with too few observations.
            fit_param, fit_covar = sp_optimize.curve_fit(
                polynomial_function,
                fit_x,
                fit_y,
                method="lm",
            )
        except RuntimeError:
            fit_param, fit_covar = sp_optimize.curve_fit(
                polynomial_function,
                fit_x,
                fit_y,
                method="trf",
                max_nfev=max_iteration_count,
            )
        # Error on the fit itself.
        fit_error = np.sqrt(np.diag(fit_covar))
        # All done.
        return fit_param, fit_error

    def _right_ascension_rotation(
        self: hint.Self,
        ra: hint.array,
    ) -> hint.array:
        """Normalize RA rotation to deal with modularity.

        If the RA loops around the 0/360 region, this function transforms
        it via a rotation to +/- 180 so that the polynomial fitting is not
        problematic.

        If there was no wraparound present, then this function just passes the
        input untouched.

        Parameters
        ----------
        ra : array-like
            The RA without the rotation where there is a possible wraparound.

        Returns
        -------
        rotated_ra : array
            The array after the rotation, if a wraparound is present.

        """
        # If a wraparound was detected, we need to do a rotation. Else
        # no rotation is required.
        ra = np.array(ra)
        rotated_ra = (ra + 180) % 360 if self.ra_wraparound else ra

        # All done.
        return rotated_ra

    def _right_ascension_inverse_rotation(
        self: hint.Self,
        rotated_ra: hint.array,
    ) -> hint.array:
        """Revert the rotation for wraparound avoidance.

        This function inverses the rotation done because of the
        transformation to avoid the wraparound in the 0/360 region if it
        exists.

        If there was no wraparound present, then this function just passes the
        input untouched.

        Parameters
        ----------
        rotated_ra : array-like
            The RA array, after the rotation has been done by the rotation
            function.

        Returns
        -------
        inverse_rotated_ra : array
            The array after the inverse rotation, if a wraparound is present.

        """
        # If a wrap around was detected, we need to do the inverse rotation.
        rotated_ra = np.array(rotated_ra)
        if self.ra_wraparound:
            inverse_rotated_ra = (rotated_ra - 180) % 360
        else:
            inverse_rotated_ra = rotated_ra
        # All done.
        return inverse_rotated_ra

    def forward_propagate(
        self: hint.Self,
        future_time: hint.array,
    ) -> tuple[hint.array, hint.array]:
        """Find the new RA and DECs from propagation.

        Determine a new location(s) based on the polynomial propagation,
        providing new times to locate in the future.

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
        # As the polynomial fitting was done with UNIX time instead of Julian
        # days, we need to convert to the same timescale.
        future_time_unix = library.conversion.julian_day_to_unix_time(
            jd=future_time,
        )
        # Determining the RA and DEC via the polynomial function based on the
        # fitted parameters.
        new_ra = self.__linear_function(future_time_unix, *self.ra_poly_param)
        new_dec = self.__linear_function(future_time_unix, *self.dec_poly_param)
        # If a wraparound is present in the original data, then the data that
        # was fit was rotated. So, the fit values provided are in that rotated
        # coordinate space. We revert it back to the original coordinates
        # before the rotation.
        new_ra = self._right_ascension_inverse_rotation(rotated_ra=new_ra)
        # Apply wrap around for the angles for any exceeding the standard
        # conventional limits.
        future_ra = (new_ra + 360) % 360
        future_dec = np.abs(((new_dec - 90) % 360) - 180) - 90
        return future_ra, future_dec


class QuadraticPropagationEngine(library.engine.PropagationEngine):
    """Quadratic propagation engine.

    A simple propagation engine which uses 2nd order extrapolation of
    RA DEC points independently to determine future location.

    Attributes
    ----------
    ra_array : ndarray
        The array of right ascension measurements to extrapolate to.
    dec_array : ndarray
        The array of declinations measurements to extrapolate to.
    obs_time_array : ndarray
        The array of observation times which the RA and DEC measurements were
        taken at. The values are in Julian days.
    ra_poly_param : tuple
            The polynomial fit parameters for the RA(time) propagation.
    dec_poly_param : tuple
            The polynomial fit parameters for the DEC(time) propagation.

    """

    def __init__(
        self: QuadraticPropagationEngine,
        ra: hint.array,
        dec: hint.array,
        obs_time: hint.array,
    ) -> None:
        """Instantiate the propagation engine.

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
            were taken at. This should be in Julian days.

        Returns
        -------
        None

        """
        # Must be parallel arrays.
        ra = np.asarray(ra)
        dec = np.asarray(dec)
        obs_time = np.asarray(obs_time)
        if ra.shape == dec.shape == obs_time.shape:
            # This is expected.
            pass
        else:
            raise error.InputError(
                "The RA, DEC, and observation time arrays should be parallel "
                "and be flat. They represent the observations of asteroids.",
            )

        # Saving the observational values. The UNIX time is helpful for fitting
        # to avoid numerical issues with using Julian days.
        self.ra_array = ra
        self.dec_array = dec
        self.unix_obs_time_array = library.conversion.julian_day_to_unix_time(
            jd=obs_time,
        )
        self.obs_time_array = obs_time

        # We need to determine if the RA values loop around the angle value.
        # If so, we need to perform a transformation to and from an alternative
        # coordinate system 180 degrees offset.
        min_likely_wrap_around = 270
        if np.ptp(ra) >= min_likely_wrap_around:
            # The angles is almost guaranteed to have wrapped around.
            self.ra_wraparound = True
        else:
            self.ra_wraparound = False

        # Computing the fitting parameters. That is, the polynomial fit of both
        # RA and DEC as a function of time.
        # If there is a wraparound, we need to account for that.
        fixed_ra_array = self._right_ascension_rotation(ra=ra)
        ra_param, __ = self.__fit_polynomial_function(
            fit_x=self.unix_obs_time_array,
            fit_y=fixed_ra_array,
        )
        dec_param, __ = self.__fit_polynomial_function(
            fit_x=self.unix_obs_time_array,
            fit_y=self.dec_array,
        )
        self.ra_poly_param = ra_param
        self.dec_poly_param = dec_param

        # All done.

    @staticmethod
    def __quadratic_function(
        x: hint.array,
        c0: float,
        c1: float,
        c2: float,
    ) -> hint.array:
        """Propagation quadratic function.

        This function is hard coded to be a specific order on purpose. The
        order may be changed between versions if need be, but should not be
        changed via configuration.

        Parameters
        ----------
        x : array-like
            The input for computing the polynomial.
        c0 : float
            Coefficient for order 0.
        c1 : float
            Coefficient for order 1.
        c2 : float
            Coefficient for order 2.

        Returns
        -------
        y : array-like
            The output after computing the polynomial with the provided
            coefficients.

        """
        # Computing the polynomial
        y = c0 + c1 * x**1 + c2 * x**2
        return y

    def __fit_polynomial_function(
        self: hint.Self,
        fit_x: hint.array,
        fit_y: hint.array,
    ) -> tuple[tuple, tuple]:
        """Wrap function for fitting the defined specific polynomial function.

        Parameters
        ----------
        fit_x : array-like
            The x values which shall be fit.
        fit_y : array-like
            The y values which shall be fit.

        Returns
        -------
        fit_param : tuple
            The parameters of the polynomial that corresponded to the best fit.
            Determined by the order of the polynomial function.
        fit_error : tuple
            The error on the parameters of the fit.

        """
        # Ensuring that the arrays are numpy-like and can thus be handled by
        # scipy.
        fit_x = np.asarray(fit_x)
        fit_y = np.asarray(fit_y)
        # Fitting.
        polynomial_function = self.__quadratic_function
        try:
            # Most efficient method, but might fail with too few observations.
            fit_param, fit_covar = sp_optimize.curve_fit(
                polynomial_function,
                fit_x,
                fit_y,
                method="lm",
                p0=[1, 1, 0],
                max_nfev=10000,
            )
        except RuntimeError:
            fit_param, fit_covar = sp_optimize.curve_fit(
                polynomial_function,
                fit_x,
                fit_y,
                method="trf",
                p0=[1, 1, 0],
                max_nfev=10000,
            )
        # Error on the fit itself.
        fit_error = np.sqrt(np.diag(fit_covar))
        # All done.
        return fit_param, fit_error

    def _right_ascension_rotation(
        self: hint.Self,
        ra: hint.array,
    ) -> hint.array:
        """Rotate the RA to avoid wrap around.

        If the RA loops around the 0/360 region, this function transforms
        it via a rotation to +/- 180 so that the polynomial fitting is not
        problematic.

        If there was no wraparound present, then this function just passes the
        input untouched.

        Parameters
        ----------
        ra : array-like
            The RA without the rotation where there is a possible wraparound.

        Returns
        -------
        rotated_ra : array
            The array after the rotation, if a wraparound is present.

        """
        # If a wraparound was detected, we need to do a rotation.
        ra = np.array(ra)
        rotated_ra = (ra + 180) % 360 if self.ra_wraparound else ra
        # All done.
        return rotated_ra

    def _right_ascension_inverse_rotation(
        self: hint.Self,
        rotated_ra: hint.array,
    ) -> hint.array:
        """Revert the rotation for wraparound avoidance.

        This function inverses the rotation done because of the
        transformation to avoid the wraparound in the 0/360 region if it
        exists. If there was no wraparound present, then this function just
        passes the input untouched.

        Parameters
        ----------
        rotated_ra : array-like
            The RA array, after the rotation has been done by the rotation
            function.

        Returns
        -------
        inverse_rotated_ra : array
            The array after the inverse rotation, if a wraparound is present.

        """
        # If a wrap around was detected, we need to do the inverse rotation.
        rotated_ra = np.array(rotated_ra)
        if self.ra_wraparound:
            inverse_rotated_ra = (rotated_ra - 180) % 360
        else:
            inverse_rotated_ra = rotated_ra
        # All done.
        return inverse_rotated_ra

    def forward_propagate(
        self: hint.Self,
        future_time: hint.array,
    ) -> tuple[hint.array, hint.array]:
        """Determine a new location(s) based on the polynomial propagation.

        Propagation serves to provide new times to locate in the future.

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
        # As the polynomial fitting was done with UNIX time instead of Julian
        # days, we need to convert to the same timescale.
        future_time_unix = library.conversion.julian_day_to_unix_time(
            jd=future_time,
        )
        # Determining the RA and DEC via the polynomial function based on the
        # fitted parameters.
        new_ra = self.__quadratic_function(
            future_time_unix,
            *self.ra_poly_param,
        )
        new_dec = self.__quadratic_function(
            future_time_unix,
            *self.dec_poly_param,
        )
        # If a wraparound is present in the original data, then the data that
        # was fit was rotated. So, the fit values provided are in that rotated
        # coordinate space. We revert it back to the original coordinates
        # before the rotation.
        new_ra = self._right_ascension_inverse_rotation(rotated_ra=new_ra)
        # Apply wrap around for the angles for any exceeding the standard
        # conventional limits.
        future_ra = (new_ra + 360) % 360
        future_dec = np.abs(((new_dec - 90) % 360) - 180) - 90
        return future_ra, future_dec
