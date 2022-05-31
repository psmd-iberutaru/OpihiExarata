import numpy as np
import os


import opihiexarata


def test_decimal_day_to_julian_day() -> None:
    """Test the conversion from decimal day to Julian days."""
    # A defining definition of Julian days.
    origin_julian_day = 2400000
    test_origin_julian = opihiexarata.library.conversion.decimal_day_to_julian_day(
        year=1858, month=11, day=16.5
    )
    assert_message = "The definition Julian day conversion is not correct."
    assert np.isclose(origin_julian_day, test_origin_julian), assert_message

    # A random date.
    tower_julian_day = 2452164.0437731
    test_tower_julian_day = opihiexarata.library.conversion.decimal_day_to_julian_day(
        year=2001, month=9, day=11.543773148
    )
    assert_message = "The random Julian day conversion is not correct."
    assert np.isclose(tower_julian_day, test_tower_julian_day), assert_message

    return None

def test_full_date_to_julian_day() -> None:
    """Test the conversion from a full date to Julian days."""
    # A defining definition of Julian time.
    origin_julian_day = 2400000
    test_origin_julian_day = opihiexarata.library.conversion.full_date_to_julian_day(
        year=1858, month=11, day=16, hour=12, minute=0, second=0
    )
    assert_message = "The definition Julian day conversion is not correct."
    assert np.isclose(origin_julian_day, test_origin_julian_day), assert_message

    # A random date.
    tower_julian_day = 2452164.0324074
    test_tower_julian_day = opihiexarata.library.conversion.full_date_to_julian_day(
        year=2001, month=9, day=11, hour=12, minute=46, second=40
    )
    assert_message = "The random Julian day conversion is not correct."
    assert np.isclose(tower_julian_day, test_tower_julian_day), assert_message
    return None
