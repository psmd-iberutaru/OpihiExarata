"""For miscellaneous conversions."""

import numpy as np
import astropy.coordinates as ap_coordinates
import astropy.time as ap_time
import astropy.units as ap_units


def degrees_to_sexagesimal_ra_dec(ra_deg:float, dec_deg:float) -> tuple[str,str]:
    """Convert RA and DEC degree measurements to the more familiar HMSDMS 
    sexagesimal format.

    Parameters
    ----------
    ra_deg : float
        The right ascension in degrees.
    dec_deg : float
        The declination in degrees.

    Returns
    -------
    ra_sex : str
        The right ascension in hour:minute:second sexagesimal.
    dec_sex : str
        The declination in degree:minute:second sexagesimal.
    """
    # Levering Astropy for this.
    skycoord = ap_coordinates.SkyCoord(ra_deg, dec_deg, frame="icrs", unit="deg")
    ra_sex, dec_sex = skycoord.to_string("hmsdms", sep=":").split(" ")
    return ra_sex, dec_sex

def sexagesimal_ra_dec_to_degrees(ra_sex:str, dec_sex:str) -> tuple[float,float]:
    """Convert RA and DEC measurements from the more familiar HMSDMS 
    sexagesimal format to degrees.

    Parameters
    ----------
    ra_sex : str
        The right ascension in hour:minute:second sexagesimal.
    dec_sex : str
        The declination in degree:minute:second sexagesimal.

    Returns
    -------
    ra_deg : float
        The right ascension in degrees.
    dec_deg : float
        The declination in degrees.
    """
    # Levering Astropy for this.
    skycoord = ap_coordinates.SkyCoord(ra_sex, dec_sex, frame="icrs", unit=(ap_units.hourangle, ap_units.deg))
    ra_deg = float(skycoord.ra.degree)
    dec_deg = float(skycoord.dec.degree)
    return ra_deg, dec_deg



def decimal_day_to_unix_time(year: int, month: int, day: float):
    """A function to convert decimal day time formats to UNIX time.

    Parameters
    ----------
    year : int
        The year of the time stamp to be converted.
    month : int
        The month of the time stamp to be converted.
    day : float
        The day of the time stamp to be converted, may be decimal, the
        values are just passed down.

    Returns
    -------
    unix_time : float
        The unix time that the date represents.
    """
    # Determining the true year and letting the remainder flow.
    int_year = np.array(year, dtype=int)
    int_month = np.array(month, dtype=int)
    int_day = np.array(day, dtype=int)
    float_day = np.array(day, dtype=float)
    # Leftover to determine HMS.
    leftover_hours = (float_day % 1) * 24
    # Hours
    int_hour = np.array(leftover_hours, dtype=int)
    leftover_minutes = (leftover_hours % 1) * 60
    # Minutes
    int_minute = np.array(leftover_minutes, dtype=int)
    leftover_seconds = (leftover_minutes % 1) * 60
    # Seconds.
    seconds = leftover_seconds
    # Unix time.
    unix_time = full_date_to_unix_time(
        year=int_year,
        month=int_month,
        day=int_day,
        hour=int_hour,
        minute=int_minute,
        second=seconds,
    )
    return unix_time


def full_date_to_unix_time(
    year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: float = 0
) -> float:
    """A function to convert the a whole date format into UNIX time.

    Parameters
    ----------
    year : int
        The year of the time stamp to be converted.
    month : int
        The month of the time stamp to be converted.
    day : int
        The day of the time stamp to be converted.
    hour : int
        The hour of the time stamp to be converted.
    minute : int
        The minute of the time stamp to be converted.
    second : float
        The second of the time stamp to be converted.

    Returns
    -------
    unix_time : float
        The time input converted into UNIX time.
    """
    time_param = {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second,
    }
    time_instance = ap_time.Time(time_param, scale="utc", format="ymdhms")
    unix_time = time_instance.to_value("unix", subfmt="long")
    return unix_time


def unix_time_to_decimal_day(unix_time:float) -> tuple:
    """A function to convert UNIX time to the decimal day time.


    Parameters
    ----------
    unix_time : float
        The unix time that is going to be converted.

    Returns
    -------
    year : int
        The year of the UNIX time.
    month : int
        The month of the UNIX time.
    day : float
        The day of the the UNIX time, the hours, minute, and seconds are all 
        contained as a decimal.
    """
    # Getting the full date and just converting it from there.
    year, month, int_day, hour, minute, second = unix_time_to_full_date(unix_time=unix_time)
    # Calculating the decimal day.
    day = int_day + hour/24 + minute/1440 + second/86400
    # All done.
    return year, month,day


def unix_time_to_full_date(unix_time:float) -> tuple:
    """A function to convert the a whole date format into UNIX time.

    Parameters
    ----------
    unix_time : float
        The UNIX time which is subject to be input.

    Returns
    -------
    year : int
        The year of the UNIX time provided.
    month : int
        The month of the UNIX time provided.
    day : int
        The day of the UNIX time provided.
    hour : int
        The hour of the UNIX time provided.
    minute : int
        The minute of the UNIX time provided.
    second : float
        The second of the UNIX time provided.
    """
    time_instance = ap_time.Time(unix_time, format="unix")
    # It is faster to not unpack, even though it would be less readable.
    return time_instance.to_value("ymdhms")
