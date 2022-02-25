import numpy as np
import os

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


def test_decimal_day_to_unix_time() -> None:
    """Test the conversion from decimal day to UNIX time."""
    # The defining definition of UNIX time.
    origin_unix_time = 0
    test_origin_unix_time = library.conversion.decimal_day_to_unix_time(
        year=1970, month=1, day=1.000
    )
    assert_message = "The epoch UNIX time conversion is not correct."
    assert np.isclose(origin_unix_time, test_origin_unix_time), assert_message

    # A random date.
    tower_unix_time = 1000213382.0
    test_tower_unix_time = library.conversion.decimal_day_to_unix_time(
        year=2001, month=9, day=11.543773148
    )
    assert_message = "The random UNIX time conversion is not correct."
    assert np.isclose(tower_unix_time, test_tower_unix_time), assert_message

    return None


def test_full_date_to_unix_time() -> None:
    """Test the conversion from a full date to UNIX time."""
    # The defining definition of UNIX time.
    origin_unix_time = 0
    test_origin_unix_time = library.conversion.full_date_to_unix_time(
        year=1970, month=1, day=1, hour=0, minute=0, second=0
    )
    assert_message = "The epoch UNIX time conversion is not correct."
    assert np.isclose(origin_unix_time, test_origin_unix_time), assert_message

    # A random date.
    tower_unix_time = 1000212400.0
    test_tower_unix_time = library.conversion.full_date_to_unix_time(
        year=2001, month=9, day=11, hour=12, minute=46, second=40
    )
    assert_message = "The random UNIX time conversion is not correct."
    assert np.isclose(tower_unix_time, test_tower_unix_time), assert_message
    return None
