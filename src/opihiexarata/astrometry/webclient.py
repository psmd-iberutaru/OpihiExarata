import os
import urllib.parse
import urllib.request
import urllib.error
import random
import astropy.wcs as ap_wcs

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

# The base URL for the API which all other service URLs are derived from.
_DEFAULT_BASE_ASTROMETRY_NET_NOVA_WEB_URL = "http://nova.astrometry.net/api/"


class AstrometryNetWebAPIEngine(library.engine.AstrometryEngine):
    """A python-based wrapper around the web API for astrometry.net.

    This API does not have the full functionality of the default Python client
    seen at https://github.com/dstndstn/astrometry.net/blob/master/net/client/client.py.
    The point of this class is to be simple enough to be understood by others and
    be specialized for OpihiExarata.

    Attributes
    ----------
    _ASTROMETRY_NET_API_BASE_URL : string
        The base URL for the API which all other service URLs are derived from.
    _apikey : string
        The API key used to log in.
    original_upload_filename : string
        The original filename that was used to upload the data.
    session : string
        The session ID of this API connection to astrometry.net
    """

    def __init__(self, url=None, apikey: str = None, silent: bool = True) -> None:
        """The instantiation, connecting to the web API using the API key.

        Parameters
        ----------
        url : string, default = None
            The base url which all other API URL links are derived from. This
            should be used if the API is a self-hosted install or has a
            different web source than nova.astrometry.net. Defaults to the
            nova.astrometry.net api service.
        apikey : string
            The API key of the user.
        silent : bool, default = True
            Should there be printed messages as the processes are executed.
            This is helpful for debugging or similar processes.

        Returns
        -------
        None
        """
        # Defining the URL.
        self._ASTROMETRY_NET_API_BASE_URL = (
            str(url) if url is not None else _DEFAULT_BASE_ASTROMETRY_NET_NOVA_WEB_URL
        )

        # Base parameters.
        # The default arguments for uploading files. In (key, value, type) form.
        # Detailed is also their useage cases per
        # http://astrometry.net/doc/net/api.html#submitting-a-url
        self._DEFAULT_URL_ARGUMENTS = [
            # These parameters are for licensing and distribution terms.
            ("allow_commercial_use", "d", str),
            ("allow_modifications", "d", str),
            # For visibility by the general public.
            ("publicly_visible", "y", str),
            # Image scaling parameters, if provided, when known, helps the
            # processing a little.
            ("scale_units", None, str),
            ("scale_type", None, str),
            ("scale_lower", None, float),
            ("scale_upper", None, float),
            ("scale_est", None, float),
            ("scale_err", None, float),
            # These parameters allows for the establishment of an initial guess
            # specified byt he centers, and its maximal deviation as specified
            # by the radius parameter. (In degrees.)
            ("center_ra", None, float),
            ("center_dec", None, float),
            ("radius", None, float),
            # Image properties, preprocessing it a little can help in its
            # determination.
            ("parity", None, int),
            ("downsample_factor", None, int),
            ("positional_error", None, float),
            ("tweak_order", None, int),
            ("crpix_center", None, bool),
            ("invert", None, bool),
            # These parameters are needed if being sent instead is an x,y list of
            # source star positions.
            ("image_width", None, int),
            ("image_height", None, int),
            ("x", None, list),
            ("y", None, list),
            ("album", None, str),
        ]

        # Use the API key to log in a derive a session key.
        self.session = None
        session_key = self.__login(apikey=apikey)
        self._apikey = apikey
        self.session = session_key

        # Placeholder variables.
        self.original_upload_filename = str()
        self._image_return_results = {}
        return None

    def __login(self, apikey: str) -> str:
        """The method to log into the API system.

        Parameters
        ----------
        apikey : string
            The API key for the web API service.

        Returns
        -------
        session_key : string
            The session key for this login session.
        """
        # The key.
        args = {"apikey": apikey}
        result = self._send_web_request(service="login", args=args)
        session = result.get("session", False)
        # Check if the session works and that the API key given is valid.
        if not session:
            raise error.WebRequestError(
                "The provided API key did not provide a valid session."
            )
        else:
            # The session should be fine.
            session_key = session
        return session_key

    def __get_submission_id(self) -> str:
        """Extract the submission ID from the image upload results."""
        image_results = self._image_return_results
        self.__submission_id = image_results.get("subid", None)
        return self.__submission_id

    def __set_submission_id(self, sub_id) -> None:
        """Assign the submission ID, it should only be done once when the
        image is obtained."""
        if self.__submission_id is None:
            self.__submission_id = sub_id
        else:
            raise error.ReadOnlyError(
                "The submission ID has already been set by obtaining it from the API"
                " service."
            )
        return None

    def __del_submission_id(self) -> None:
        """Remove the current submission ID association."""
        self.__submission_id = None
        return None

    __doc_submission_id = (
        "When file upload or table upload is sent to the API, the submission ID is"
        " saved here."
    )
    __submission_id = None
    submission_id = property(
        __get_submission_id,
        __set_submission_id,
        __del_submission_id,
        __doc_submission_id,
    )

    def __get_job_id(self) -> str:
        """Extract the job ID from the image upload results. It may be the
        case that there is not job yet associated with this submission.
        """
        # If the job ID already has been obtained, then there is no reason to
        # call the API again.
        if self.__job_id is not None:
            return self.__job_id
        # Call the API to get the job ID.
        try:
            submission_results = self.get_submission_results(
                submission_id=self.submission_id
            )
        except error.WebRequestError:
            # Make a more helpful error message for what is going on.
            if self.submission_id is None:
                raise error.WebRequestError(
                    "There cannot be a job id without there being a submission for that"
                    " job to operate on."
                )
            else:
                # What happened is unknown.
                raise error.UndiscoveredError("Why the web request failed is unknown.")
        else:
            job_id_list = submission_results.get("jobs", [])
            # If there are no jobs, then it is likely still in queue.
            if len(job_id_list) == 0:
                self.__job_id = None
            else:
                self.__job_id = job_id_list[-1]
            return self.__job_id
        raise error.LogicFlowError
        return None

    def __set_job_id(self, job_id) -> None:
        """Assign the job ID, it should only be done once when the
        image is obtained."""
        if self.__job_id is None:
            self.__job_id = job_id
        else:
            raise error.ReadOnlyError(
                "The job ID has already been set by obtaining it from the API service."
            )
        return None

    def __del_job_id(self) -> None:
        """Remove the current job ID association."""
        self.__job_id = None
        return None

    __doc_job_id = (
        "When file upload or table upload is sent to the API, the job ID of the"
        " submission is saved here."
    )
    __job_id = None
    job_id = property(__get_job_id, __set_job_id, __del_job_id, __doc_job_id)

    def _generate_service_url(self, service: str) -> str:
        """Generate the correct URL for the desired service. Because astrometry.net
        uses a convention, we can follow it to obtain the desired service URL.

        Parameters
        ----------
        service : str
            The service which the API URL for should be generated from.

        Returns
        -------
        url : str
            The URL for the service.
        """
        url = self._ASTROMETRY_NET_API_BASE_URL + service
        return url

    def _generate_upload_args(self, **kwargs) -> dict:
        """Generate the arguments for sending a request. This constructs the
        needed arguments, replacing the defaults with user provided arguments
        where desired.

        Parameters
        ----------
        **kwargs : dict
            Arguments which would override the defaults.

        Returns
        -------
        args : dict
            The arguments which can be used to send the request.

        """
        args = {}
        for keydex, defaultdex, typedex in self._DEFAULT_URL_ARGUMENTS:
            if keydex in kwargs:
                new_value = kwargs.pop(keydex)
                new_value = typedex(new_value)
                args.update({keydex: new_value})
            elif defaultdex is not None:
                args.update({keydex: defaultdex})
        return args

    def _send_web_request(
        self, service: str, args: dict = {}, file_args: dict = None
    ) -> dict:
        """A wrapper function for sending a webrequest to the astrometry.net API
        service. Returns the results as well.

        Parameters
        ----------
        service : string
            The service which is being requested. The web URL is constructed
            from this string.
        args : dictionary, default = {}
            The arguments being sent over the web request.
        file_args : dictionary, default = None
            If a file is being uploaded instead, special care must be taken to
            sure it matches the upload specifications.

        Returns
        -------
        results : dictionary
            The results of the web request if it did not fail.
        """
        # Obtain the session key derived when this class is instantiated and
        # logged into. Use this session key for requests.
        if self.session is not None:
            args.update({"session": self.session})
        # The API requires that the data format must be a JSON based datatype.
        json_data = library.json.dictionary_to_json(dictionary=args)
        # The URL which to send this request to, constructed from the service
        # desired.
        api_url = self._generate_service_url(service=service)

        # If the request requires that a file be send, then it must be in the
        # correct format. Namely, a multipart/form-data format.
        if file_args is not None:
            boundary_key = "".join([random.choice("0123456789") for __ in range(19)])
            boundary = "==============={bkey}==".format(bkey=boundary_key)
            headers = {
                "Content-Type": 'multipart/form-data; boundary="{bd}"'.format(
                    bd=boundary
                )
            }
            data_pre = str(
                "--"
                + boundary
                + "\n"
                + "Content-Type: text/plain\r\n"
                + "MIME-Version: 1.0\r\n"
                + 'Content-disposition: form-data; name="request-json"\r\n'
                + "\r\n"
                + json_data
                + "\n"
                + "--"
                + boundary
                + "\n"
                + "Content-Type: application/octet-stream\r\n"
                + "MIME-Version: 1.0\r\n"
                + 'Content-disposition: form-data; name="file"; filename="{name}"'.format(
                    name=file_args["filename"]
                )
                + "\r\n"
                + "\r\n"
            )
            data_post = "\n" + "--" + boundary + "--\n"
            data = data_pre.encode() + file_args["data"] + data_post.encode()

        else:
            # Otherwise, the form should be standard encoded: x-www-form-encoded
            headers = {}
            data = {"request-json": json_data}
            data = urllib.parse.urlencode(data)
            data = data.encode("utf-8")

        # Finally send the request.
        request = urllib.request.Request(url=api_url, headers=headers, data=data)

        # Processing the request.
        try:
            file = urllib.request.urlopen(
                request, timeout=library.config.ASTROMETRYNET_WEBAPI_JOB_QUEUE_TIMEOUT
            )
            text = file.read()
            result = library.json.json_to_dictionary(json_string=text)
            # Check if the status of the request provided is a valid status.
            status = result.get("status")
            if status == "error":
                error_message = result.get("errormessage", "(none)")
                # Try to deduce what the error is.
                if error_message == "bad apikey":
                    raise error.WebRequestError(
                        "The API key provided is not a valid key."
                    )
                else:
                    raise error.WebRequestError(
                        "The server returned an error status message: \n {message}".format(
                            message=error_message
                        )
                    )
            else:
                return result
        except urllib.error.HTTPError:
            raise error.WebRequestError(
                "The web request output cannot be properly processed. This is likely"
                " from a bad web request."
            )
        # The logic should not flow beyond this point.
        raise error.LogicFlowError
        return None

    def get_job_results(self, job_id: str = None) -> dict:
        """Get the results of a job sent to the API service.

        Parameters
        ----------
        job_id : str, default = None
            The ID of the job that the results should be obtained from. If not
            provided, the ID determined by the file upload is used.

        Returns
        -------
        results : dict
            The results of the astrometry.net job. They are, in general: (If
            the job has not finished yet, None is returned.)

                - Status : The status of the job.
                - Calibration : Calibration of the image uploaded.
                - Tags : Known tagged objects in the image, people inputted.
                - Machine Tags : Ditto for tags, but only via machine inputs.
                - Objects in field : Known objects in the image field.
                - Annotations : Known objects in the field, with annotations.
                - Info : A collection of most everything above.
        """
        job_id = job_id if job_id is not None else self.job_id
        # Get the result of the job.
        service_string = "jobs/{id}".format(id=job_id)
        try:
            job_result = self._send_web_request(service=service_string)
        except error.WebRequestError:
            # This error is likely because the job is still in queue.
            return None
        # Check that the service was successful.
        status = job_result.get("status", False)
        if status != "success":
            raise error.WebRequestError(
                "The job result request failed, check that the job ID is correct or try"
                " again later."
            )
        else:
            results = {}
            # For the status.
            results["status"] = status
            # For the calibrations.
            service_string = "jobs/{id}/calibration".format(id=job_id)
            results["calibration"] = self._send_web_request(service=service_string)
            # For the tags.
            service_string = "jobs/{id}/tags".format(id=job_id)
            results["tags"] = self._send_web_request(service=service_string)
            # For the machine tags.
            service_string = "jobs/{id}/machine_tags".format(id=job_id)
            results["machine_tags"] = self._send_web_request(service=service_string)
            # For the objects in field.
            service_string = "jobs/{id}/objects_in_field".format(id=job_id)
            results["objects_in_field"] = self._send_web_request(service=service_string)
            # For the annotations.
            service_string = "jobs/{id}/annotations".format(id=job_id)
            results["annotations"] = self._send_web_request(service=service_string)
            # For the info.
            service_string = "jobs/{id}/info".format(id=job_id)
            results["info"] = self._send_web_request(service=service_string)
        # All done.
        return results

    def get_job_status(self, job_id: str = None) -> str:
        """Get the status of a job specified by its ID.

        Parameters
        ----------
        job_id : str, default = None
            The ID of the job that the results should be obtained from. If not
            provided, the ID determined by the file upload is used.

        Returns
        -------
        status : string
            The status of the submission. If the job has not run yet, None is
            returned instead.
        """
        job_id = job_id if job_id is not None else self.job_id
        # Get the result of the job.
        service_string = "jobs/{id}".format(id=job_id)
        status = None
        try:
            job_result = self._send_web_request(service=service_string)
        except error.WebRequestError:
            # This error is likely because the job is still in queue.
            status = None
        else:
            # Check the job status.
            status = job_result.get("status")
        finally:
            return status
        # Should not get here.
        raise error.LogicFlowError
        return None

    def get_submission_results(self, submission_id: str = None) -> dict:
        """Get the results of a submission specified by its ID.

        Parameters
        ----------
        submission_id : str
            The ID of the submission. If it is not passed, the ID determined
            by the file upload is used.

        Returns
        -------
        result : dict
            The result of the submission.
        """
        submission_id = (
            submission_id if submission_id is not None else self.submission_id
        )
        service_string = "submissions/{sub_id}".format(sub_id=submission_id)
        result = self._send_web_request(service=service_string)
        return result

    def get_submission_status(self, submission_id: str = None) -> str:
        """Get the status of a submission specified by its ID.

        Parameters
        ----------
        submission_id : str, default = None
            The ID of the submission. If it is not passed, the ID determined
            by the file upload is used.

        Returns
        -------
        status : string
            The status of the submission.
        """
        submission_id = (
            submission_id if submission_id is not None else self.submission_id
        )
        results = self.get_submission_results(submission_id=submission_id)
        status = results.get("status")
        return status

    def get_reference_star_pixel_correlation(
        self, job_id: str = None, temp_filename: str = None, delete_after: bool = True
    ) -> hint.Table:
        """This obtains the table that correlates the location of reference
        stars and their pixel locations. It is obtained from the fits corr file
        that is downloaded into a temporary directory.

        Parameters
        ----------
        job_id : string, default = None
            The ID of the job that the results should be obtained from. If not
            provided, the ID determined by the file upload is used.
        temp_filename : string, default = None
            The filename that the downloaded correlation file will be
            downloaded as. The path is going to still be in the temporary
            directory.
        delete_after : bool, default = True
            Delete the file after downloading it to extract its information.

        Returns
        -------
        correlation_table : Table
            The table which details the correlation between the coordinates of
            the stars and their pixel locations.
        """
        job_id = job_id if job_id is not None else self.job_id
        # Download the correlation file to read into a data table.
        upload_filename = library.path.get_filename_without_extension(
            pathname=self.original_upload_filename
        )
        fits_table_filename = (
            temp_filename if temp_filename is not None else upload_filename + "_corr"
        )
        # The full path of the filename derived from saving it in a temporary
        # directory.
        corr_filename = library.path.merge_pathname(
            filename=fits_table_filename, extension="fits"
        )
        corr_pathname = library.temporary.make_temporary_directory_path(
            filename=corr_filename
        )
        # Save the correlation file.
        self.download_result_file(
            filename=corr_pathname, file_type="corr", job_id=job_id
        )
        # Load the data from the file.
        __, correlation_table = library.fits.read_fits_table_file(
            filename=corr_pathname, extension=1
        )
        # Delete the temporary file after loading it if desired.
        if delete_after:
            os.remove(corr_pathname)
        return correlation_table

    def get_wcs(
        self, job_id: str = None, temp_filename: str = None, delete_after: bool = True
    ) -> hint.WCS:
        """This obtains the wcs header file and then computes World Coordinate
        System solution from it. Because astrometry.net computes it for us,
        we just extract it from the header file using Astropy.

        Parameters
        ----------
        job_id : string, default = None
            The ID of the job that the results should be obtained from. If not
            provided, the ID determined by the file upload is used.
        temp_filename : string, default = None
            The filename that the downloaded wcs file will be downloaded as.
            The path is going to still be in the temporary directory.
        delete_after : bool, default = True
            Delete the file after downloading it to extract its information.

        Returns
        -------
        wcs : Astropy WCS
            The world coordinate solution class for the image provided.
        """
        job_id = job_id if job_id is not None else self.job_id
        # Download the correlation file to read into a data table.
        upload_filename = library.path.get_filename_without_extension(
            pathname=self.original_upload_filename
        )
        fits_table_filename = (
            temp_filename if temp_filename is not None else upload_filename + "_wcs"
        )
        # The full path of the filename derived from saving it in a temporary
        # directory.
        corr_filename = library.path.merge_pathname(
            filename=fits_table_filename, extension="fits"
        )
        corr_pathname = library.temporary.make_temporary_directory_path(
            filename=corr_filename
        )
        # Save the correlation file.
        self.download_result_file(
            filename=corr_pathname, file_type="wcs", job_id=job_id
        )
        # Load the header from the file.
        wcs_header = library.fits.read_fits_header(filename=corr_pathname)
        wcs = ap_wcs.WCS(wcs_header)

        # Delete the temporary file after loading it if desired.
        if delete_after:
            os.remove(corr_pathname)
        return wcs

    def upload_file(self, pathname: str, **kwargs) -> dict:
        """A wrapper to allow for the uploading of files or images to the API.

        This also determines the submission ID and the job ID for the uploaded
        image and saves it.

        Parameters
        ----------
        pathname : str
            The pathname of the file to open. The filename is extracted and
            used as well.

        Returns
        -------
        results : dict
            The results of the API call to upload the image.
        """
        # When uploading a new file, the submission and job IDs will change.
        # They must be reset because of their read-only nature.
        del self.submission_id, self.job_id

        # Save the file information.
        self.original_upload_filename = pathname

        args = self._generate_upload_args(**kwargs)
        # Process the file upload.
        file_args = None
        try:
            file = open(pathname, "rb")
            filename = library.path.get_filename_with_extension(pathname=pathname)
            file_args = {"filename": filename, "data": file.read()}
        except IOError:
            raise error.FileError("File does not exist: {path}".format(path=pathname))
        # Extract the submission id. This allows for easier
        # association between this class instance and the uploaded file.
        upload_results = self._send_web_request("upload", args, file_args)
        self._image_return_results = upload_results
        return upload_results

    def download_result_file(
        self, filename: str, file_type: str, job_id: str = None
    ) -> None:
        """Downloads fits data table files which correspond to the job id.

        Parameters
        ----------
        filename : str
            The filename of the file when it is downloaded and saved to disk.
        file_type : str
            The type of file to be downloaded from astrometry.net. It should
            one of the following:

                - `wcs`: The world coordinate data table file.
                - `new_fits`, `new_image`: A new fits file, containing the
                  original image, annotations, and WCS header information.
                - `rdls`: A table of reference stars nearby.
                - `axy`: A table in of the location of stars detected in the
                  provided image.
                - `corr`: A table of the correspondences between reference
                  stars location in the sky and in pixel space.

        job_id : str, default = None
            The ID of the job that the results should be obtained from. If not
            provided, the ID determined by the file upload is used.

        Returns
        -------
        None
        """
        # Get the proper job ID.
        job_id = job_id if job_id is not None else self.job_id
        # Ensure that the type provided is a valid type which we can pull
        # from the API service. Accommodating for capitalization.
        file_type = str(file_type).lower()
        valid_api_file_types = ("wcs", "new_fits", "rdls", "axy", "corr")
        if file_type not in valid_api_file_types:
            raise error.WebRequestError(
                "The provided file type to be downloaded is not a valid type which can"
                " be downloaded, it must be one of: {fty}".format(
                    fty=valid_api_file_types
                )
            )
        # Construct the URL for the request. It is a little different from the
        # normal API scheme so a new method is made.
        def _construct_file_download_url(ftype: str, id: str) -> str:
            """Construct the file curl from the file type `ftype` and the
            job id `id`."""
            url = "http://nova.astrometry.net/{_type}_file/{_id}".format(
                _type=ftype, _id=id
            )
            return url

        file_download_url = _construct_file_download_url(ftype=file_type, id=job_id)
        # Before downloading the file, check that the file actually exists.
        if job_id is None:
            raise error.WebRequestError("There is no job to download the file from.")
        if library.http.get_http_status_code(url=file_download_url) != 200:
            raise error.WebRequestError(
                "The file download link is not giving an acceptable http status code."
                " It is likely that the job is still processing and thus the data files"
                " are not ready."
            )
        # Download the file.
        library.http.download_file_from_url(
            url=file_download_url, filename=filename, overwrite=True
        )
        return None
