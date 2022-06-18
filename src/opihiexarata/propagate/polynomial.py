"""For polynomial fitting propagation, using approximations of 1st or 2nd order
terms but ignoring some spherical effects.

Although this could be easily implemented in a better method using subclassing
rather than having two classes, as having a 3rd order is not really feasible, 
and for the sake of readability and stability, two separate copy-like classes
are written.
"""

import numpy as np
import scipy as sp
import scipy.optimize as sp_optimize

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


class LinearPropagationEngine(library.engine.PropagationEngine):
    """A simple propagation engine which uses 1st order extrapolation of
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

    def __init__(self, ra: hint.array, dec: hint.array, obs_time: hint.array) -> None:
        """Instantiation of the propagation engine.

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
                "The RA, DEC, and observation time arrays should be parallel and be"
                " flat. They represent the observations of asteroids."
            )

        # Saving the observational values. The UNIX time is helpful for fitting
        # to avoid numerical issues with using Julian days.s
        self.ra_array = ra
        self.dec_array = dec
        self.unix_obs_time_array = library.conversion.julian_day_to_unix_time(
            jd=obs_time
        )
        self.obs_time_array = obs_time

        # Computing the fitting parameters. That is, the polynomial fit of both
        # RA and DEC as a function of time.
        ra_param, __ = self.__fit_polynomial_function(
            fit_x=self.unix_obs_time_array, fit_y=self.ra_array
        )
        dec_param, __ = self.__fit_polynomial_function(
            fit_x=self.unix_obs_time_array, fit_y=self.dec_array
        )
        self.ra_poly_param = ra_param
        self.dec_poly_param = dec_param

        # All done.
        return None

    @staticmethod
    def __linear_function(
        x: hint.array,
        c0: float,
        c1: float,
    ) -> hint.array:
        """The linear polynomial function that will be used.

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
        self, fit_x: hint.array, fit_y: hint.array
    ) -> tuple[tuple, tuple]:
        """A wrapper class for fitting the defined specific polynomial function.

        Parameters
        ----------
        fix_x : array-like
            The x values which shall be fit.
        fix_y : array-like
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
        except:
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

    def forward_propagate(
        self, future_time: hint.array
    ) -> tuple[hint.array, hint.array]:
        """Determine a new location(s) based on the polynomial propagation,
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
        future_time_unix = library.conversion.julian_day_to_unix_time(jd=future_time)
        # Determining the RA and DEC via the polynomial function based on the
        # fitted parameters.
        new_ra = self.__linear_function(future_time_unix, *self.ra_poly_param)
        new_dec = self.__linear_function(future_time_unix, *self.dec_poly_param)
        # Apply wrap around for the angles.
        future_ra = (new_ra + 360) % 360
        future_dec = np.abs(((new_dec - 90) % 360) - 180) - 90
        return future_ra, future_dec


class QuadraticPropagationEngine(library.engine.PropagationEngine):
    """A simple propagation engine which uses 2nd order extrapolation of
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

    def __init__(self, ra: hint.array, dec: hint.array, obs_time: hint.array) -> None:
        """Instantiation of the propagation engine.

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
                "The RA, DEC, and observation time arrays should be parallel and be"
                " flat. They represent the observations of asteroids."
            )

        # Saving the observational values. The UNIX time is helpful for fitting
        # to avoid numerical issues with using Julian days.
        self.ra_array = ra
        self.dec_array = dec
        self.unix_obs_time_array = library.conversion.julian_day_to_unix_time(
            jd=obs_time
        )
        self.obs_time_array = obs_time

        # Computing the fitting parameters. That is, the polynomial fit of both
        # RA and DEC as a function of time.
        ra_param, __ = self.__fit_polynomial_function(
            fit_x=self.unix_obs_time_array, fit_y=self.ra_array
        )
        dec_param, __ = self.__fit_polynomial_function(
            fit_x=self.unix_obs_time_array, fit_y=self.dec_array
        )
        self.ra_poly_param = ra_param
        self.dec_poly_param = dec_param

        # All done.
        return None

    @staticmethod
    def __quadratic_function(
        x: hint.array, c0: float, c1: float, c2: float
    ) -> hint.array:
        """The polynomial function that will be used.

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
        self, fit_x: hint.array, fit_y: hint.array
    ) -> tuple[tuple, tuple]:
        """A wrapper class for fitting the defined specific polynomial function.

        Parameters
        ----------
        fix_x : array-like
            The x values which shall be fit.
        fix_y : array-like
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
        except:
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

    def forward_propagate(
        self, future_time: hint.array
    ) -> tuple[hint.array, hint.array]:
        """Determine a new location(s) based on the polynomial propagation,
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
        future_time_unix = library.conversion.julian_day_to_unix_time(jd=future_time)
        # Determining the RA and DEC via the polynomial function based on the
        # fitted parameters.
        new_ra = self.__quadratic_function(future_time, *self.ra_poly_param)
        new_dec = self.__quadratic_function(future_time, *self.dec_poly_param)
        # Apply wrap around for the angles.
        future_ra = (new_ra + 360) % 360
        future_dec = np.abs(((new_dec - 90) % 360) - 180) - 90
        return future_ra, future_dec
