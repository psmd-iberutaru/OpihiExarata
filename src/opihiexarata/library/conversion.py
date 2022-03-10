"""For miscellaneous conversions."""

import astropy.time as ap_time


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
    int_year = int(year)
    int_month = int(month)
    int_day = int(day)
    # Leftover to determine HMS.
    leftover_hours = (day % 1) * 24
    # Hours
    int_hour = int(leftover_hours)
    leftover_minutes = (leftover_hours % 1) * 60
    # Minutes
    int_minute = int(leftover_minutes)
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
