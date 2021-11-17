"""Fits file based operations. These are kind of like convince functions."""

import numpy as np
import astropy.io.fits as ap_fits
import astropy.table as ap_table

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


def read_fits_header(filename: str, extension: hint.Union[int, str] = 0) -> hint.Header:
    """This reads the header of fits files only. This should be used only if
    there is no data.

    Really, this is just a wrapper around Astropy, but it is made for
    consistency and to avoid the usage of the convince functions.

    Parameters
    ----------
    filename : string
        The filename that the fits image file is at.
    extension : int or string, default = 0
        The fits extension that is desired to be opened.

    Returns
    -------
    header : Astropy Header
        The header of the fits file.
    """
    with ap_fits.open(filename) as hdul:
        hdu = hdul[extension].copy()
        header = hdu.header
        data = hdu.data
    # Check that the data does not exist, so the data read should be none.
    if data is not None:
        raise error.FileError(
            "This function is designed to read headers of fits files only, and thus the"
            " data of this fits file or extension is expected to be None, nothing."
        )
    return header


def read_fits_image_file(
    filename: str, extension: hint.Union[int, str] = 0
) -> tuple[hint.Header, hint.ArrayLike]:
    """This reads fits files, assuming that the fits file is an image. It is a
    wrapper function around the astropy functions.

    Parameters
    ----------
    filename : string
        The filename that the fits image file is at.
    extension : int or string, default = 0
        The fits extension that is desired to be opened.

    Returns
    -------
    header : Astropy Header
        The header of the fits file.
    """
    with ap_fits.open(filename) as hdul:
        hdu = hdul[extension].copy()
        header = hdu.header
        data = hdu.data
    # Check that the data really is an image.
    if not isinstance(data, np.ndarray):
        raise error.FileError(
            "This function is designed to read image fits files, and thus the data of"
            " this fits file or extension is expected to be array-like."
        )
    return header, data


def read_fits_table_file(
    filename: str, extension: hint.Union[int, str] = 0
) -> tuple[hint.Header, hint.Table]:
    """This reads fits files, assuming that the fits file is a binary table.
    It is a wrapper function around the astropy functions.

    Parameters
    ----------
    filename : string
        The filename that the fits image file is at.
    extension : int or string, default = 0
        The fits extension that is desired to be opened.

    Returns
    -------
    header : Astropy Header
        The header of the fits file.
    table : Astropy Table
        The data table of the fits file.
    """
    with ap_fits.open(filename) as hdul:
        hdu = hdul[extension].copy()
        header = hdu.header
        data = hdu.data
    # Check that the data really is table-like.
    if not isinstance(data, (ap_table.Table, ap_fits.FITS_rec)):
        raise error.FileError(
            "This function is designed to read binary table fits files, and thus the"
            " data of this fits file or extension is expected to be a table."
        )
    else:
        # The return is specified to be an astropy table.
        table = ap_table.Table(data)
    return header, table


def write_fits_image_file(
    filename: str, header: hint.Header, data: hint.ArrayLike, overwrite: bool = False
) -> None:
    """This writes fits image files to disk. Acting as a wrapper around the
    fits functionality of astropy.

    Parameters
    ----------
    filename : string
        The filename that the fits image file will be written to.
    header : Astropy Header
        The header of the fits file.
    data : array-like
        The data image of the fits file.
    overwrite : boolean, default = False
        Decides if to overwrite the file if it already exists.

    Returns
    -------
    None
    """
    # Type checking, ensuring that this function is being used for images only.
    if not isinstance(header, (dict, ap_fits.Header)):
        raise error.InputError(
            "The header must either be an astropy Header class or something convertable"
            " to it."
        )
    if not isinstance(data, np.ndarray):
        raise error.InputError(
            "The data must be an image-like object, stored as a Numpy array."
        )
    # Create the image and add the header.
    hdu = ap_fits.PrimaryHDU(data=data, header=header)
    # Write.
    hdu.writeto(filename, overwrite=overwrite)
    return None


def write_fits_table_file(
    filename: str, header: hint.Header, data: hint.Table, overwrite: bool = False
) -> None:
    """This writes fits table files to disk. Acting as a wrapper around the
    fits functionality of astropy.

    Parameters
    ----------
    filename : string
        The filename that the fits image file will be written to.
    header : Astropy Header
        The header of the fits file.
    data : Astropy Table
        The data table of the table file.
    overwrite : boolean, default = False
        Decides if to overwrite the file if it already exists.

    Returns
    -------
    None
    """
    # Type checking, ensuring that this function is being used for images only.
    if not isinstance(header, (dict, ap_fits.Header)):
        raise error.InputError(
            "The header must either be an astropy Header class or something convertable"
            " to it."
        )
    if not isinstance(data, (ap_table.Table, ap_fits.FITS_rec)):
        raise error.InputError("The data must be an table-like object.")
    # Create the table data
    binary_table = ap_fits.BinTableHDU(data=data, header=header)
    # Write.
    binary_table.writeto(filename, overwrite=overwrite)
    return None
