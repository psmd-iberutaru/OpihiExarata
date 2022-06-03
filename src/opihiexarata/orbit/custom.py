"""This is a class which defines a custom orbit. A user supplies the orbital 
elements to this engine and the vehicle function."""

import numpy as np

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


class CustomOrbitEngine(library.engine.OrbitEngine):
    """This engine is just a wrapper for when a custom orbit is desired to be
    specified.

    Attributes
    ----------
    semimajor_axis : float
        The semi-major axis of the orbit provided, in AU.
    semimajor_axis_error : float
        The error on the semi-major axis of the orbit provided, in AU.
    eccentricity : float
        The eccentricity of the orbit provided.
    eccentricity_error : float
        The error on the eccentricity of the orbit provided.
    inclination : float
        The angle of inclination of the orbit provided, in degrees.
    inclination_error : float
        The error on the angle of inclination of the orbit provided, in degrees.
    longitude_ascending_node : float
        The longitude of the ascending node of the orbit provided, in degrees.
    longitude_ascending_node_error : float
        The error on the longitude of the ascending node of the orbit
        provided, in degrees.
    argument_perihelion : float
        The argument of perihelion of the orbit provided, in degrees.
    argument_perihelion_error : float
        The error on the argument of perihelion of the orbit
        provided, in degrees.
    mean_anomaly : float
        The mean anomaly of the orbit provided, in degrees.
    mean_anomaly_error : float
        The error on the mean anomaly of the orbit provided, in degrees.
    epoch_julian_day : float
        The epoch where for these osculating orbital elements. This value is
        in Julian days.
    """

    def __init__(
        self,
        semimajor_axis: float,
        eccentricity: float,
        inclination: float,
        longitude_ascending_node: float,
        argument_perihelion: float,
        mean_anomaly: float,
        epoch_julian_day: float,
        semimajor_axis_error: float = None,
        eccentricity_error: float = None,
        inclination_error: float = None,
        longitude_ascending_node_error: float = None,
        argument_perihelion_error: float = None,
        mean_anomaly_error: float = None,
    ) -> None:
        """The orbital elements are already provided for this custom
        solution. If errors may optionally be provided.

        Parameters
        ----------
        semimajor_axis : float
            The semi-major axis of the orbit provided, in AU.
        eccentricity : float
            The eccentricity of the orbit provided.
        inclination : float
            The angle of inclination of the orbit provided, in degrees.
        longitude_ascending_node : float
            The longitude of the ascending node of the orbit
            provided, in degrees.
        argument_perihelion : float
            The argument of perihelion of the orbit provided, in degrees.
        mean_anomaly : float
            The mean anomaly of the orbit provided, in degrees.
        epoch_julian_day : float
            The epoch where for these osculating orbital elements. This value is
            in Julian days.
        semimajor_axis_error : float, default = None
            The error on the semi-major axis of the orbit provided, in AU.
        eccentricity_error : float, default = None
            The error on the eccentricity of the orbit provided.
        inclination_error : float, default = None
            The error on the angle of inclination of the orbit provided, in degrees.
        longitude_ascending_node_error : float, default = None
            The error on the longitude of the ascending node of the orbit
            provided, in degrees.
        argument_perihelion_error : float, default = None
            The error on the argument of perihelion of the orbit
            provided, in degrees.
        mean_anomaly_error : float, default = None
            The error on the mean anomaly of the orbit provided, in degrees.

        Returns
        -------
        None
        """
        # Given that all of the values were provided to us, we just
        # re-encapsulate it.

        # The orbital elements must be defined so they are already numbers.
        self.semimajor_axis = float(semimajor_axis)
        self.eccentricity = float(eccentricity)
        self.inclination = float(inclination)
        self.longitude_ascending_node = float(longitude_ascending_node)
        self.argument_perihelion = float(argument_perihelion)
        self.mean_anomaly = float(mean_anomaly)
        self.epoch_julian_day = float(epoch_julian_day)

        # Errors are optional, if they were not provided, it is most
        # appropriate for them to be NaN.
        self.semimajor_axis_error = (
            np.nan if semimajor_axis_error is None else float(semimajor_axis_error)
        )
        self.eccentricity_error = (
            np.nan if eccentricity_error is None else float(eccentricity_error)
        )
        self.inclination_error = (
            np.nan if inclination_error is None else float(inclination_error)
        )
        self.longitude_ascending_node_error = (
            np.nan
            if longitude_ascending_node_error is None
            else float(longitude_ascending_node_error)
        )
        self.argument_perihelion_error = (
            np.nan
            if argument_perihelion_error is None
            else float(argument_perihelion_error)
        )
        self.mean_anomaly_error = (
            np.nan if mean_anomaly_error is None else float(mean_anomaly_error)
        )

        # All done.
        return None
