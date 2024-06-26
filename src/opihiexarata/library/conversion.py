"""For miscellaneous conversions."""

# isort: split
# Import required to remove circular dependencies from type checking.
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opihiexarata.library import hint
# isort: split

import datetime
import time
import zoneinfo

import astropy.coordinates as ap_coordinates
import astropy.time as ap_time
import astropy.units as ap_units
import numpy as np

from opihiexarata.library import error


def degrees_per_second_to_arcsec_per_second(degree_per_second: float) -> float:
    """This converts from degrees per second to arcseconds per second.

    Parameters
    ----------
    degree_per_second : float
        The value, in degrees per second, which you want to convert from.

    Returns
    -------
    arcsec_per_second : float
        The value, in arcseconds per second, which you converted to.

    """
    # A simple multiplicative conversion.
    arcsec_per_second = degree_per_second * 3600
    return arcsec_per_second


def degrees_to_sexagesimal_ra_dec(
    ra_deg: float,
    dec_deg: float,
    precision: int = 2,
) -> tuple[str, str]:
    """Convert RA and DEC degree measurements to the more familiar HMSDMS
    sexagesimal format.

    Parameters
    ----------
    ra_deg : float
        The right ascension in degrees.
    dec_deg : float
        The declination in degrees.
    precision : int
        The precision of the conversion's seconds term, i.e. how many numbers
        are used.

    Returns
    -------
    ra_sex : str
        The right ascension in hour:minute:second sexagesimal.
    dec_sex : str
        The declination in degree:minute:second sexagesimal.

    """
    # Levering Astropy for this.
    skycoord = ap_coordinates.SkyCoord(
        ra_deg,
        dec_deg,
        frame="icrs",
        unit="deg",
    )
    ra_sex = skycoord.ra.to_string(
        ap_units.hour,
        sep=":",
        pad=True,
        precision=precision,
    )
    dec_sex = skycoord.dec.to_string(
        ap_units.deg,
        sep=":",
        pad=True,
        precision=precision,
        alwayssign=True,
    )
    return ra_sex, dec_sex


def sexagesimal_ra_dec_to_degrees(
    ra_sex: str,
    dec_sex: str,
) -> tuple[float, float]:
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
    skycoord = ap_coordinates.SkyCoord(
        ra_sex,
        dec_sex,
        frame="icrs",
        unit=(ap_units.hourangle, ap_units.deg),
    )
    ra_deg = float(skycoord.ra.degree)
    dec_deg = float(skycoord.dec.degree)
    return ra_deg, dec_deg


def decimal_day_to_julian_day(year: int, month: int, day: float):
    """A function to convert decimal day time formats to the Julian day.

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
    julian_day : float
        The Julian day of the date provided.

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
    # Julian time.
    julian_day = full_date_to_julian_day(
        year=int_year,
        month=int_month,
        day=int_day,
        hour=int_hour,
        minute=int_minute,
        second=seconds,
    )
    return julian_day


def full_date_to_julian_day(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    second: float,
) -> float:
    """A function to convert the a whole date format into the Julian day time.

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
    julian_day : float
        The time input converted into the Julian day.

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
    julian_day = time_instance.to_value("jd", subfmt="long")
    return julian_day


def modified_julian_day_to_julian_day(mjd: float) -> float:
    """A function to convert modified Julian days to Julian days.

    Parameters
    ----------
    mjd : float
        The modified Julian day to be converted to a Julian day.

    Returns
    -------
    jd : float
        The Julian day value after conversion.

    """
    time_instance = ap_time.Time(mjd, format="mjd")
    jd = float(time_instance.to_value("jd", subfmt="float"))
    return jd


def julian_day_to_modified_julian_day(jd: float) -> float:
    """A function to convert Julian days to  modified Julian days.

    Parameters
    ----------
    jd : float
        The Julian day to be converted to a modified Julian day.

    Returns
    -------
    mjd : float
        The modified Julian day value after conversion.

    """
    time_instance = ap_time.Time(jd, format="mjd")
    mjd = float(time_instance.to_value("mjd", subfmt="float"))
    return mjd


def julian_day_to_unix_time(jd: float) -> float:
    """A function to convert between Julian days to UNIX time.

    Parameters
    ----------
    jd : float
        The Julian day to be converted.

    Returns
    -------
    unix_time : float
        The time converted to UNIX time.

    """
    # This could eventually be replaced with multiplication and addition, but
    # this is a convenient way of doing it.
    time_instance = ap_time.Time(jd, format="jd")
    unix_time = np.asarray(time_instance.to_value("unix"))
    return unix_time


def unix_time_to_julian_day(unix_time: float) -> float:
    """A function to convert between julian days to Unix time.

    Parameters
    ----------
    unix_time : float
        The UNIX time to be converted to a Julian day.

    Returns
    -------
    jd : float
        The Julian day value as converted.

    """
    # This could eventually be replaced with multiplication and addition, but
    # this is a convenient way of doing it.
    time_instance = ap_time.Time(unix_time, format="unix")
    jd = np.asarray(time_instance.to_value("jd"))
    return jd


def julian_day_to_decimal_day(jd: float) -> tuple:
    """A function to convert the Julian day time to the decimal day time.

    Parameters
    ----------
    jd : float
        The Julian day time that is going to be converted.

    Returns
    -------
    year : int
        The year of the Julian day time.
    month : int
        The month of the Julian day time.
    day : float
        The day of the the Julian day time, the hours, minute, and seconds are all
        contained as a decimal.

    """
    # Getting the full date and just converting it from there.
    year, month, int_day, hour, minute, second = julian_day_to_full_date(jd=jd)
    # Calculating the decimal day.
    day = int_day + hour / 24 + minute / 1440 + second / 86400
    # All done.
    return year, month, day


def julian_day_to_full_date(jd: float) -> tuple[int, int, int, int, int, float]:
    """A function to convert the Julian day to a full date time.

    Parameters
    ----------
    jd : float
        The Julian day time that is going to be converted.

    Returns
    -------
    year : int
        The year of the Julian day provided.
    month : int
        The month of the Julian day provided.
    day : int
        The day of the Julian day provided.
    hour : int
        The hour of the Julian day provided.
    minute : int
        The minute of the Julian day provided.
    second : float
        The second of the Julian day provided.

    """
    time_instance = ap_time.Time(jd, format="jd")
    # It is faster to not unpack, even though it is less readable.
    return tuple(time_instance.to_value("ymdhms"))


def current_utc_to_julian_day() -> float:
    """Return the current UTC time when this function is called as a Julian day
    time.

    Parameters
    ----------
    None

    Returns
    -------
    current_jd : float
        The current time in Julian date format.

    """
    # We can just derive it from the system UNIX time.
    current_unix_time = time.time()
    current_jd = unix_time_to_julian_day(unix_time=current_unix_time)
    return current_jd


def datetime_timezone_1_to_timezone_2(
    from_datetime: hint.Union[hint.datetime, str],
    from_timezone: str,
    to_timezone: str,
) -> hint.datetime:
    """This function converts a date time from one timezone to another timezone.

    If the datetime provided is a string of an ISO 8601 time, we convert it,
    otherwise, we raise. The timezones provided can be any IANA timezone.

    Parameters
    ----------
    from_datetime : datetime or str
        The data time, or string representation of one to convert.
    from_timezone : str
        The timezone which date_time is currently in.
    to_timezone : str
        The timezone which we are converting to.

    Returns
    -------
    to_datetime : datetime
        The datetime after the conversion.

    """
    # Check if the datetime is really a datetime or a string representation
    # thereof.
    if isinstance(from_datetime, datetime.datetime):
        # All good.
        pass
    elif isinstance(from_datetime, str):
        # Try and convert.
        try:
            from_datetime = datetime.datetime.fromisoformat(from_datetime)
        except ValueError:
            raise error.InputError(
                "The string format of the datetime is not valid and cannot be"
                " converted. We require it to be in an ISO 8601-like format."
                f" The input: {from_datetime}",
            )
    else:
        raise error.InputError(
            "The datetime input provided is neither a datetime or a datetime"
            f" string to be converted. The input: {from_datetime}",
        )

    # Adding the important timezone information, using the built in class.
    from_timezone = zoneinfo.ZoneInfo(key=from_timezone)
    to_timezone = zoneinfo.ZoneInfo(key=to_timezone)
    # Adding it to the datetime.
    from_datetime_zone_aware = datetime.datetime(
        year=from_datetime.year,
        month=from_datetime.month,
        day=from_datetime.day,
        hour=from_datetime.hour,
        minute=from_datetime.minute,
        second=from_datetime.second,
        microsecond=from_datetime.microsecond,
        tzinfo=from_timezone,
    )
    # Converting it to a different timezone.
    to_datetime = from_datetime_zone_aware.astimezone(to_timezone)
    return to_datetime


def string_month_to_number(month_str: str) -> int:
    """A function to convert from the name of a month to the month number.
    This is just because it is easy to have here and to add a package import
    for something like this is silly.

    Parameters
    ----------
    month_str : string
        The month name. If it is exactly three characters in length, we assume
        it is abbreviated month names and search through that instead.

    Returns
    -------
    month_int : int
        The month number integer.

    """
    # Capitalization does not matter.
    month_str = month_str.casefold()
    # There is no real need to import a new package.
    month_dict = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12,
    }
    # It could also be a 3 letter month abbreviation.
    three_letter_month_dict = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }
    if len(month_str) == 3:
        # It is likely a 3 letter month abbreviation, or May.
        month_int = three_letter_month_dict[month_str]
    else:
        month_int = month_dict[month_str]
    return month_int


def filter_header_string_to_filter_name(header_string: str) -> str:
    """The filter position string is exactly how it exists in the header files.
    This converts from the string as it exists in the header file to the filter
    name.
    The filter position set: {0: b, 1: 2, 2: 1, 3: z, 4: i, 5: r, 6: g, 7: c}

    Parameters
    ----------
    header_string : str
        The string as recorded in the header file which describes the filter
        position.

    Returns
    -------
    filter_name : str
        The name of the filter that corresponds to the given filter position.

    """
    # As the filter position string from the camera controller and the
    # corresponding names for OpihiExarata.
    filter_header_string_dictionary = {
        "blank": "b",
        "open2": "2",
        "open": "1",
        "z": "z",
        "i": "i",
        "r": "r",
        "g": "g",
        "clear": "c",
    }
    # Getting the OpihiExarata filter name from the string in the FITS header
    # file. We do not worry about case.
    header_string = header_string.casefold()
    filter_name = filter_header_string_dictionary.get(header_string)
    # Double check that a proper filter name was found from the dictionary.
    if filter_name is None:
        raise error.InputError(
            "The header string provided to determine the filter name is not a"
            f" valid filter name. It was `{header_string}`, supported header"
            f" strings are `{list(filter_header_string_dictionary.keys())}`",
        )
    return filter_name


def numpy_type_string_to_instance(numpy_type_string: str) -> hint.numpy_generic:
    """Provided an input string which is supposed to represent a Numpy type,
    this function provides the type instance itself.

    The main reason for breaking this out into a new function is in the
    event that aliases needs to be made.

    Parameters
    ----------
    numpy_type_string : str
        The Numpy type, provided as a string which is formatted mostly as
        numpy.{type_string}. However, should alias exist, they will also be
        handled.

    Returns
    -------
    numpy_type_instance : Numpy generic
        The data type instance that the string is likely referring to.

    """
    # It is likely easiest to do a falling cascade for both readability and
    # form. We check all of the types to known aliases or results.
    np_t_str = str(numpy_type_string).casefold()
    # Staring with integers.
    if np_t_str in ("short", "int16", "h"):
        numpy_type_instance = np.short
    elif np_t_str in ("intc", "int32", "i") or np_t_str in (
        "int_",
        "int64",
        "intp",
        "l",
    ):
        numpy_type_instance = np.intc
    # Now onto floats.
    elif np_t_str in ("half", "float16", "e"):
        numpy_type_instance = np.half
    elif np_t_str in ("single", "float32", "f"):
        numpy_type_instance = np.single
    elif np_t_str in ("", "double", "float_", "float64", "d"):
        numpy_type_instance = np.double
    elif np_t_str in ("longdouble", "longfloat", "float128", "g"):
        numpy_type_instance = np.longdouble
    # No matching type.
    else:
        # We default to Numpy's default.
        numpy_type_instance = np.float64

    # All done.
    return numpy_type_instance
