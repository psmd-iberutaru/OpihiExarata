"""The general photometric solver."""

import astropy.table as ap_table
import numpy as np

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
    intersection_star_table : Table
        A table of stars with both the astrometric and photometric RA and DEC
        coordinates found by the astrometric solution and the photometric
        engine. The filter magnitudes of these stars are also provided. It is
        gauranteed that the stars within this table are correlated.
    """

    astrometrics = None
    star_table = None
    intersection_star_table = None

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
        solver_engine : PhotometryEngine subclass
            The photometric solver engine class. This is what will act as the
            "behind the scenes" and solve the field, using this middlewhere to
            translate it into something that is easier.
        astrometrics : AstrometricSolution, default = None
            A precomputed astrometric solution which belongs to this image.

        Returns
        -------
        None
        """
        # It is a core assumption that the astrometric solution and this
        # photometric solution is working on the same file.
        if fits_filename != astrometrics._original_filename:
            raise error.InputError(
                "The astrometric solution solved an image file different than the image"
                " this photometric solution is trying to solve. It is assumed that the"
                " input astrometric solution and this photometric solution is solving"
                " the same image."
            )

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
                ra=self.astrometrics.ra,
                dec=self.astrometrics.dec,
                radius=self.astrometrics.radius,
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

        # Derive the intersection star table from the photometric results and the
        # astrometric solution. The data table is also used.
        self.intersection_star_table = self.__calculate_intersection_star_table()

        # All done.
        return None

    def __calculate_intersection_star_table(self) -> hint.Table:
        """This function determines the intersection star table.

        Basically this function matches the entries in the astrometric star
        table with the photometric star table. This function accomplishes that
        by simpily associating the closest entires as the same star. The
        distance function assumes a tangent sky projection.

        Parameters
        ----------
        None

        Returns
        -------
        intersection_table : Table
            The intersection of the astrometric and photometric star tables
            giving the correleated star entries between them.
        """
        # The astrometric and photometric tables to be worked with. This
        # functions should be called after they exist so this is fine. This
        # also makes the code a little more readable.
        astrometric_table = self.astrometrics.star_table
        photometric_table = self.star_table

        # The intersection table. The columns are just both tables joined.
        # The first entries are just hard-coded to be first because they are
        # the basic required columns.
        base_columns = [
            "ra_astro",
            "dec_astro",
            "ra_photo",
            "dec_photo",
            "pixel_x",
            "pixel_y",
            "separation",
            "g_mag",
            "g_err",
            "r_mag",
            "r_err",
            "i_mag",
            "i_err",
            "z_mag",
            "z_err",
        ]
        # This sorting method relies on dictionaries preserving insertion
        # order.
        intersection_colnames = (
            base_columns + astrometric_table.colnames + photometric_table.colnames
        )
        intersection_colnames = list(dict.fromkeys(intersection_colnames))
        # Making the table.
        intersection_table = ap_table.Table(masked=True, names=intersection_colnames)

        # The RA and DEC of the photometric tables. Cache them as variables
        # is a little more time efficient.
        ra_phototable = photometric_table["ra_photo"]
        dec_phototable = photometric_table["dec_photo"]

        # A function for finding the signed difference between two angles. This
        # is needed for angular separation comparison to avoid angle wrapping.
        def _sgn_ang_diff(a, b):
            """Find the signed difference between two angles. Assumes degrees."""
            return 180 - (180 - a + b) % 360

        # The maximum that two entries can be seperated while still being the
        # same target. The configuration file's units is arcseconds, convert to
        # degrees.
        MAX_SEP_AECSEC = library.config.PHOTOMETRY_MAXIMUM_INTERSECTION_SEPARATION
        MAX_SEP_DEG = MAX_SEP_AECSEC / 3600

        # Find the closest star within the photometric table for each
        # astrometric star. It is assumed that the two closest entries are
        # the same star.
        for rowdex in astrometric_table:
            # Reassignment for ease.
            ra_astro_row = rowdex["ra_astro"]
            dec_astro_row = rowdex["dec_astro"]
            # Assuming tangential projection and pythagoras distances for
            # finding closest star. Modulus is needed to ensure that angle
            # differences properly wrap around 0 degrees.
            ra_diff = _sgn_ang_diff(a=ra_astro_row, b=ra_phototable)
            dec_diff = _sgn_ang_diff(a=dec_astro_row, b=dec_phototable)
            # Finding minimum separation.
            separations = np.sqrt(ra_diff ** 2 + dec_diff ** 2)
            minimum_separation_index = np.nanargmin(separations)
            minimum_separation = separations[minimum_separation_index]

            # If the separation exceeds the maximum set, then there simply is
            # no pair.
            if MAX_SEP_DEG < minimum_separation:
                # No luck, no matching entry.
                continue
            else:
                # Entries are good enough to match. The photometric table row
                # at the found index is the matching star, combine the data
                # entries. The separation between the is also helpful to have.
                data = (
                    dict(photometric_table[minimum_separation_index])
                    | dict(rowdex)
                    | {"separation": minimum_separation}
                )
                intersection_table.add_row(data)
        # All done.
        return intersection_table


def _vehicle_panstarrs_mast_web_api(ra: float, dec: float, radius: float) -> hint.Table:
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
    # When pulling the table data, the column names are built to be case
    # insensitive, but Astropy tables are case sensitive.
    current_column_names = list(map(lambda s: s.casefold(), using_columns.values()))
    expected_column_names = list(using_columns.keys())
    masked_star_table.rename_columns(current_column_names, expected_column_names)
    # Renaming for documentation purposes.
    photo_star_table = masked_star_table
    return photo_star_table
