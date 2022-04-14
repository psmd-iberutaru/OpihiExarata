"""A data wrapper class which takes in raw Opihi data, flats, and darks and 
produces a valid reduced image.
"""
import copy

import numpy as np

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


class OpihiPreprocessSolution:
    """A class which represents the reduction process of Opihi data, having the
    raw data corrected using previously and provided derived flats and darks.
    The required parameters (such as exposure time) must also be provided.

    This class does not have an engine as there is only one way to reduce data
    provided the systematics of the Opihi telescope itself; as such the
    data is handled straight by this solution class.

    Attributes
    ----------
    _mask_c_fits_filename : string
        The filename for the pixel mask for the clear filter stored in a
        fits file.
    _mask_g_fits_filename : string
        The filename for the pixel mask for the g filter stored in a
        fits file.
    _mask_r_fits_filename : string
        The filename for the pixel mask for the r filter stored in a
        fits file.
    _mask_i_fits_filename : string
        The filename for the pixel mask for the i filter stored in a
        fits file.
    _mask_z_fits_filename : string
        The filename for the pixel mask for the z filter stored in a
        fits file.
    _mask_1_fits_filename : string
        The filename for the pixel mask for the 1 filter stored in a
        fits file.
    _mask_2_fits_filename : string
        The filename for the pixel mask for the 2 filter stored in a
        fits file.
    _mask_3_fits_filename : string
        The filename for the pixel mask for the 3 filter stored in a
        fits file.

    _flat_c_fits_filename : string
        The filename for the flat field for the clear filter stored in a
        fits file.
    _flat_g_fits_filename : string
        The filename for the flat field for the g filter stored in a
        fits file.
    _flat_r_fits_filename : string
        The filename for the flat field for the r filter stored in a
        fits file.
    _flat_i_fits_filename : string
        The filename for the flat field for the i filter stored in a
        fits file.
    _flat_z_fits_filename : string
        The filename for the flat field for the z filter stored in a
        fits file.
    _flat_1_fits_filename : string
        The filename for the flat field for the 1 filter stored in a
        fits file.
    _flat_2_fits_filename : string
        The filename for the flat field for the 2 filter stored in a
        fits file.
    _flat_3_fits_filename : string
        The filename for the flat field for the 3 filter stored in a
        fits file.

    _bias_fits_filename : string
        The filename for the per-pixel bias values of the data,
        stored in a fits file.
    _dark_rate_fits_filename : string
        The filename for the per-pixel rate values of the dark data,
        stored in a fits file.
    _linearity_fits_filename : string
        The filename for the linearity responce of the CCD. This should be a
        1D fits file detailing counts as a function of time for the saturation
        curve of the CCD.


    mask_c : array
        The pixel mask for the clear filter as determined by the provided
        fits file.
    mask_g : array
        The pixel mask for the g filter as determined by the provided
        fits file.
    mask_r : array
        The pixel mask for the r filter as determined by the provided
        fits file.
    mask_i : array
        The pixel mask for the i filter as determined by the provided
        fits file.
    mask_z : array
        The pixel mask for the z filter as determined by the provided
        fits file.
    mask_1 : array
        The pixel mask for the 1 filter as determined by the provided
        fits file.
    mask_2 : array
        The pixel mask for the 2 filter as determined by the provided
        fits file.
    mask_3 : array
        The pixel mask for the 3 filter as determined by the provided
        fits file.

    flat_c : array
        The flat field for the clear filter as determined by the provided
        fits file.
    flat_g : array
        The flat field for the g filter as determined by the provided
        fits file.
    flat_r : array
        The flat field for the r filter as determined by the provided
        fits file.
    flat_i : array
        The flat field for the i filter as determined by the provided
        fits file.
    flat_z : array
        The flat field for the z filter as determined by the provided
        fits file.
    flat_1 : array
        The flat field for the 1 filter as determined by the provided
        fits file.
    flat_2 : array
        The flat field for the 2 filter as determined by the provided
        fits file.
    flat_3 : array
        The flat field for the 3 filter as determined by the provided
        fits file.


    bias : array
        The bias array as determined by the provided fits file.
    dark_rate : array
        The dark rate, per pixel, as determined by the provided fits file.
    linearity_function : function
        The linearity function across the whole CCD. It is an average function
        across all of the pixels.
    """

    def __init__(
        self,
        mask_c_fits_filename: str,
        mask_g_fits_filename: str,
        mask_r_fits_filename: str,
        mask_i_fits_filename: str,
        mask_z_fits_filename: str,
        mask_1_fits_filename: str,
        mask_2_fits_filename: str,
        mask_3_fits_filename: str,
        flat_c_fits_filename: str,
        flat_g_fits_filename: str,
        flat_r_fits_filename: str,
        flat_i_fits_filename: str,
        flat_z_fits_filename: str,
        flat_1_fits_filename: str,
        flat_2_fits_filename: str,
        flat_3_fits_filename: str,
        bias_fits_filename: str,
        dark_rate_fits_filename: str,
        linearity_fits_filename: str,
    ) -> None:
        """Instantiation of the reduced Opihi data class.

        Parameters
        ----------
        mask_c_fits_filename : string
            The filename for the pixel mask in the clear filter stored in a
            fits file.
        mask_g_fits_filename : string
            The filename for the pixel mask in the g filter stored in a
            fits file.
        mask_r_fits_filename : string
            The filename for the pixel mask in the r filter stored in a
            fits file.
        mask_i_fits_filename : string
            The filename for the pixel mask in the i filter stored in a
            fits file.
        mask_z_fits_filename : string
            The filename for the pixel mask in the z filter stored in a
            fits file.
        mask_1_fits_filename : string
            The filename for the pixel mask in the 1 filter stored in a
            fits file.
        mask_2_fits_filename : string
            The filename for the pixel mask in the 2 filter stored in a
            fits file.
        mask_3_fits_filename : string
            The filename for the pixel mask in the 3 filter stored in a
            fits file.

        flat_c_fits_filename : string
            The filename for the flat field in the clear filter stored in a
            fits file.
        flat_g_fits_filename : string
            The filename for the flat field in the g filter stored in a
            fits file.
        flat_r_fits_filename : string
            The filename for the flat field in the r filter stored in a
            fits file.
        flat_i_fits_filename : string
            The filename for the flat field in the i filter stored in a
            fits file.
        flat_z_fits_filename : string
            The filename for the flat field in the z filter stored in a
            fits file.
        flat_1_fits_filename : string
            The filename for the flat field in the 1 filter stored in a
            fits file.
        flat_2_fits_filename : string
            The filename for the flat field in the 2 filter stored in a
            fits file.
        flat_3_fits_filename : string
            The filename for the flat field in the 3 filter stored in a
            fits file.


        bias_fits_filename : string
            The filename for the per-pixel bias values of the data,
            stored in a fits file.
        dark_rate_fits_filename : string
            The filename for the per-pixel rate values of the dark data,
            stored in a fits file.
        linearity_fits_filename : string
            The filename for the linearity responce of the CCD, stored as a
            text file.

        Returns
        -------
        None
        """
        # Adding the raw inputs as they may be needed later for some reason.
        # Mask files, per filter.
        self._mask_c_fits_filename = mask_c_fits_filename
        self._mask_g_fits_filename = mask_g_fits_filename
        self._mask_r_fits_filename = mask_r_fits_filename
        self._mask_i_fits_filename = mask_i_fits_filename
        self._mask_z_fits_filename = mask_z_fits_filename
        self._mask_1_fits_filename = mask_1_fits_filename
        self._mask_2_fits_filename = mask_2_fits_filename
        self._mask_3_fits_filename = mask_3_fits_filename
        # Flat files, per filter.
        self._flat_c_fits_filename = flat_c_fits_filename
        self._flat_g_fits_filename = flat_g_fits_filename
        self._flat_r_fits_filename = flat_r_fits_filename
        self._flat_i_fits_filename = flat_i_fits_filename
        self._flat_z_fits_filename = flat_z_fits_filename
        self._flat_1_fits_filename = flat_1_fits_filename
        self._flat_2_fits_filename = flat_2_fits_filename
        self._flat_3_fits_filename = flat_3_fits_filename
        # Bias, filter independent.
        self._bias_fits_filename = bias_fits_filename
        # Dark rate, filter independent.
        self._dark_rate_fits_filename = dark_rate_fits_filename
        # Linearity, filter independent.
        self._linearity_fits_filename = linearity_fits_filename
        # Reading the fits file data.
        self.__init_read_mask_data()
        self.__read_flat_data()
        # Reading the linearity data and create the linearity function.
        self.__init_linearity_data()

        # All done.
        return None

    def __init_read_mask_data(self) -> None:
        """This function just reads all of the fits file data for the
        filter-dependent pixel masks and puts it where it belongs per the
        documentation.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Reading all of the mask files.
        __, mask_c = library.fits.read_fits_image_file(
            filename=self._mask_c_fits_filename
        )
        __, mask_g = library.fits.read_fits_image_file(
            filename=self._mask_g_fits_filename
        )
        __, mask_r = library.fits.read_fits_image_file(
            filename=self._mask_r_fits_filename
        )
        __, mask_i = library.fits.read_fits_image_file(
            filename=self._mask_i_fits_filename
        )
        __, mask_z = library.fits.read_fits_image_file(
            filename=self._mask_z_fits_filename
        )
        __, mask_1 = library.fits.read_fits_image_file(
            filename=self._mask_1_fits_filename
        )
        __, mask_2 = library.fits.read_fits_image_file(
            filename=self._mask_2_fits_filename
        )
        __, mask_3 = library.fits.read_fits_image_file(
            filename=self._mask_3_fits_filename
        )
        # Adding the masks to this solution so the fits files need not be
        # accessed again.
        self.mask_c = mask_c
        self.mask_g = mask_g
        self.mask_r = mask_r
        self.mask_i = mask_i
        self.mask_z = mask_z
        self.mask_1 = mask_1
        self.mask_2 = mask_2
        self.mask_3 = mask_3
        return None

    def __init_read_flat_data(self) -> None:
        """This function just reads all of the fits file data for the
        filter-dependent flat fields and puts it where it belongs per the
        documentation.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Reading all of the flat files.
        __, flat_c = library.fits.read_fits_image_file(
            filename=self._flat_c_fits_filename
        )
        __, flat_g = library.fits.read_fits_image_file(
            filename=self._flat_g_fits_filename
        )
        __, flat_r = library.fits.read_fits_image_file(
            filename=self._flat_r_fits_filename
        )
        __, flat_i = library.fits.read_fits_image_file(
            filename=self._flat_i_fits_filename
        )
        __, flat_z = library.fits.read_fits_image_file(
            filename=self._flat_z_fits_filename
        )
        __, flat_1 = library.fits.read_fits_image_file(
            filename=self._flat_1_fits_filename
        )
        __, flat_2 = library.fits.read_fits_image_file(
            filename=self._flat_2_fits_filename
        )
        __, flat_3 = library.fits.read_fits_image_file(
            filename=self._flat_3_fits_filename
        )
        # Adding the flats to this solution so the fits files need not be
        # accessed again.
        self.flat_c = flat_c
        self.flat_g = flat_g
        self.flat_r = flat_r
        self.flat_i = flat_i
        self.flat_z = flat_z
        self.flat_1 = flat_1
        self.flat_2 = flat_2
        self.flat_3 = flat_3

    def __init_read_linearity_data(self):
        """This function reads all of the linearity data and creates a
        function for linearity. First order interpolation is done on this data.

        It is expected that the data from the linearity filename is of high
        enough resolution that first order interpolation is good enough.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

    def preprocess_data_image(
        self, raw_data: hint.array, exposure_time: float
    ) -> hint.array:
        """The formal reduction algorithm for data from Opihi. It follows
        preprocessing instructions for CCDs.

        Parameters
        ----------
        data : array-like
            The raw image data from the Opihi telescope.
        exposure_time : float
            The exposure time of the image in seconds.

        Returns
        -------
        preprocess_data : array
            The data, after it has been preprocessed.
        """
        # TODO
        raise error.DevelopmentError



    def preprocess_fits_file(
        self, raw_filename: str, out_filename: str = None
    ) -> tuple[hint.Header, hint.array]:
        """Preprocess an Opihi image, the provided fits filename is read, the
        needed information extracted from it, and it is processed using
        historical archive calibration files created per the documentation and
        specified by the configuration files.

        Parameters
        ----------
        raw_filename : str
            The filename of the raw fits file image from Opihi.
        out_filename : str, default = None
            The filename to save the reduced image as a fits file. Some added
            entries are added to the header. If this is not provided as
            defaults to None, no file is saved.

        Returns
        -------
        preprocess_header : Astropy Header
            The header of the fits file after preprocessing. Some added
            entries are present to document information from preprocessing.
        preprocess_data : array
            The data array of the image after the raw image went through the
            preprocess reduction.
        """
        # Read the needed fits information to do the reduction.
        raw_header, raw_data = library.fits.read_fits_image_file(filename=raw_filename)
        # The exposure time is needed for reducing the image data. (The fits
        # file uses integration time as the name.)
        raw_exposure_time = float(raw_header["itime"])

        # Preprocessing the data.
        preprocess_data = self.preprocess_data_image(
            raw_data=raw_data, exposure_time=raw_exposure_time
        )

        # Adding helpful preprocessing information to the header, just in the
        # event it may be needed. Using a copy just in case.
        preprocess_header = copy.deepcopy(raw_header)
        # TODO.
        

        # If the user wanted to save the preprocessed data as a file.
        if isinstance(out_filename, str):
            # Assume it is a valid path, if it is not, the writing function or
            # Astropy will likely bark.
            library.fits.write_fits_image_file(
                filename=out_filename,
                header=preprocess_header,
                data=preprocess_data,
                overwrite=False,
            )
        elif out_filename is not None:
            # The outgoing filename is entered but it was not an acceptable
            # path as a string, this is an error (likely on the development
            # side).
            raise error.InputError(
                "The out filename provided is not a string; therefore, it cannot be"
                " interpreted as a path where which the preprocessed file would be"
                " saved."
            )
        else:
            # The file is not to be saved.
            pass

        # All done.
        return preprocess_header, preprocess_data
