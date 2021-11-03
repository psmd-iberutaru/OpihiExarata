"""A collection of functions to deal with JSON input and handling. For the 
most part, these functions are just wrappers around the built-in JSON handling."""

import json

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


def dictionary_to_json(dictionary: dict) -> str:
    """Converts a Python dictionary to a JSON string.

    Parameters
    ----------
    dictionary : dict
        The Python dictionary which will be converted to a JSON string.

    Returns
    -------
    json_string : str
        The JSON string.
    """
    json_string = json.dumps(dictionary)
    return json_string


def json_to_dictionary(json_string: str) -> dict:
    """Converts a JSON string to a dictionary.

    Parameters
    -------
    json_string : str
        The JSON string.

    Returns
    ----------
    dictionary : dict
        The Python dictionary which will be converted to a JSON string.
    """
    dictionary = json.loads(json_string)
    return dict(dictionary)
