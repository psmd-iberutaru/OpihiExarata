"""Fits file based operations. These are kind of like convince functions."""

import copy

import numpy as np
import astropy.io.fits as ap_fits
import astropy.table as ap_table

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

# This is structured as {key:(default, comment)}.
_OPIHIEXARATA_HEADER_KEYWORDS_DICTIONARY = {
    # Beginning.
    "OX_BEGIN": (True, "OX: If True, image has been processed by OpihiExarata (OX)."),
    # Target/asteroid information; T.
    "OXT_PX_X": (None, "OX: The X pixel location of the target/asteroid in the image."),
    "OXT_PX_Y": (None, "OX: The Y pixel location of the target/asteroid in the image."),
    "OXT___RA": (None, "OX: The RA of the target or asteroid in the image."),
    "OXT__DEC": (None, "OX: The DEC of the target or asteroid in the image."),
    # Metadata; M.
    "OXM_ORFN": (None, "OX: The original filename of the FITS file read."),
    "OXM_REDU": (False, "OX: If True, this array has been preprocessed/reduced."),
    # Astrometry; A.
    "OXA_SLVD": (False, "OX: If True, the astrometry for this image has been solved."),
    "OXA__ENG": (None, "OX: The used astrometric engine to solve for the astrometry."),
    "OXA___RA": (None, "OX: The RA of the center of the image from astrometry."),
    "OXA__DEC": (None, "OX: The DEC of the center of the image from astrometry."),
    "OXA_ANGL": (None, "OX: The orientation of the image from astrometry, degree."),
    "OXA_RADI": (None, "OX: The radius of the image."),
    "OXA_PXSC": (None, "OX: The pixel scale of the image, arcsec/pixel."),
    # Photometry; P.
    "OXP_SLVD": (False, "OX: If True, the photometry for this image has been solved."),
    "OXP__ENG": (None, "OX: The used photometric engine to solve for the photometry."),
    "OXP_FILT": (None, "OX: The name of the filter based on the filter position."),
    "OXPSKYCT": (None, "OX: The average sky counts per pixel of the image."),
    "OXP_ZP_M": (None, "OX: The zero point magnitude of the image for the filter."),
    "OXP_ZP_E": (None, "OX: The error on the zero point magnitude of the image."),
    # Orbital elements; O.
    "OXO_SLVD": (False, "OX: If True, the orbital for the target has been solved."),
    "OXO__ENG": (None, "OX: The used orbit engine to solve for the orbital elements."),
    "OXO_A__S": (None, "OX: The solved semi-major axis of the orbit, AU."),
    "OXO_E__S": (None, "OX: The solved eccentricity of the orbit, 1."),
    "OXO_IN_S": (None, "OX: The solved inclination angle of the orbit, degree."),
    "OXO_OM_S": (None, "OX: The solved ascending node of the orbit, degree."),
    "OXO__W_S": (None, "OX: The solved perihelion of the orbit, degree."),
    "OXO_MA_S": (None, "OX: The solved mean anomaly of the orbit, degree."),
    "OXO_EA_D": (None, "OX: The derived eccentric anomaly of the orbit, degree."),
    "OXO_TA_D": (None, "OX: The derived true anomaly of the orbit, degree."),
    "OXO_A__E": (None, "OX: The error on the semi-major axis, AU."),
    "OXO_E__E": (None, "OX: The error on the eccentricity, 1."),
    "OXO_IN_E": (None, "OX: The error on the inclination angle, degree."),
    "OXO_OM_E": (None, "OX: The error on the ascending node, degree."),
    "OXO__W_E": (None, "OX: The error on the perihelion, degree."),
    "OXO_MA_E": (None, "OX: The error on the mean anomaly, degree."),
    "OXO_EA_E": (None, "OX: The error on the eccentric anomaly, degree."),
    "OXO_TA_E": (None, "OX: The error on the true anomaly, degree."),
    "OXO_EPCH": (None, "OX: The epoch of the orbital elements, Julia days."),
    # Ephemeris; E.
    "OXE_SLVD": (False, "OX: If True, the ephemeris for the target has been solved."),
    "OXE__ENG": (None, "OX: The used ephemeris engine to solve for the ephemeris."),
    "OXE_RA_V": (None, "OX: The ephemeris 1st order (vel.) rate for RA, arcsec/s."),
    "OXE_DECV": (None, "OX: The ephemeris 1st order (vel.) rate for DEC, arcsec/s."),
    "OXE_RA_A": (None, "OX: The ephemeris 2nd order (accel.) rate for RA, arcsec/s^2."),
    "OXE_DECA": (None, "OX: The ephemeris 2nd order (accel.) rate for DEC, arcsec/s^2."),
    # Propagation; R.
    "OXR_SLVD": (False, "OX: If True, the propagation for the target has been solved."),
    "OXR__ENG": (None, "OX: The used propagation engine to solve for the propagation."),
    "OXR_RA_V": (None, "OX: The propagate 1st order (vel.) rate for RA, arcsec/s."),
    "OXR_DECV": (None, "OX: The propagate 1st order (vel.) rate for DEC, arcsec/s."),
    "OXR_RA_A": (None, "OX: The propagate 2nd order (accel.) rate for RA, arcsec/s^2."),
    "OXR_DECA": (None, "OX: The propagate 2nd order (accel.) rate for DEC, arcsec/s^2."),
    # End.
    "OX___END": (False, "OX: If True, saving this file had no errors."),
}


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


def update_opihiexarata_fits_header(
    header: hint.Header,
    entries: dict,
) -> hint.Header:
    """This appends entries from a dictionary to an Astropy header.

    This function is specifically for OpihiExarata data entries. All other 
    entries or header keyword value pairs are ignored. The OpihiExarata 
    results (or header information per say) are appended or updated.

    Comments are provided by the standard OpihiExarata form.

    Parameters
    ----------
    header : Astropy Header
        The header which the entries will be added to.
    entries : dictionary
        The new entries to the header.

    Returns
    -------
    opihiexarata_header : Astropy Header
        The header which OpihiExarata entries have been be added to.
    """
    # Working on a copy of the header just in case.
    opihiexarata_header = copy.deepcopy(header)
    # Type checking.
    entries = entries if isinstance(entries, dict) else dict(entries)

    # We assume the defaults at first and see if the provided header or the 
    # provided entries have overridden us. This ensures that the defaults 
    # are always there.
    for keydex in _OPIHIEXARATA_HEADER_KEYWORDS_DICTIONARY.keys():
        # Extracting the default values and the comment.
        defaultdex, commentdex = _OPIHIEXARATA_HEADER_KEYWORDS_DICTIONARY[keydex]
        # We attempt to get a value, either from the supplied header or the 
        # entries provided, to override our default.
        if entries.get(keydex, None) is not None:
            # We first check for a new value provided.
            valuedex = entries[keydex]
        elif opihiexarata_header.get(keydex, None) is not None:
            # Then if a value already existed in the old header, there is 
            # nothing to change or a default to add.
            continue
        else:
            # Otherwise, we just use the default.
            valuedex = defaultdex

        # We type check as FITS header files are picky about the object types 
        # they get FITS headers really only support some specific basic types.
        if not isinstance(valuedex, (int, float, bool, str)):
            raise error.InputError(
                "The input value {v} has a type of {t}. FITS file headers really"
                " only accept strings or numbers.".format(v=valuedex, t=type(valuedex))
            )
        # Adding this record to the row.
        opihiexarata_header.set(
            keyword=keydex, value=valuedex, comment=commentdex
        )
    # All done.
    return opihiexarata_header


def read_fits_image_file(
    filename: str, extension: hint.Union[int, str] = 0
) -> tuple[hint.Header, hint.array]:
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
    data : array
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


def write_fits_image_file(
    filename: str, header: hint.Header, data: hint.array, overwrite: bool = False
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
            "The header must either be an astropy Header class or something convertible"
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
            "The header must either be an astropy Header class or something convertible"
            " to it."
        )
    if not isinstance(data, (ap_table.Table, ap_fits.FITS_rec)):
        raise error.InputError("The data must be an table-like object.")
    # Create the table data
    binary_table = ap_fits.BinTableHDU(data=data, header=header)
    # Write.
    binary_table.writeto(filename, overwrite=overwrite)
    return None
