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
    "OX_BEGIN": (True, "OX: True if OpihiExarata (OX) processed."),
    # Target/asteroid information; T.
    "OXT_NAME": (None, "OX: Target/asteroid name."),
    "OXT_PX_X": (None, "OX: Target pixel x location."),
    "OXT_PX_Y": (None, "OX: Target pixel y location."),
    "OXT___RA": (None, "OX: Target RA coordinate."),
    "OXT__DEC": (None, "OX: Target DEC coordinate."),
    "OXT__MAG": (None, "OX: Aperture magnitude."),
    "OXT_MAGE": (None, "OX: Aperture magnitude error."),
    # Metadata; M.
    "OXM_ORFN": (None, "OX: Original FITS filename."),
    "OXM_REDU": (False, "OX: True if image preprocessed."),
    # Astrometry; A.
    "OXA_SLVD": (False, "OX: True if astrometry solved."),
    "OXA__ENG": (None, "OX: Astrometry engine."),
    "OXA___RA": (None, "OX: Center RA coordinate."),
    "OXA__DEC": (None, "OX: Center DEC coordinate."),
    "OXA_ANGL": (None, "OX: Image orientation, degree."),
    "OXA_RADI": (None, "OX: Image radius, degree."),
    "OXA_PXSC": (None, "OX: Pixel scale, arcsec/pix."),
    # Photometry; P.
    "OXP_SLVD": (False, "OX: True if photometry solved."),
    "OXP__ENG": (None, "OX: Photometry engine."),
    "OXP_FILT": (None, "OX: Filter name."),
    "OXPSKYCT": (None, "OX: Average sky counts."),
    "OXP_ZP_M": (None, "OX: Zero point magnitude."),
    "OXP_ZP_E": (None, "OX: Zero point error."),
    "OXP_APTR": (None, "OX: Aperture radius, arcsec."),
    # Orbital elements; O.
    "OXO_SLVD": (False, "OX: True if orbit solved."),
    "OXO__ENG": (None, "OX: The orbit engine."),
    "OXO_A__S": (None, "OX: Semi-major axis, AU."),
    "OXO_E__S": (None, "OX: Eccentricity, 1."),
    "OXO_IN_S": (None, "OX: Inclination, degree."),
    "OXO_OM_S": (None, "OX: Ascending node, degree."),
    "OXO__W_S": (None, "OX: Perihelion, degree."),
    "OXO_MA_S": (None, "OX: Mean anomaly, degree."),
    "OXO_EA_D": (None, "OX: Eccentric anomaly, degree."),
    "OXO_TA_D": (None, "OX: True anomaly, degree."),
    "OXO_A__E": (None, "OX: Semi-major axis error, AU."),
    "OXO_E__E": (None, "OX: Eccentricity error, 1."),
    "OXO_IN_E": (None, "OX: Inclination angle error, degree."),
    "OXO_OM_E": (None, "OX: Ascending node error, degree."),
    "OXO__W_E": (None, "OX: Perihelion error, degree."),
    "OXO_MA_E": (None, "OX: Mean anomaly error, degree."),
    "OXO_EA_E": (None, "OX: Eccentric anomaly error, degree."),
    "OXO_TA_E": (None, "OX: True anomaly error, degree."),
    "OXO_EPCH": (None, "OX: Epoch, Julian days."),
    # Ephemeris; E.
    "OXE_SLVD": (False, "OX: True if ephemeris solved."),
    "OXE__ENG": (None, "OX: Ephemeritic engine."),
    "OXE_RA_V": (None, "OX: Ephem. RA vel., arcsec/s."),
    "OXE_DECV": (None, "OX: Ephem. DEC vel., arcsec/s."),
    "OXE_RA_A": (None, "OX: Ephem. RA acc., arcsec/s^2."),
    "OXE_DECA": (None, "OX: Ephem. DEC acc., arcsec/s^2."),
    # Propagation; R.
    "OXR_SLVD": (False, "OX: True if propagate solved."),
    "OXR__ENG": (None, "OX: The propagation engine."),
    "OXR_RA_V": (None, "OX: Prop. RA vel., arcsec/s."),
    "OXR_DECV": (None, "OX: Prop. DEC vel., arcsec/s."),
    "OXR_RA_A": (None, "OX: Prop. RA acc., arcsec/s^2."),
    "OXR_DECA": (None, "OX: Prop. DEC acc., arcsec/s^2."),
    # End.
    "OX___END": (False, "OX: True if no error on save."),
}


def get_observing_time(filename: str) -> float:
    """This reads the header of a FITS file and extracts from it the
    time of observation from the FITS file and returns it. This assumes
    the header key of the observing time to be pulled is: `MJD_OBS`.

    Parameters
    ----------
    filename : string
        The FITS filename to pull the observing time from.

    Returns
    -------
    observing_time_jd : float
        The time of the observation, in Julian days.
    """
    # We pull the header.
    header = read_fits_header(filename=filename)
    # Extracting the observing time, it is in modified Julian days.
    observing_time_mjd = header["MJD_OBS"]
    # We convert to Julian days as that is the convention of this software.
    observing_time_jd = library.conversion.modified_julian_day_to_julian_day(
        mjd=observing_time_mjd
    )
    return observing_time_jd


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
        if isinstance(valuedex, (int, float, bool, str)):
            # These are generally accepted types.
            pass
        elif valuedex is None:
            # Astropy may be able to handle it.
            pass
        else:
            raise error.InputError(
                "The input value {v} has a type of {t}. FITS file headers really"
                " only accept strings or numbers.".format(v=valuedex, t=type(valuedex))
            )
        # Adding this record to the row.
        opihiexarata_header.set(keyword=keydex, value=valuedex, comment=commentdex)
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
