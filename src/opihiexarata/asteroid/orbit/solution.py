"""The orbit solution class."""

import opihiexarata.asteroid.orbit as orbit
import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


class OrbitSolution(hint.ExarataSolution):
    """This is the class which solves a record of observations to derive the 
    orbital parameters of asteroids or objects in general. A record of 
    observations must be provided.
    
    Attributes
    ----------
    semimajor_axis : float
        The semimajor axis of the orbit solved, in AU.
    semimajor_axis_error : float
        The error on the semimajor axis of the orbit solved, in AU.
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
    """

    def __init__(self, observation_record:list[str], solver_engine: type[hint.OrbitEngine]) -> None:
        """The initialization function. Provided the list of observations,
        solves the orbit for the Keplarian orbits. 

        Additional representations of the orbits in different coordinate 
        frames are provided via computation. TODO

        Parameters
        ----------
        observation_record : list
            A list of the standard MPC 80-column observation records. Each
            element of the list should be a string representing the observation.
        solver_engine : OrbitEngine subclass
            The engine which will be used to complete the orbital elements 
            from the observation record.

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
                " used for astrometric solutions."
            )

        # Derive the orbital elements using the proper vehicle function for 
        # the desired engine is that is to be used.
        if issubclass(solver_engine, orbit.OrbfitOrbitDeterminerEngine):
            # Solve using the API.
            solution_results = _vehicle_astrometrynet_web_api(
                fits_filename=fits_filename
            )
        else:
            # There is no vehicle function, the engine is not supported.
            raise error.EngineError(
                "The provided orbit engine `{eng}` is not supported, there is no"
                " associated vehicle function for it.".format(eng=str(solver_engine))
            )