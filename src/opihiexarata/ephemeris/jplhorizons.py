"""The different ephemeris engines which use JPL horizons as its backend."""

import requests
import numpy as np
import scipy.interpolate as sp_interpolate
import astropy.table as ap_table

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
    ra_velocity : float
        The right ascension angular velocity of the target, in degrees per
        second.
    dec_velocity : float
        The declination angular velocity of the target, in degrees per
        second.
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

        # We adapt the internal time for accurate ephemeris, this is done so
        # we do not request too much data. Using sensible defaults.
        current_time = library.conversion.current_utc_to_julian_day()
        self.start_time = current_time - ((15 / 60) / 24)
        self.stop_time = current_time + ((30 / 60) / 24)
        self.time_step = 60

        # Extracting the first pass ephemeris table. The ephemeris function
        # uses this table to properly compute the future locations.
        __ = self._refresh_ephemeris(
            start_time=self.start_time, stop_time=self.stop_time
        )

        # The rates of the asteroid. We care only about the rates most
        # accurate to the current time and so we can use the rates calculated
        # from the close by default time.
        ra_rate = np.nanmean(self.ephemeris_table["ra_rate"])
        dec_rate = np.nanmean(self.ephemeris_table["dec_rate"])
        # The rates from JPL are in arcseconds per hour. Convention for this
        # software is degrees per second, converting.
        as_hr_to_dg_s = lambda ashr: ashr / (3600 * 3600)
        self.ra_velocity = as_hr_to_dg_s(ra_rate)
        self.dec_velocity = as_hr_to_dg_s(dec_rate)

        # All done.
        return None

    @staticmethod
    def __parse_jpl_horizons_output(response_text: str) -> hint.Table:
        """This function serves to parse the output from the JPL horizons. It
        is a text output that is human readable but some parsing is needed.
        We do that here, assuming the quantities in the original request.

        Parameters
        ----------
        response_text : str
            The raw response from the JPL horizons web API service.

        Returns
        -------
        """
        # Using lines is a lot easier to manage.
        response_lines = response_text.split("\n")
        # The ephemeris lines are demarked by $$SOE and $$EOE tags, extracting the
        # ephemeris only as that is what we care about.
        soe_index = None
        eoe_index = None
        for index, linedex in enumerate(response_lines):
            if "$$SOE" in linedex:
                soe_index = index
            elif "$$EOE" in linedex:
                eoe_index = index
            else:
                continue
        # Using the demarcations to extract the ephemeris section of the query lines.
        # We do not need the demarcations themselves though.
        ephemeris_lines = response_lines[soe_index + 1 : eoe_index]

        # Parsing the lines individually.
        def _parse_jpl_horizons_ephemeris_line(line: str) -> dict:
            """We parse the line into the known parts based on the query."""
            # Removing extra spaces which might cause issues.
            line = line.strip()
            # The solar presence is not really relevant and because of its formatting,
            # screws up with the delimitation as "nighttime" is denoted by a space
            # character. We remove it here.
            line_nosun = line[:25] + "    " + line[29:]

            # Splitting it into different parts.
            line_split = line_nosun.split()
            # ...and dealing with the parts.
            # The date of the observation location, the month is in text form but
            # it is easier to deal with numbers.
            date = line_split[0]
            year, month_name, day = date.split("-")
            year = int(year)
            month = library.conversion.string_month_to_number(month_name)
            day = int(day)
            # The time of the observation location.
            time = line_split[1]
            hour, minute, second = time.split(":")
            hour = int(hour)
            minute = int(minute)
            second = float(second)
            # The RA and DEC strings are split because of the deliminator being spaces.
            # combine them back to HMS and DMS.
            ra_sex = line_split[2] + ":" + line_split[3] + ":" + line_split[4]
            dec_sex = line_split[5] + ":" + line_split[6] + ":" + line_split[7]
            ra_deg, dec_deg = library.conversion.sexagesimal_ra_dec_to_degrees(
                ra_sex=ra_sex, dec_sex=dec_sex
            )
            # The RA and DEC rates; these values are in arcsec/hr, but convention in this
            # software is arcsec/sec so convert. The flat planar conversion is already
            # done by Horizon.
            ra_rate = float(line_split[8]) / 3600
            dec_rate = float(line_split[9]) / 3600
            # The true anomaly.
            true_anomaly = float(line_split[10])
            # The exact usage of these parameters are really not know yet but they seem
            # useful; not using any of that.
            sky_motion = float(line_split[11])
            sky_position_angle = float(line_split[12])
            sky_velocity_angle = float(line_split[13])

            # From the current date and time, deriving the julian day. It
            # is useful for all of the other calculations.
            julian_day = library.conversion.full_date_to_julian_day(
                year=year, month=month, day=day, hour=hour, minute=minute, second=second
            )

            # Compiling the dictionary.
            line_dict = {
                "year": year,
                "month": month,
                "day": day,
                "hour": hour,
                "minute": minute,
                "second": second,
                "julian_day": julian_day,
                "ra": ra_deg,
                "dec": dec_deg,
                "ra_rate": ra_rate,
                "dec_rate": dec_rate,
                "true_anomaly": true_anomaly,
            }
            return line_dict

        # Using the above abstracted function for parsing the individual lines.
        ephemeris_table = []
        for linedex in ephemeris_lines:
            ephemeris_record = _parse_jpl_horizons_ephemeris_line(line=linedex)
            ephemeris_table.append(ephemeris_record)
        ephemeris_table = ap_table.Table(ephemeris_table)

        # All done.
        return ephemeris_table

    def _refresh_ephemeris(
        self, start_time: float = None, stop_time: float = None, time_step: float = None
    ) -> None:
        """This function refreshes the calculations rederiving the solution
        table and the ephemeris function.

        Parameters
        ----------
        start_time : float, default = None
            The time that the ephemeris should start at, in Julian days. If
            not provided, then the old start time will be used instead.
        stop_time : float, default = None
            The time that the ephemeris should stop at, in Julian days. If
            not provided, then the old stop time will be used instead.
        time_step : float, default = None
            The time step of the entries of the ephemeris calculation, in
            seconds. (Note, JPL does not accept anything less than a minute.)
            If not provided, then the old time step will be used instead.

        Returns
        -------
        None
        """
        # If the values provided do not really differ from what we have now,
        # then it would be a lot of work for nothing.
        if (start_time is None) and (stop_time is None) and (time_step is None):
            # Doing no work.
            return None
        else:
            # Assign refreshed values to the current instance to do the work.
            self.start_time = self.start_time if start_time is None else start_time
            self.stop_time = self.stop_time if stop_time is None else stop_time
            self.time_step = self.time_step if time_step is None else time_step

        # Requery the Horizons service.
        ephemeris_table = self._query_jpl_horizons(
            start_time=self.start_time,
            stop_time=self.stop_time,
            time_step=self.time_step,
        )
        self.ephemeris_table = ephemeris_table

        # All done.
        return None

    def _query_jpl_horizons(
        self, start_time: float, stop_time: float, time_step: float
    ) -> hint.Table:
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
            The table of computed sky locations over time from JPL horizons.
        """
        # The JPL service does not accept time steps in less than a second
        # and floors at a minute. Minutes are the best unit, so we round to
        # the nearest minute.
        time_step_minute = int(time_step / 60)

        # The entries for JPL Horizon API. The less needed escape
        # characters the better. Strings need to be wrapped for the URI call.
        query_parameters = {
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
            "STEP_SIZE": "{min}m".format(min=time_step_minute),
            # The output quantities to be extracted from the JPL Horizons
            # service. It is specified by a set of flags. See:
            # https://ssd.jpl.nasa.gov/horizons/manual.html#output
            # We want the ephemeris (1), the on-sky rates (3), with optionally
            # the true anomaly (41), and vector-form sky motion (47).
            "QUANTITIES": "1,3,41,47",
            # The output of the time should include seconds, just in case given
            # the current parser assumes hardcoded column positions.
            "TIME_DIGITS": "seconds",
            # The format that the output will be specified in. There is little
            # difference between JSON and text as it is all just text.
            "format": "text",
        }

        # Constructing the API call. The parameters are delimitated by
        # ampersands. The query character for query is added as well. The
        # requests package handles it well.
        BASE_JPL_HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
        # Sending the request, characters are properly encoded here.
        response = requests.get(BASE_JPL_HORIZONS_URL, params=query_parameters)
        result = response.text

        # Extracting from this result the needed results.
        ephemeris_table = self.__parse_jpl_horizons_output(response_text=result)
        return ephemeris_table

    def forward_ephemeris(self, future_time: float) -> tuple[float, float]:
        """This allows the computation of future positions at a future time
        using the derived ephemeris.

        Parameters
        ----------
        future_time : array-like
            The set of future times which to derive new RA and DEC coordinates.
            The time must be in Julian day time.

        Returns
        -------
        future_ra : ndarray
            The set of right ascensions that corresponds to the future times,
            in degrees.
        future_dec : ndarray
            The set of declinations that corresponds to the future times, in
            degrees.
        """
        # If any of the future time is outside of the current times provided
        # by the ephemeris table, then more data needs to be obtained. We
        # do not propagate or extrapolate.
        future_time = np.array(future_time)
        if not np.all(
            np.logical_and(self.start_time < future_time, future_time < self.stop_time)
        ):
            # New data to be queried. Establishing it so that the bounds are
            # set by the new time requested plus a buffer of a few minutes.
            buffer_time = 5 / (24 * 60)
            future_start_time = np.nanmin(future_time) - buffer_time
            future_stop_time = np.nanmax(future_time) + buffer_time
            # We do not want to reduce the current table we have, use the
            # previous values where needed.
            new_start_time = (
                self.start_time
                if self.start_time < future_start_time
                else future_start_time
            )
            new_stop_time = (
                future_stop_time
                if self.stop_time < future_stop_time
                else self.stop_time
            )
            # Refreshing the ephemeris data.
            self._refresh_ephemeris(start_time=new_start_time, stop_time=new_stop_time)
            # Attempt to compute the forward ephemeris data now with the
            # updated information.
            return self.forward_ephemeris(future_time=future_time)

        # It is unlikely that the ephemeris table has the exact data points,
        # so we interpolate.
        ra_interpolate = sp_interpolate.interp1d(
            self.ephemeris_table["julian_day"],
            self.ephemeris_table["ra"],
            kind="quadratic",
            bounds_error=True,
        )
        dec_interpolate = sp_interpolate.interp1d(
            self.ephemeris_table["julian_day"],
            self.ephemeris_table["dec"],
            kind="quadratic",
            bounds_error=True,
        )
        # Computing the interpolation. If for some reason it is outside of the
        # bounds again, something is off. As such, we make sure it is not
        # caught with other error catching systems.
        try:
            future_ra = ra_interpolate(future_time)
            future_dec = dec_interpolate(future_time)
        except ValueError:
            raise error.DevelopmentError(
                "The ephemeris interpolation functions are trying to interpolate"
                " outside of their defined range. However, this should have already"
                " been caught with the time bounds check and a new queried ephemeris"
                " table should have fixed this issue."
            )
        else:
            # All done, seem to be fine.
            return future_ra, future_dec
        # The code should not reach here.
        raise error.LogicFlowError
        return None
