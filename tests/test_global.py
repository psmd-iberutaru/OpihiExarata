"""Tests which do not really match any given function but instead apply 
globally."""

import opihiexarata


def test_true() -> None:
    """This is a test that should always pass. This is just a default test
    to make sure tests runs.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    # Always true test.
    assert_message = "This test should always pass."
    assert True, assert_message
    return None
