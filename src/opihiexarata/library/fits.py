"""Fits file based operations. These are kind of like convince functions."""

import numpy as np
import astropy.io.fits as ap_fits
import astropy.table as ap_table

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


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
    data : array-like
        The data image of the fits file.
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
