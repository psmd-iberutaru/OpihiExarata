"""This is where functions dealing with the temporary files and temporary 
directory of the OpihiExarata system. Temporary files are helpful because they 
may also contain information useful to the user. These functions thus serve the 
same purpose as Python's build-in functions, but it is more restricted to 
OpihiExarata and it is also more persistant."""

import os
import glob

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


def create_temporary_directory() -> None:
    """Make the temporary directory. Fails if the directory already exists.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    directory = os.path.abspath(library.config.TEMPORARY_DIRECTORY)
    if os.path.isdir(directory):
        raise error.DirectoryError(
            "The directory path provided for the temporary directory already exists. A"
            " temporary directory cannot be made. Directory: {dir}".format(
                dir=directory
            )
        )
    else:
        os.makedirs(directory)
    return None


def delete_temporary_directory() -> None:
    """Delete the temporary directory. If the directory does not exist, this
    function will do nothing. If the directory exists, but contains files, then
    this function will fail.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    directory = os.path.abspath(library.config.TEMPORARY_DIRECTORY)
    # Determine if the directory is empty of all useful files.
    try:
        with os.scandir(directory) as temp_dir:
            for entry in temp_dir:
                if entry.is_file():
                    raise error.DirectoryError(
                        "Cannot delete the temporary directory, it contains files."
                        " Purge the temporary directory before deleteing it. Directory:"
                        " {dir}".format(dir=directory)
                    )
    except FileNotFoundError:
        raise error.DirectoryError(
            "The directory cannot be found. The temporary directory cannot be deleted"
            " if it does not exist. Directory: {dir}".format(dir=directory)
        )
    # Otherwise, delete the directory.
    if os.path.isdir(directory):
        os.removedirs(directory)
    else:
        # The directory does not exist, or it is not actually a directory.
        pass
    return None


def purge_temporary_directory() -> None:
    """Delete or purge all files in the temporary directory. This does it
    recursively.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    # List of all of the files.
    directory = os.path.abspath(library.config.TEMPORARY_DIRECTORY)
    file_list = glob.glob(directory, recursive=True)
    # Remove all of the files.
    for filedex in file_list:
        try:
            os.remove(filedex)
        except OSError:
            continue
    # All done.
    return None


def make_temporary_directory_path(filename: str) -> str:
    """Creates a full filename path to use. This function basically adds the
    temporary directory path prefix to place the filename path into it.

    Parameters
    ----------
    filename : string
        The filename of the target to be placed in the temporary directory.

    Returns
    -------
    full_path : string
        The full path of the file, as it would be stored in the temporary
        directory.
    """
    directory = os.path.abspath(library.config.TEMPORARY_DIRECTORY)
    full_path = library.path.merge_pathname(directory=directory, filename=filename)
    return full_path
