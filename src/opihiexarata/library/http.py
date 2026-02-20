"""Functions and methods which allow for ease of interacting with web based
resources. Included here are functions which download files, query web resources
and other things. This interacts mostly with HTTP based services.
"""

import os
import shutil
import time
import urllib.request

import requests

from opihiexarata import library
from opihiexarata.library import error


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


def download_file_from_url(
    url: str,
    filename: str,
    http_headers: dict = {},
    overwrite: bool = False,
) -> None:
    """Download a file from a URL to disk.

    ..warning:: The backend of this function relies on a function which may be
    depreciated in the future. This function may need to be rewritten.

    Parameters
    ----------
    url : string
        The url which the file will be downloaded from.
    filename : string
        The filename where the file will be saved.
    http_headers : dict
        If provided, the HTTP headers are tacked along for the ride.
    overwrite : bool, default = False
        If the file already exists, overwrite it. If False, it would raise
        an error instead.

    """
    # Sensible defaults for the headers. Common web crawler blockers check for
    # these and adding them is useful.
    default_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0"
        ),
    }
    using_headers = {**http_headers, **default_headers}
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
                f"The filename provided already exists: \n {filename}",
            )
    # Save the file. We supply here two methods in the event the first really
    # does get removed.
    try:
        with requests.get(url, headers=using_headers, stream=True) as req:
            try:
                req.raise_for_status()
            except requests.HTTPError:
                # We just detail it a bit more.
                raise error.InputError(
                    "Downloading file from URL returned an HTTP error.",
                )
            # Otherwise...
            with open(filename, "wb") as file:
                file.writelines(req.iter_content(chunk_size=8192))
    except Exception:
        # Alternative method.
        with (
            urllib.request.urlopen(url) as in_stream,
            open(filename, "wb") as out_file,
        ):
            shutil.copyfileobj(in_stream, out_file)
