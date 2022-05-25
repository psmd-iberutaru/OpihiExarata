"""The different ephemeris engines which use JPL horizons as its backend."""

import requests
import numpy as np
import astropy.table as ap_table
from opihiexarata import ephemeris

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


class JPLHorizonsWebAPIEngine(hint.EphemerisEngine):
    """This obtains the ephemeris of an asteroid using JPL horizons provided
    the Keplerian orbital elements of the asteroid as determined by orbital
    solutions.

    Attributes
    ----------
    semimajor_axis : float
        The semi-major axis of the orbit, in AU.
    eccentricity : float
        The eccentricity of the orbit.
    inclination : float
        The angle of inclination of the orbit, in degrees.
    longitude_ascending_node : float
        The longitude of the ascending node of the orbit, in degrees.
    argument_perihelion : float
        The argument of perihelion of the orbit, in degrees.
    mean_anomaly : float
        The mean anomaly of the orbit, in degrees.
    epoch : float
        The modified Julian date epoch of the osculating orbital elements.
    forward_ephemeris : function
        Calculates a ephemeris position on the sky at a given time provided
        the orbital elements.
    """

    def __init__(
        self,
        semimajor_axis: float,
        eccentricity: float,
        inclination: float,
        longitude_ascending_node: float,
        argument_perihelion: float,
        mean_anomaly: float,
        epoch: float,
    ) -> None:
        """Creating the engine.

        Parameters
        ----------
        semimajor_axis : float
            The semi-major axis of the orbit, in AU.
        eccentricity : float
            The eccentricity of the orbit.
        inclination : float
            The angle of inclination of the orbit, in degrees.
        longitude_ascending_node : float
            The longitude of the ascending node of the orbit, in degrees.
        argument_perihelion : float
            The argument of perihelion of the orbit, in degrees.
        mean_anomaly : float
            The mean anomaly of the orbit, in degrees.
        epoch : float
            The full Julian date epoch of these osculating orbital elements.

        Return
        ------
        None
        """
        # Storing the orbital elements for usage during the API calls.
        self.semimajor_axis = semimajor_axis
        self.eccentricity = eccentricity
        self.inclination = inclination
        self.longitude_ascending_node = longitude_ascending_node
        self.argument_perihelion = argument_perihelion
        self.mean_anomaly = mean_anomaly
        self.epoch = epoch

        # Deriving the forward ephemeris function.

    def _query_jpl_horizons(self, start_time, stop_time, time_step) -> hint.Table:
        """This function queries JPL horizons. Using the current orbital
        elements, and provided a minimum time, maximum time, and time step,
        we can fetch the new table of ephemeris measurements.

        Parameters
        ----------
        start_time : float
            The time that the ephemeris should start at, in Julian days.
        stop_time : float
            The time that the ephemeris should stop at, in Julian days.
        time_step : float
            The time step of the entries of the ephemeris calculation, in
            seconds. (Note, JPL does not accept anything less than a minute.)

        Returns
        -------
        epidermis_table : Table
            The table of computed parameters from JPL horizons.
        """
        # The JPL service does not accept time steps in less than a second
        # and floors at a minute. Minutes are the best unit, so we round to
        # the nearest minute.
        time_step = int(time_step / 60)

        # The entries for JPL Horizon API. The less needed escape
        # characters the better. Strings need to be wrapped for the URI call.
        api_parameters = {
            # Adding a dummy name as this call has no preconceived knowledge of
            # what this asteroid or object is.
            "OBJECT": "OpihiExarata-Small-Body",
            # The location of the observatory, we assume an observatory on 
            # Earth.
            "CENTER": "{code}@399".format(code=library.config.MPC_OBSERVATORY_CODE),
            # Specifying to the JPL system that we are supplying elements, the
            # semicolon must be URI encoded else the system does not 
            # recognize it. Also specifying that our ephemeris calculations 
            # are for an observer.
            "COMMAND": ";",
            "EPHEM_TYPE": "OBSERVER",
            # Formatting the orbital elements and the current ecliptic that
            # we are using as our assumption for the angles.
            "A": self.semimajor_axis,
            "EC": self.eccentricity,
            "IN": self.inclination,
            "OM": self.longitude_ascending_node,
            "W": self.argument_perihelion,
            "MA": self.mean_anomaly,
            "EPOCH": self.epoch,
            "ECLIP": "J2000",
            # Formatting the time parameters.
            "START_TIME": "JD{start}".format(start=start_time),
            "STOP_TIME": "JD{stop}".format(stop=stop_time),
            "STEP_SIZE": "{min}m".format(min=time_step),
            # The output quantities to be extracted from the JPL Horizons
            # service. It is specified by a set of flags. See:
            # https://ssd.jpl.nasa.gov/horizons/manual.html#output
            # We want the ephemeris (1), the on-sky rates (3), with optionally 
            # the true anomaly (41), and vector-form sky motion (47).
            "QUANTITIES": "1,3,41,47",
            # The format that the output will be specified in. There is little
            # difference between JSON and text as it is all just text.
            "format": "text",
        }

        # Constructing the API call. The parameters are delimitated by
        # ampersands. The query character for query is added as well. The
        # requests package handles it well.
        BASE_JPL_HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
        # Sending the request.
        query_result = requests.get(BASE_JPL_HORIZONS_URL, params=api_parameters)

        # Extracting from this result the needed results...
        # TODO
