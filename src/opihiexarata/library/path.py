"""This module is just functions to deal with different common pathname manipulations.
As Exarata is going to be cross platform, this is a nice abstraction."""

import os
import glob
import copy

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


def get_most_recent_filename_in_directory(
    directory: str,
    extension: hint.Union[str, list] = None,
    recency_function: hint.Callable[[str], float] = None,
    exclude_opihiexarata_output_files: bool = False,
) -> str:
    """This gets the most recent filename from a directory.

    Because of issues with different operating systems having differing
    issues with storing the creation time of a file, this function sorts based
    off of modification time.

    Parameters
    ----------
    directory : string
        The directory by which the most recent file will be derived from.
    extension : string or list, default = None
        The extension by which to filter for. It is often the case that some
        files are created but the most recent file of some type is desired.
        Only files which match the included extensions will be considered.
    recency_function : callable, default = None
        A function which, when provided, provides a sorting index for a given
        filename. This is used when the default sorting method (modification
        time) is not desired and a custom function can be provided here. The
        larger the value returned by this function, the more "recent" a
        given file will be considered to be.
    exclude_opihiexarata_output_files : boolean, default = False
        If True, files which have been marked as being outputs of OpihiExarata
        (via the file suffixes as per the configuration file) will not be
        included.

    Returns
    -------
    recent_filename : string
        The filename of the most recent file, by modification time, in the
        directory.
    """
    # Check if the directory provided actually exists.
    if not os.path.isdir(directory):
        raise error.InputError(
            "The directory provided `{d}` does not exist. A most recent file cannot be"
            " obtained.".format(d=str(directory))
        )

    # The default recency function, if not provided, is the modification times
    # of the files themselves.
    recency_function = (
        os.path.getmtime if recency_function is None else recency_function
    )

    # We need to check all of the files matching the provided extension. If
    # none was provided, we use all.
    extension = "*" if extension is None else extension
    extension_list = (extension,) if isinstance(extension, str) else tuple(extension)
    matching_filenames = []
    for extensiondex in extension_list:
        # If the extension has a leading dot, then we remove it as it
        # is already assumed.
        if extensiondex.startswith("."):
            extensiondex = extensiondex[1:]
        # Fetch all of the matching files within the directory. We only want
        # files within the directory, not above or below.
        pathname_glob_filter = merge_pathname(
            directory=directory, filename="*", extension=extensiondex
        )
        extension_matching_files = glob.glob(pathname_glob_filter, recursive=False)
        matching_filenames += extension_matching_files

    # If flagged, we do not include files which have been marked as outputs
    # of OpihiExarata.
    if exclude_opihiexarata_output_files:
        # Mark for files which have been preprocessed.
        PREPROCESS_SUFFIX = library.config.PREPROCESS_DEFAULT_SAVING_SUFFIX
        SOLUTION_SUFFIX = library.config.GUI_MANUAL_DEFAULT_FITS_SAVING_SUFFIX
        MPCRECORD_SUFFIX = library.config.GUI_MANUAL_DEFAULT_MPC_RECORD_SAVING_SUFFIX
        for filenamedex in copy.deepcopy(matching_filenames):
            if (
                (PREPROCESS_SUFFIX in filenamedex)
                or (SOLUTION_SUFFIX in filenamedex)
                or (MPCRECORD_SUFFIX in filenamedex)
            ):
                matching_filenames.remove(filenamedex)
            # Also check the .FITS variant.
            elif (
                (PREPROCESS_SUFFIX + ".fits" in filenamedex)
                or (SOLUTION_SUFFIX + ".fits" in filenamedex)
                or (MPCRECORD_SUFFIX + ".fits" in filenamedex)
            ):
                matching_filenames.remove(filenamedex)


    # For all of the matching filenames, we need to find the most recent via
    # the modification time. Given that the modification times are a UNIX time,
    # the largest is the most recent.
    recent_filename = max(matching_filenames, key=lambda f: recency_function(f))
    # Just a quick check to make sure the file exists.
    if not os.path.isfile(recent_filename):
        raise error.DevelopmentError(
            "For some reason, the detected most recent file is not actually a file."
            " Something is wrong."
        )
    return recent_filename


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
    # We only remove last one as is the conventions for extensions.
    file_components = os.path.basename(pathname).split(".")[:-1]
    filename = ".".join(file_components)
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
    directory : string or list, default = None
        The directory(s) which is going to be used. If it is a list,
        then the paths within it are combined.
    filename : string, default = None
        The filename that is going to be used for path construction.
    extension : string, default = None
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
    if extension == "":
        filename_extension = filename
    else:
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
