"""The astrometric solution class."""

import time
import astropy.coordinates as ap_coordinates

import opihiexarata.astrometry as astrometry
import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


class AstrometricSolution(hint.ExarataSolution):
    """The primary class describing an astrometric solution, based on an image
    provided.

    This class is the middlewere class between the engines which solve the
    astrometry, and the rest of the OpihiExarata code.

    Attributes
    ----------
    _original_filename : string
        The original filename where the fits file is stored at, or copied to.
    _original_header : Header
        The original header of the fits file that was pulled to solve for this
        astrometric solution.
    _original_data : array-like
        The original data of the fits file that was pulled to solve for this
        astrometric solution.
    skycoord : SkyCoord
        The sky coordinate which describes the current astrometric solution.
    ra : float
        The right ascension of the center of the image, in decimal degrees.
    dec : float
        The declination of the center of the image, in decimal degrees.
    orientation : float
        The angle of orientation that the image is at, in degrees.
    radius : float
        The radius of the image, or more specifically, the approximate radius
        that the image covers in the sky, in degrees.
    pixel_scale : float
        The pixel scale of the image, in arcseconds per pixel.
    wcs : Astropy WCS
        The world coordinate solution unified interface provided by Astropy
        for interface to the world coordinate which allows conversion between
        sky and pixel spaces.
    star_table : Table
        A table detailing the correlation of star locations in both pixel and
        celestial space.

    Methods
    -------
    """

    def __init__(
        self, fits_filename: str, solver_engine: type[hint.AstrometryEngine]
    ) -> None:
        """Solving the astrometry via the image provided. The engine class must
        also be provided.

        Parameters
        ----------
        fits_filename : string
            The path of the fits file that contains the data for the astrometric
            solution.
        solver_engine : AstrometryEngine subclass
            The astrometric solver engine class. This is what will act as the
            "behind the scenes" and solve the field, using this middleware to
            translate it into something that is easier.

        Returns
        -------
        None
        """
        # Check that the solver engine is a valid submission, that is is an
        # expected engine class.
        if isinstance(solver_engine, library.engine.AstrometryEngine):
            raise error.EngineError(
                "The astrometric solver engine provided should be the engine class"
                " itself, not an instance thereof."
            )
        elif issubclass(solver_engine, library.engine.AstrometryEngine):
            # It is fine, the user submitted a valid astrometric engine.
            pass
        else:
            raise error.EngineError(
                "The provided astrometric engine is not a valid engine which can be"
                " used for astrometric solutions."
            )


        # Extract information from the header itself.
        header, data = library.fits.read_fits_image_file(filename=fits_filename)

        # Derive the astrometry depending on the engine provided, calling the
        # vehicle functions to run the engines and provide the data needed.
        if issubclass(solver_engine, astrometry.AstrometryNetWebAPIEngine):
            # Solve using the API.
            solution_results = _vehicle_astrometrynet_web_api(
                fits_filename=fits_filename
            )
        else:
            # There is no vehicle function, the engine is not supported.
            raise error.EngineError(
                "The provided astrometric engine `{eng}` is not supported, there is no"
                " associated vehicle function for it.".format(eng=str(solver_engine))
            )

        # Get the results of the solution. If the engine did not provide all of
        # the needed values, then the engine is deficient.
        try:
            # The original information.
            self._original_filename = fits_filename
            self._original_header = header
            self._original_data = data
            # The base astrometric properties of the image.
            self.ra = solution_results["ra"]
            self.dec = solution_results["dec"]
            self.orientation = solution_results["orientation"]
            self.radius = solution_results["radius"]
            self.pixel_scale = solution_results["pixscale"]
            self.wcs = solution_results["wcs"]
            # The stars within the region.
            self.star_table = solution_results["star_table"]
        except KeyError:
            raise error.EngineError(
                "The engine results provided are insufficient for this astrometric"
                " solver. Either the engine cannot be used because it cannot provide"
                " the needed results, or the vehicle function does not pull the"
                " required results from the engine."
            )
        # Construct the Skycoord object from the data provided.
        self.skycoord = ap_coordinates.SkyCoord(
            self.ra, self.dec, frame="icrs", unit="deg"
        )
        # All done.
        return None


def _vehicle_astrometrynet_web_api(fits_filename: str) -> dict:
    """A vehicle function for astrometric solutions. Solve the fits file
    astrometry using the astrometry.net nova web API.

    Parameters
    ----------
    fits_filename : string
        The path of the fits file that contains the data for the astrometric
        solution.

    Returns
    -------
    solution_results : dict
        A dictionary containing the results of the astrometric solution.
    """
    # The results of the solve.
    solution_results = {}
    # Create an instance of the web API to work with.
    PRIVATE_KEY = library.config.SECRET_ASTROMETRYNET_WEB_API_KEY
    # The connection may fail the first time, so it is advised to repeat it a
    # few times first.
    attempt_count = 0
    MAX_ATTEMPTS = library.config.API_CONNECTION_MAXIMUM_ATTEMPTS
    while True:
        try:
            anet_webapi = astrometry.AstrometryNetWebAPIEngine(apikey=PRIVATE_KEY)
        except error.WebRequestError:
            # The connection failed, try again in a little while.
            if attempt_count >= MAX_ATTEMPTS:
                raise error.WebRequestError(
                    "Cannot connect to the astrometry.net web API service. Connection"
                    " attempts exceeded the maximum value specified in the"
                    " configuration file."
                )
            else:
                library.http.api_request_sleep()
                continue
        else:
            # The connection succeeded, there is no need to be in this loop.
            break
        finally:
            attempt_count += 1

    # Before the image is uploaded to astrometry.net, it should be scaled
    # appropriately. To also guard against oddities with fits files, png are
    # send instead if configured to do so.
    if library.config.ASTROMETRYNET_SEND_PNG_IMAGE_FILES:
        # Convert and send the png file instead. The png is made in a temporary
        # directory.
        __, image_data = library.fits.read_fits_image_file(filename=fits_filename)
        # Rescaling the array as it helps with finding the stars. The maximum
        # and minimum values are determined by the png specification.
        LOW_CUT = library.config.ASTROMETRYNET_SEND_PNG_LOWER_PERCENT_CUT
        HIGH_CUT = library.config.ASTROMETRYNET_SEND_PNG_UPPER_PERCENT_CUT
        scaled_image_data = library.image.scale_image_array(
            array=image_data,
            minimum=0,
            maximum=254,
            lower_percent_cut=LOW_CUT,
            upper_percent_cut=HIGH_CUT,
        )
        # Save the image as a png as a temporary file.
        png_path = library.temporary.make_temporary_directory_path(
            filename=library.path.merge_pathname(
                filename=library.path.get_filename_without_extension(
                    pathname=fits_filename
                ),
                extension="png",
            )
        )
        library.image.save_array_as_png_grayscale(
            array=scaled_image_data, filename=png_path, overwrite=False
        )
        file_upload_path = png_path
    else:
        # Send the fits file raw from the detector.
        file_upload_path = fits_filename

    # Upload the file to the API service.
    anet_webapi.upload_file(pathname=file_upload_path)

    # The session and job must be completed before any other post processing
    # can happen.
    if anet_webapi.submission_id is None:
        raise error.WebRequestError(
            "The uploaded file does not have a submission corresponding to it. The job"
            " or results of the solution cannot be obtained without it."
        )
    # It may take a little for the job to finish as there is a job queue for
    # astrometry.net.
    start_time = time.time()
    TIMEOUT_TIME = library.config.ASTROMETRYNET_WEBAPI_JOB_QUEUE_TIMEOUT
    while True:
        try:
            job_id = anet_webapi.job_id
            job_status = anet_webapi.get_job_status()
            if (job_id is None) or (job_status is None):
                raise error.IntentionalError
            elif job_status == "success":
                # The job completed.
                break
            elif job_status == "solving":
                # It is in the process of solving, give it more time.
                continue
            elif job_status == "failure":
                # The job failed.
                raise error.EngineError(
                    "The astrometry web API solving engine failed to solve this field."
                )
            else:
                raise error.UndiscoveredError(
                    "There is a response case that is not checked? Astrometry.net job"
                    " id `{id}` and status `{stat}`".format(id=job_id, stat=job_status)
                )
        except error.IntentionalError:
            # The job likely has not started yet so the data request did
            # not do anything. But, check if the time waited exceeded the
            # timeout.
            current_time = time.time()
            if (current_time - start_time) >= TIMEOUT_TIME:
                raise error.WebRequestError(
                    "The job request did not return any results. It is likely the job"
                    " queue time exceeds the timeout time provided in the"
                    " configuration."
                )
            else:
                library.http.api_request_sleep()
                continue
        else:
            # The logic should not get here.
            raise error.LogicFlowError

    # Preparing data for extraction.
    job_results = anet_webapi.get_job_results()

    wcs = anet_webapi.get_wcs()
    star_corr_table = anet_webapi.get_reference_star_pixel_correlation()
    column_key = ("field_x", "field_y", "field_ra", "field_dec")
    pref_name = ("pixel_x", "pixel_y", "ra_astro", "dec_astro")
    star_corr_subset = star_corr_table[column_key]
    star_corr_subset.rename_columns(column_key, pref_name)

    # Extracting the data
    solution_results["ra"] = job_results["calibration"]["ra"]
    solution_results["dec"] = job_results["calibration"]["dec"]
    solution_results["orientation"] = job_results["calibration"]["orientation"]
    solution_results["radius"] = job_results["calibration"]["radius"]
    solution_results["pixscale"] = job_results["calibration"]["pixscale"]
    solution_results["wcs"] = wcs
    solution_results["star_table"] = star_corr_subset

    return solution_results
