"""This module is just functions to deal with different common pathname manipulations.
As Exarata is going to be cross platform, this is a nice abstraction."""

import os

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


def get_directory(pathname: str) -> str:
    """Get the directory from the pathname without the file or the extension.

    Parameters
    ----------
    pathname : string
        The pathname which the directory will be extracted.

    Returns
    -------
    directory : string
        The directory which belongs to the pathname.
    """
    directory = os.path.dirname(pathname)
    return directory


def get_filename_without_extension(pathname: str) -> str:
    """Get the filename from the pathname without the file extension.

    Parameters
    ----------
    pathname : string
        The pathname which the filename will be extracted.

    Returns
    -------
    filename : string
        The filename without the file extension.
    """
    # In the event that there are more than one period in the full filename.
    file_components = os.path.basename(pathname).split(".")[:-1]
    filename = "".join(file_components)
    return filename


def get_filename_with_extension(pathname: str) -> str:
    """Get the filename from the pathname with the file extension.

    Parameters
    ----------
    pathname : string
        The pathname which the filename will be extracted.

    Returns
    -------
    filename : string
        The filename with the file extension.
    """
    return os.path.basename(pathname)


def get_file_extension(pathname: str) -> str:
    """Get the file extension only from the pathname.

    Parameters
    ----------
    pathname : string
        The pathname which the file extension will be extracted.

    Returns
    -------
    extension : string
        The file extension only.
    """
    extension = os.path.basename(pathname).split(".")[-1]
    return extension


def merge_pathname(
    directory: hint.Union[str, list] = None, filename: str = None, extension: str = None
) -> str:
    """Joins directories, filenames, and file extensions into one pathname.

    Parameters
    ----------
    directory : string or list
        The directory(s) which is going to be used. If it is a list,
        then the paths within it are combined.
    filename : string
        The filename that is going to be used for path construction.
    extension : string
        The filename extension that is going to be used.

    Returns
    -------
    pathname : string
        The combined pathname.
    """
    # Combine the directories if it is a list.
    directory = directory if directory is not None else ""
    directory = directory if isinstance(directory, (list, tuple)) else [str(directory)]
    total_directory = os.path.join(*directory)
    # Filename.
    filename = filename if filename is not None else ""
    # File extension.
    extension = extension if extension is not None else ""
    # Combining them into one path.
    filename_extension = filename + "." + extension
    pathname = os.path.join(total_directory, filename_extension)
    return pathname


def split_pathname(pathname: str) -> tuple[str, str, str]:
    """Splits a path into a directory, filename, and file extension.

    This is a wrapper function around the more elementry functions
    `get_directory`, `get_filename_without_extension`, and
    `get_file_extension`.

    Parameters
    ----------
    pathname : string
        The combined pathname which to be split.

    Returns
    -------
    directory : string
        The directory which was split from the pathname.
    filename : string
        The filename which was split from the pathname.
    extension : string
        The filename extension which was split from the pathname.
    """
    directory = get_directory(pathname=pathname)
    filename = get_filename_without_extension(pathname=pathname)
    extension = get_file_extension(pathname=pathname)
    return directory, filename, extension
