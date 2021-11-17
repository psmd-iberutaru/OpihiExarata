"""The general photometric solver."""

import opihiexarata.astrometry as astrometry
import opihiexarata.photometry as photometry
import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


class PhotometricSolution:
    """The primary class describing an photometric solution, based on an image
    provided and catalog data provided from the photometric engine.

    This class is the middlewere class between the engines which solve the
    photometry, and the rest of the OpihiExarata code.

    Attributes
    ----------
    _original_filename : string
        The original filename where the fits file is stored at, or copied to.
    _original_header : Header
        The original header of the fits file that was pulled to solve for this
        astrometric solution.
    _original_data : array-like
        The original data of the fits file that was pulled to solve for this
        photometric solution.
    astrometrics : AstrometricSolution
        The astrometric solution that is required for the photometric solution.
    star_table : Table
        A table of stars around the image with their RA, DEC, and filter
        magnitudes. It is not guaranteed that this star table and the
        astrometric star table is correlated.
    union_star_table : Table
        A table of stars with both the astrometric and photometric RA and DEC
        coordinates found by the astrometric solution and the photometric
        engine. The filter magnitudes of these stars are also provided. It is
        gauranteed that the stars within this table are correlated.
    """

    astrometrics = None
    star_table = None
    union_star_table = None

    def __init__(
        self,
        fits_filename: str,
        solver_engine: hint.PhotometryEngine,
        astrometrics: hint.AstrometricSolution,
    ) -> None:
        """Initialization of the photometric solution.

        Parameters
        ----------
        fits_filename : string
            The path of the fits file that contains the data for the astrometric
            solution.
        solver_engine : AstrometryEngine subclass
            The photometric solver engine class. This is what will act as the
            "behind the scenes" and solve the field, using this middlewhere to
            translate it into something that is easier.
        astrometrics : AstrometricSolution, default = None
            A precomputed astrometric solution which belongs to this image.

        Returns
        -------
        None
        """
        # Check that the solver engine is a valid submission, that is is an
        # expected engine class.
        if isinstance(solver_engine, library.engine.PhotometryEngine):
            raise error.EngineError(
                "The photometric solver engine provided should be the engine class"
                " itself, not an instance thereof."
            )
        elif issubclass(solver_engine, library.engine.PhotometryEngine):
            # It is fine, the user submitted a valid photometric engine.
            pass
        else:
            raise error.EngineError(
                "The provided photometric engine is not a valid engine which can be"
                " used for photometric solutions."
            )
        # Check that the astrometric solution is a valid solution.
        if not isinstance(astrometrics, astrometry.AstrometricSolution):
            raise error.InputError(
                "A precomputed astrometric solution is required for the computation of"
                " the photometric solution. It must be an AstrometricSolution class"
                " from OpihiExarata."
            )
        else:
            self.astrometrics = astrometrics

        # Extract information from the header itself.
        header, data = library.fits.read_fits_image_file(filename=fits_filename)

        # Derive the photometric star table.
        if issubclass(solver_engine, photometry.PanstarrsMastWebAPI):
            # Solve using the API.
            photo_star_table = _vehicle_panstarrs_mast_web_api(
                fits_filename=fits_filename
            )
        else:
            # There is no vehicle function, the engine is not supported.
            raise error.EngineError(
                "The provided astrometric engine `{eng}` is not supported, there is no"
                " associated vehicle function for it.".format(eng=str(solver_engine))
            )
        # Double check that the photometric star table has the proper columns
        # and conforms to the expectations of the photometric vehicle functions.
        # The order of the columns do not matter, if it has extra columns as
        # well, it does not matter.
        expected_colnames = (
            "ra_photo",
            "dec_photo",
            "g_mag",
            "g_err",
            "r_mag",
            "r_err",
            "i_mag",
            "i_err",
            "z_mag",
            "z_err",
        )
        for colnamedex in expected_colnames:
            if colnamedex not in photo_star_table.colnames:
                raise error.EngineError(
                    "The photometric engine does not generate a star table which has"
                    " the correct expected magnitude columns. The engine or the vehicle"
                    " may not be sufficient. The star table's columns may also have"
                    " incorrect names."
                )
        self.star_table = photo_star_table

        # Derive the union star table from the photometric results and the
        # astrometric solution. The data table is also used.
        self.union_star_table = self.__calculate_union_star_table()

        # All done.
        return None


def _vehicle_panstarrs_mast_web_api(
    self, ra: float, dec: float, radius: float
) -> hint.Table:
    """A vehicle function for photometric solutions. Extract photometric
    data using the PanSTARRS database accessed via the MAST API.

    Parameters
    ----------
    ra : float
        The right accension of the center of the area to extract from,
        in degrees.
    dec : float
        The declination of the center of the area to extract from,
        in degrees.
    radius : float
        The search radius from the center that defines the search area.

    Retruns
    -------
    photo_star_table : Table
        The photometric star table as found from the query.
    """
    # Instance of the PanSTARRS web api client, there does not need to be
    # an API key so far. Sometimes SSL issues arise though.
    SSL_VERIFY = library.config.API_CONNECTION_ENABLE_SSL_CHECKS
    panstarrs_client = photometry.PanstarrsMastWebAPI(verify_ssl=SSL_VERIFY)

    # The columns of relevance to this photometric solver, and their
    # associations with the expected photometric star table that is
    # expected output.
    using_columns = {
        "ra_photo": "raMean",
        "dec_photo": "decMean",
        "g_mag": "gMeanPSFMag",
        "g_err": "gMeanPSFMagErr",
        "r_mag": "rMeanPSFMag",
        "r_err": "rMeanPSFMagErr",
        "i_mag": "iMeanPSFMag",
        "i_err": "iMeanPSFMagErr",
        "z_mag": "zMeanPSFMag",
        "z_err": "zMeanPSFMagErr",
    }

    # Obtain the stars within the region in question. The masked version
    # of this call allows for better handling of invalid entries in
    # PanSTARRS data. Also, we only want targets with photometric results.
    MINIMUM_DETECT = library.config.PHOTOMETRY_MINIMUM_FILTER_OBSERVATIONS
    DR_VER = library.config.PANSTARRS_MAST_API_DATA_RELEASE_VERSION
    MAX_ROW = library.config.PANSTARRS_MAST_API_MAXIMUM_DATA_ROWS
    masked_star_table = panstarrs_client.masked_cone_search(
        ra=ra,
        dec=dec,
        radius=radius,
        detections=MINIMUM_DETECT,
        color_detections=MINIMUM_DETECT,
        columns=list(using_columns.values()),
        max_rows=MAX_ROW,
        data_release=DR_VER,
    )

    # To ensure that the format of the table is as expected for the output
    # of this vehicle function, the columns must be renamed to their
    # prescribed names.
    current_column_names = list(using_columns.values())
    expected_column_names = list(using_columns.keys())
    masked_star_table.rename_columns(current_column_names, expected_column_names)
    # Renaming for documentation purposes.
    photo_star_table = masked_star_table
    return photo_star_table
