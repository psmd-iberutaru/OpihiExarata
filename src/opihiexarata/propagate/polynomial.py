"""For polynomial fitting propagation, using approximations of 2nd order
terms but ignoring some spherical effects."""

import numpy as np
import scipy as sp
import scipy.optimize as sp_optimize

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


class PolynomialPropagationEngine(hint.PropagationEngine):
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
        taken at. The values are in UNIX time.
    ra_poly_param : tuple
            The polynomial fit parameters for the RA(time) propagation.
    dec_poly_param : tuple
            The polynomial fit parameters for the DEC(time) propagation.
    """

    def __init__(
        self, ra: hint.ArrayLike, dec: hint.ArrayLike, obs_time: hint.ArrayLike
    ) -> None:
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
            were taken at. This should be in UNIX time.

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

        # Saving the observational values.
        self.ra_array = ra
        self.dec_array = dec
        self.obs_time_array = obs_time

        # Computing the fitting parameters. That is, the polynomial fit of both
        # RA and DEC as a function of time.
        ra_param, __ = self.__fit_polynomial_function(
            fit_x=self.obs_time_array, fit_y=self.ra_array
        )
        dec_param, __ = self.__fit_polynomial_function(
            fit_x=self.obs_time_array, fit_y=self.dec_array
        )
        self.ra_poly_param = ra_param
        self.dec_poly_param = dec_param

        # All done.
        return None

    @staticmethod
    def __polynomial_function(
        x: hint.ArrayLike, c0: float, c1: float, c2: float
    ) -> hint.ArrayLike:
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
        y = c0 + c1 * x ** 1 + c2 * x ** 2
        return y

    @classmethod
    def __fit_polynomial_function(
        cls, fit_x: hint.ArrayLike, fit_y: hint.ArrayLike
    ) -> tuple[hint.ArrayLike, hint.ArrayLike]:
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
        polynomial_function = cls.__polynomial_function
        try:
            # Most efficient method, but might fail with too few observations.
            fit_param, fit_covar = sp_optimize.curve_fit(
                polynomial_function, fit_x, fit_y, method="lm", p0=[1, 1, 0], max_nfev=10000
            )
        except:
            fit_param, fit_covar = sp_optimize.curve_fit(
                polynomial_function, fit_x, fit_y, method="trf", p0=[1, 1, 0], max_nfev=10000
            )
        # Error on the fit itself.
        fit_error = np.sqrt(np.diag(fit_covar))
        # All done.
        return fit_param, fit_error

    def forward_propagate(
        self, future_time: hint.ArrayLike
    ) -> tuple[hint.ArrayLike, hint.ArrayLike]:
        """Determine a new location(s) based on the polynomial propagation,
        providing new times to locate in the future.

        Parameters
        ----------
        future_time : array-like
            The set of future times which to derive new RA and DEC coordinates.
            The time must be in UNIX time.

        Returns
        -------
        future_ra : ndarray
            The set of right ascensions that cooresponds to the future times, 
            in degrees.
        future_dec : ndarray
            The set of declinations that cooresponds to the future times, in 
            degrees.
        """
        # Determining the RA and DEC via the polynomial function based on the
        # fitted parameters.
        new_ra = self.__polynomial_function(future_time, *self.ra_poly_param)
        new_dec = self.__polynomial_function(future_time, *self.dec_poly_param)
        # Apply wrap around for the angles.
        future_ra = (new_ra + 360) % 360
        future_dec = np.abs(((new_dec - 90) % 360) - 180) - 90
        return future_ra, future_dec
