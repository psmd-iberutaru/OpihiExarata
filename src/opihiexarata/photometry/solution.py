"""The general photometric solver."""

import astropy.coordinates as ap_coord
import astropy.table as ap_table
import numpy as np

import opihiexarata.astrometry as astrometry
import opihiexarata.photometry as photometry
import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


class PhotometricSolution(hint.ExarataSolution):
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
    sky_counts : float
        The average sky contribution per pixel.
    star_table : Table
        A table of stars around the image with their RA, DEC, and filter
        magnitudes. It is not guaranteed that this star table and the
        astrometric star table is correlated.
    intersection_star_table : Table
        A table of stars with both the astrometric and photometric RA and DEC
        coordinates found by the astrometric solution and the photometric
        engine. The filter magnitudes of these stars are also provided. It is
        gauranteed that the stars within this table are correlated.
    exposure_time : float
        How long, in seconds, the image in question was exposed for.
    filter_name : string
        A single character string describing the name of the filter band that
        this image was taken in. Currently, it assumes the MKO/SDSS visual
        filters.
    zero_point : float
        The zero point of the image.
    zero_point_error : float
        The standard deviation of the error point mean as calculated using
        many stars.
    """

    def __init__(
        self,
        fits_filename: str,
        solver_engine: hint.PhotometryEngine,
        astrometrics: hint.AstrometricSolution,
        exposure_time: float = None,
        filter_name: str = None,
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
        exposure_time : float, default = None
            How long, in seconds, the image in question was exposed for. If
            not provided, calculation of the zero-point is skipped.
        filter_name : string, default = None
            A single character string describing the name of the filter band that
            this image was taken in. Currently, it assumes the MKO/SDSS visual
            filters. If it is None, calculation of the zero-point is skipped.

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
        self._original_filename = fits_filename
        self._original_header = header
        self._original_data = data

        # Derive the photometric star table.
        if issubclass(solver_engine, photometry.PanstarrsMastWebAPIEngine):
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

        # Determine the average sky contribution per pixel.
        self.sky_counts_mask = self.__calculate_sky_counts_mask()
        self.sky_counts = self.__calculate_sky_counts_value()

        # Calculating the zero point of this filter image as it is part of the
        # photometric solution.
        if exposure_time is None or filter_name is None:
            # Both is needed to compute the zero point, skip it.
            self.exposure_time = None
            self.zero_point = None
            self.zero_point_error = None
            self.filter_name = None
        else:
            zero, zero_err = self._calculate_zero_point(
                exposure_time=exposure_time, filter_name=filter_name
            )
            self.exposure_time = exposure_time
            self.zero_point = zero
            self.zero_point_error = zero_err
            self.filter_name = filter_name

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
            "counts",
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

        # The size of a star, used for the photometric count determination. As
        # the star photon counts function uses degrees, a conversion is done.
        STAR_RADIUS_DEG = library.config.PHOTOMETRY_STAR_RADIUS_ARCSECOND * (1 / 3600)

        # Find the closest star within the photometric table for each
        # astrometric star. It is assumed that the two closest entries are
        # the same star.
        for rowdex in astrometric_table:
            # Reassignment for ease.
            ra_astro_row = rowdex["ra_astro"]
            dec_astro_row = rowdex["dec_astro"]
            # Assuming tangential projection and pythagoras distances for
            # finding closest star. Special function used to handle angle
            # wrapping.
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
                # Entries are good enough to match.

                # The difference between the two locations in space may be
                # useful.
                separation = minimum_separation
                # The total counts of this star. This table is going to be
                # used for photometric calculations so having this in the table
                # is a useful convince.
                dn_counts = self._calculate_star_photon_counts_coordinate(
                    ra=ra_astro_row, dec=dec_astro_row, radius=STAR_RADIUS_DEG
                )

                # The photometric table row at the found index is the matching
                # star, combine the data entries.
                data = (
                    dict(photometric_table[minimum_separation_index])
                    | dict(rowdex)
                    | {"separation": separation}
                    | {"counts": dn_counts}
                )
                intersection_table.add_row(data)
        # All done.
        return intersection_table

    def __calculate_sky_counts_mask(self) -> hint.ArrayLike:
        """Calculate a mask which blocks out all but the sky for sky counts
        determination.

        The method used is to exclude the regions where stars exist (as
        determined by the star tables) and also the central region
        of the image (as it is expected that there is a science object there).

        Parameters
        ----------
        None

        Returns
        -------
        sky_counts_mask : float
            The mask which masks out which is not intresting regarding sky
            count calculations.
        """
        # Extracting the needed information from the computed solution values.
        data_array = np.array(self.astrometrics._original_data, dtype=float, copy=True)
        wcs = self.astrometrics.wcs
        arcsec_pixel_scale = self.astrometrics.pixel_scale
        photo_star_table = self.star_table
        astro_star_table = self.astrometrics.star_table
        # Information about the data array.
        n_rows, n_cols = data_array.shape

        # Using the photometric star table as the locations for the stars is
        # likely more accurate and also would theoretically exclude more stars
        # than the astrometric star table. But, there is no harm in using both.
        # The pixel values for the photometric table are derived from the WCS.
        photo_ra, photo_dec = (
            photo_star_table["ra_photo"],
            photo_star_table["dec_photo"],
        )
        photo_x, photo_y = wcs.world_to_pixel_values(photo_ra, photo_dec)
        photo_x = np.array(photo_x, dtype=int)
        photo_y = np.array(photo_y, dtype=int)
        astro_x = np.array(astro_star_table["pixel_x"], dtype=int)
        astro_y = np.array(astro_star_table["pixel_y"], dtype=int)
        # The pixel locations of all detected stars.
        stars_x = np.append(photo_x, astro_x)
        stars_y = np.append(photo_y, astro_y)
        # The length of the masking box region for a star, being generous on
        # the half definition for odd sized boxes.
        STAR_RADIUS_AS = library.config.PHOTOMETRY_STAR_RADIUS_ARCSECOND
        STAR_RADIUS_PIXEL = STAR_RADIUS_AS / arcsec_pixel_scale
        HALF_BOX_LENGTH = int(2 * STAR_RADIUS_PIXEL) + 2
        # Definiting the star mask to mask regions where stars have been
        # detected.
        star_mask = np.zeros_like(data_array, dtype=bool)
        for colindex, rowindex in zip(stars_x, stars_y):
            star_mask[
                rowindex - HALF_BOX_LENGTH : rowindex + HALF_BOX_LENGTH,
                colindex - HALF_BOX_LENGTH : colindex + HALF_BOX_LENGTH,
            ] = True
        # Masking the center region as well as a science object is expected
        # to be there.
        SCIENCE_RADIUS = library.config.PHOTOMETRY_SCIENCE_RADIUS_MASK_PIXELS
        SCI_WIDTH = int(2 * SCIENCE_RADIUS + 1)
        science_mask = np.zeros_like(data_array, dtype=bool)
        science_mask[
            n_rows // 2 - SCI_WIDTH : n_rows // 2 + SCI_WIDTH,
            n_cols // 2 - SCI_WIDTH : n_cols // 2 + SCI_WIDTH,
        ] = True
        # Mask the edges of the array as often they are spurious and may have
        # bleed over from electronics onto the detector itself. This also is a
        # way of ignoring that the slices above may not be proper, hence the
        # edge value.
        EDGE_WIDTH = library.config.PHOTOMETRY_EDGE_WIDTH_MASK_PIXELS
        edge_mask = np.ones_like(data_array, dtype=bool)
        edge_mask[EDGE_WIDTH:-EDGE_WIDTH, EDGE_WIDTH:-EDGE_WIDTH] = False
        # Finally, making any values which do not really make any sense or are
        # already nans.
        nan_mask = ~(np.isfinite(data_array))

        # Adding all of the masks.
        sky_counts_mask = star_mask | science_mask | edge_mask | nan_mask
        return sky_counts_mask

    def __calculate_sky_counts_value(self) -> float:
        """Calculate the background sky value, in counts, from the image.
        Obviously needed for photometric calibrations.

        The regions outside of the sky mask represent the sky and the sky
        counts is extracted from that.

        Parameters
        ----------
        None

        Returns
        -------
        sky_counts : float
            The total number of counts, in DN that, on average, the sky
            contributes per pixel.
        """
        # Extracting the needed information from the computed solution values.
        data_array = np.array(self.astrometrics._original_data, dtype=float, copy=True)
        # If the sky mask has not been computed, then it should be determined.
        try:
            sky_counts_mask = self.sky_counts_mask
        except AttributeError:
            # Calculate the mask first, it is strange that this is called first.
            sky_counts_mask = self.__calculate_sky_counts_mask()

        # Apply the sky mask.
        masked_data_array = np.ma.array(data_array, mask=sky_counts_mask)
        sky_data_values = masked_data_array.compressed()

        # Computing the sky value based on the star-masked array.
        sky_counts = np.ma.median(sky_data_values)
        return sky_counts

    def _calculate_star_photon_counts_coordinate(
        self, ra: float, dec: float, radius: float
    ) -> float:
        """Calculate the total number of photometric counts at an RA DEC. The
        counts are already corrected for the sky counts.

        This function does not check if a star is actually there. This function
        is a wrapper around its pixel version, converting via the WCS solution.

        Parameters
        ----------
        ra : float
            The right ascension in degrees.
        dec : float
            The declination in degrees.
        radius : float
            The radius of the circular aperture to be considered, in degrees.

        Returns
        -------
        photon_counts : float
            The sum of the sky corrected counts for the region defined.
        """
        # Extracting the needed parameters.
        wcs = self.astrometrics.wcs
        arcsec_pixel_scale = self.astrometrics.pixel_scale

        # Translating the coordinates to the usable pixels.
        photo_x, photo_y = wcs.world_to_pixel_values(ra, dec)

        # The radius is in angular degrees, converting it to pixels via the
        # scale. Converting the astrometrics scale to degrees as well as the
        # input unit is that.
        pixel_radius = radius / (arcsec_pixel_scale * (1 / 3600))

        # Using the pixel version because there is little need to implement
        # it all again.
        photon_counts = self._calculate_star_photon_counts_pixel(
            pixel_x=photo_x, pixel_y=photo_y, radius=pixel_radius
        )
        return photon_counts

    def _calculate_star_photon_counts_pixel(
        self, pixel_x: int, pixel_y: int, radius: float
    ) -> float:
        """Calculate the total number of photometric counts at a pixel
        location. The counts are already corrected for the sky counts.

        This function does not check if a star is actually there.

        Parameters
        ----------
        pixel_x : int
            The x cordinate of the center pixel.
        pixel_y : int
            The y cordinate of the center pixel.
        radius : float
            The radius of the circular aperture to be considered in pixel
            counts.

        Returns
        -------
        photon_counts : float
            The sum of the sky corrected counts for the region defined.
        """
        # Extracting the needed parameters.
        data_array = np.array(self.astrometrics._original_data, dtype=float, copy=True)
        sky_counts = self.sky_counts

        # Taking out the sky contribution.
        data_array_nosky = data_array - sky_counts

        # A circular mask is used to define the star.
        star_mask = library.image.create_circular_mask(
            array=data_array_nosky, center_x=pixel_x, center_y=pixel_y, radius=radius
        )
        star_array_nosky = np.ma.array(data_array_nosky, mask=star_mask)

        # Summing up the total counts within the star region as defined by the
        # star mask, this is the total photon counts.
        photon_counts = np.nansum(star_array_nosky)
        return photon_counts

    def _calculate_zero_point(
        self, exposure_time: float, filter_name: str = None
    ) -> float:
        """This function calculates the photometric zero-point of the image
        provided the data in the intersection star table.

        This function uses the set exposure time and the intersection star
        table. The band is also assumed from the initial parameters.

        Parameters
        ----------
        exposure_time : float
            How long, in seconds, the image in question was exposed for.
        filter_name : string, default = None
            A single character string describing the name of the filter band that
            this image was taken in. Currently, it assumes the MKO/SDSS visual
            filters. If it is None, then this function does nothing.

        Returns
        -------
        zero_point : float
            The zero point of this image. This is computed as a mean of all of
            the calculated zero points.
        zero_point_error : float
            The standard deviation of the zero points calculated.
        """
        # Obtaining the needed information.
        inter_star_table = self.intersection_star_table

        # The exposure time information.
        self.exposure_time = float(exposure_time)

        # The filter name, check that it is a valid expected filter which the
        # photometric engines and vehicle functions are expected to deal with.
        ACCEPTED_FILTERS = ("g", "r", "i", "z")
        if filter_name is None:
            # The filter is not provided and thus photometry cannot be
            # performed.
            zero_point = self.zero_point
            zero_point_error = self.zero_point_error
            return zero_point, zero_point_error
        elif filter_name not in ACCEPTED_FILTERS:
            raise error.InputError(
                "The filter name provided `{f}` is not a filter that is supposed by"
                " OpihiExarata's supported photometric engines and vehicle functions"
                " and therefore cannot be used to derive a photometric solution."
                " Accepted filters: {af}".format(f=filter_name, af=ACCEPTED_FILTERS)
            )
        else:
            self.filter_name = str(filter_name)

        # Extract the proper photometric values for the filter being used.
        filter_table_header = "{f}_mag".format(f=filter_name)
        magnitude = inter_star_table[filter_table_header]
        # And the count data.
        counts = inter_star_table["counts"]

        # Instrument magnitudes.
        inst_magnitude = -2.5 * np.log10(counts / exposure_time)

        # Zero points via the definition equation
        zero_points = magnitude - inst_magnitude
        zero_point = np.mean(zero_points)
        zero_point_error = np.std(zero_points)
        return zero_point, zero_point_error


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
    panstarrs_client = photometry.PanstarrsMastWebAPIEngine(verify_ssl=SSL_VERIFY)

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
