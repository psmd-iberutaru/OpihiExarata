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
