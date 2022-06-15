"""The ephemeris solution class."""

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

import opihiexarata.ephemeris as ephemeris
import opihiexarata.orbit as orbit


class EphemeriticSolution(library.engine.ExarataSolution):
    """This obtains the ephemeris of an asteroid using an ephemeris engine
    provided the Keplerian orbital elements of the asteroid as determined
    by orbital solutions.

    Attributes
    ----------
    orbitals : OrbitalSolution
        The orbital solution from which the orbital elements will be taken from
        to determine the orbit of the target.
    ra_velocity : float
        The right ascension angular velocity of the target, in degrees per
        second.
    dec_velocity : float
        The declination angular velocity of the target, in degrees per
        second.
    ra_acceleration : float
        The right ascension angular acceleration of the target, in degrees per
        second squared.
    dec_acceleration : float
        The declination angular acceleration of the target, in degrees per
        second squared.
    """

    def __init__(
        self,
        orbitals: hint.OrbitalSolution,
        solver_engine: hint.EphemerisEngine,
        vehicle_args: dict = {},
    ) -> None:
        """Instantiating the solution class.

        Parameters
        ----------
        orbitals : OrbitalSolution
            The orbital solution from which the orbital elements will be taken
            from to determine the orbit of the target.
        solver_engine : EphemerisEngine
            The ephemeris solver engine class. This is what will act as the
            "behind the scenes" and solve the orbit, using this middleware to
            translate it into something that is easier to read.
        vehicle_args : dictionary
            If the vehicle function for the provided solver engine needs
            extra parameters not otherwise provided by the standard input,
            they are given here.

        Returns
        -------
        None
        """
        # Check that the solver engine is a valid submission, that is is an
        # expected engine class.
        if isinstance(solver_engine, library.engine.EphemerisEngine):
            raise error.EngineError(
                "The ephemeris solver engine provided should be the engine class"
                " itself, not an instance thereof."
            )
        elif issubclass(solver_engine, library.engine.EphemerisEngine):
            # It is fine, the user submitted a valid orbit engine.
            pass
        else:
            raise error.EngineError(
                "The provided ephemeris engine is not a valid engine which can be"
                " used for ephemeris solutions."
            )

        # Check that the astrometric solution is a valid solution.
        if not isinstance(orbitals, orbit.OrbitalSolution):
            raise error.InputError(
                "A precomputed orbital solution is required for the computation of"
                " the ephemeritic solution. It must be an OrbitalSolution class"
                " from OpihiExarata."
            )
        else:
            self.orbitals = orbitals

        # Derive the propagation values using the proper vehicle function for
        # the desired engine is that is to be used.
        if issubclass(solver_engine, ephemeris.JPLHorizonsWebAPIEngine):
            # The propagation results.
            raw_ephemeris_results = _vehicle_jpl_horizons_web_api(
                orbitals=self.orbitals
            )
        else:
            # There is no vehicle function, the engine is not supported.
            raise error.EngineError(
                "The provided ephemeris engine `{eng}` is not supported, there is no"
                " associated vehicle function for it.".format(eng=str(solver_engine))
            )

        # Get the results of the solution. If the engine did not provide all of
        # the needed values, then the engine is deficient.
        try:
            # The original information.
            self._ephemeris_function = raw_ephemeris_results["ephemeris_function"]
            self.ra_velocity = raw_ephemeris_results["ra_velocity"]
            self.dec_velocity = raw_ephemeris_results["dec_velocity"]
            self.ra_acceleration = raw_ephemeris_results["ra_acceleration"]
            self.dec_acceleration = raw_ephemeris_results["dec_acceleration"]
        except KeyError:
            raise error.EngineError(
                "The engine results provided are insufficient for this ephemeris"
                " solver. Either the engine cannot be used because it cannot provide"
                " the needed results, or the vehicle function does not pull the"
                " required results from the engine."
            )

        # All done.
        return None

    def forward_ephemeris(
        self, future_time: hint.array
    ) -> tuple[hint.array, hint.array]:
        """A wrapper call around the engine's ephemeris function. This
        allows the computation of future positions at a future time using
        the ephemeris derived from the orbital elements.

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
        future_ra, future_dec = self._ephemeris_function(future_time)
        return future_ra, future_dec


def _vehicle_jpl_horizons_web_api(orbitals: hint.OrbitalSolution):
    """This uses the JPL Horizons web URL API service to derive the ephemeris.

    Parameters
    ----------
    orbitals : OrbitalSolution
        The orbital solution to use to get the orbital elements to send off to
        the JPL Horizons API.

    Returns
    -------
    ephemeris_results : dictionary
        The results of the ephemeris engine which then gets integrated into
        the solution.
    """
    # The results dictionary.
    ephemeris_results = {}

    # Extracting the six orbital elements from the orbital solutions. The
    # JPL horizon page does not accept errors.
    sa = orbitals.semimajor_axis
    ec = orbitals.eccentricity
    ic = orbitals.inclination
    la = orbitals.longitude_ascending_node
    ph = orbitals.argument_perihelion
    ma = orbitals.mean_anomaly
    ep = orbitals.epoch_julian_day

    # Creating the JPL horizons instance.
    jpl_horizons = ephemeris.JPLHorizonsWebAPIEngine(
        semimajor_axis=sa,
        eccentricity=ec,
        inclination=ic,
        longitude_ascending_node=la,
        argument_perihelion=ph,
        mean_anomaly=ma,
        epoch=ep,
    )

    # The future ephemeris function to determine the location of the orbit
    # in the future. The time already requires Julian days.
    ephemeris_function = lambda t: jpl_horizons.forward_ephemeris(future_time=t)

    # The on sky rates as derived from the orbital elements.
    ra_velocity = float(jpl_horizons.ra_velocity)
    dec_velocity = float(jpl_horizons.dec_velocity)
    ra_acceleration = float(jpl_horizons.ra_acceleration)
    dec_acceleration = float(jpl_horizons.dec_acceleration)

    # Constructing the solution dictionary.
    ephemeris_results = {
        "ephemeris_function": ephemeris_function,
        "ra_velocity": ra_velocity,
        "dec_velocity": dec_velocity,
        "ra_acceleration": ra_acceleration,
        "dec_acceleration": dec_acceleration,
    }
    # All done.
    return ephemeris_results
