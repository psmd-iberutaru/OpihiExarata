"""Functions and methods which allow for ease of interacting with web based
resources. Included here are functions which download files, query web resources
and other things. This interacts mostly with HTTP based services."""

import os
import shutil
import time
import urllib.request
import requests

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


def get_http_status_code(url: str) -> int:
    """This gets the http status code of a web resource.

    Parameters
    ----------
    url : string
        The url which the http status code will try and obtain.

    Return
    ------
    status_code : int
        The status code.
    """
    web_request = requests.get(url)
    status_code = web_request.status_code
    return status_code


def api_request_sleep(seconds: float = None) -> None:
    """Sleep for the time, specified in the configuration file, for API
    requests. This function exists to ensure uniformity in application.

    Parameters
    ----------
    seconds : float, default = None
        The number of seconds that the program should sleep for. If not
        provided, then it defaults to the configuration value.

    Results
    -------
    None
    """
    SLEEP_SECONDS = library.config.API_CONNECTION_REQUEST_SLEEP_SECONDS
    seconds = seconds if seconds is not None else SLEEP_SECONDS
    time.sleep(seconds)
    return None


def download_file_from_url(url: str, filename: str, overwrite: bool = False) -> None:
    """Download a file from a URL to disk.

    ..warning:: The backend of this function relies on a function which may be
    depreciated in the future. This function may need to be rewritten.

    Parameters
    ----------
    url : string
        The url which the file will be downloaded from.
    filename : string
        The filename where the file will be saved.
    overwrite : bool, default = False
        If the file already exists, overwrite it. If False, it would raise
        an error instead.
    """
    # See if the file exists, if so, delete it if overwrite is True, to simulate
    # overwriting the file.
    if os.path.isfile(filename):
        # The file exists. Check if it should be overridden or not.
        if overwrite:
            # Overwrite the file, mostly by deleting it then writing to disk.
            os.remove(filename)
        else:
            # Cannot overwrite file.
            raise error.FileError(
                "The filename provided already exists: \n {fname}".format(
                    fname=filename
                )
            )
    # Save the file. We supply here two methods in the event the first really
    # does get removed.
    try:
        urllib.request.urlretrieve(url, filename)
    except Exception:
        # Alternative method.
        with urllib.request.urlopen(url) as in_stream, open(filename, "wb") as out_file:
            shutil.copyfileobj(in_stream, out_file)
    return None
