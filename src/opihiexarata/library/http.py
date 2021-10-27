"""Functions and methods which allow for ease of interacting with web based
resources. Included here are functions which download files, query web resources
and other things. This interacts mostly with HTTP based services."""

import os
import urllib.request
import shutil

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

def download_file_from_url(url:str, filename:str, overwrite:bool=False)-> None:
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
            raise error.FileError("The filename provided already exists: \n {fname}".format(fname=filename))
    # Save the file. We supply here two methods in the event the first really
    # does get removed.
    try:
        urllib.request.urlretrieve(url, filename)
    except Exception:
        # Alternative method.
        with urllib.request.urlopen(url) as in_stream, open(filename, 'wb') as out_file:
            shutil.copyfileobj(in_stream, out_file)
    return None