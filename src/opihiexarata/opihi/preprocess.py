"""A data wrapper class which takes in raw Opihi data, flats, and darks and
produces a valid reduced image.
"""

# isort: split
# Import required to remove circular dependencies from type checking.
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opihiexarata.library import hint
# isort: split

import copy
import os

import numpy as np
import scipy.optimize as sp_optimize

from opihiexarata import library
from opihiexarata.library import error


class OpihiPreprocessSolution(library.engine.ExarataSolution):
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
    _mask_b_fits_filename : string
        The filename for the pixel mask for the block filter stored in a
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
    _flat_b_fits_filename : string
        The filename for the flat field for the block filter stored in a
        fits file.

    _bias_fits_filename : string
        The filename for the per-pixel bias values of the data,
        stored in a fits file.
    _dark_current_fits_filename : string
        The filename for the per-pixel rate values of the dark data,
        stored in a fits file.
    _linearity_fits_filename : string
        The filename for the linearity response of the CCD. This should be a
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
    mask_b : array
        The pixel mask for the block filter as determined by the provided
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
    flat_b : array
        The flat field for the block filter as determined by the provided
        fits file.


    bias : array
        The bias array as determined by the provided fits file.
    dark_current : array
        The dark rate, per pixel, as determined by the provided fits file.
        The dark current unit is counts / second.
    linearity_factors : array
        The polynomial factors of the linearity function starting from the
        0th order.
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
        mask_b_fits_filename: str,
        flat_c_fits_filename: str,
        flat_g_fits_filename: str,
        flat_r_fits_filename: str,
        flat_i_fits_filename: str,
        flat_z_fits_filename: str,
        flat_1_fits_filename: str,
        flat_2_fits_filename: str,
        flat_b_fits_filename: str,
        bias_fits_filename: str,
        dark_current_fits_filename: str,
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
        mask_b_fits_filename : string
            The filename for the pixel mask in the block filter stored in a
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
        flat_b_fits_filename : string
            The filename for the flat field in the block filter stored in a
            fits file.


        bias_fits_filename : string
            The filename for the per-pixel bias values of the data,
            stored in a fits file.
        dark_current_fits_filename : string
            The filename for the per-pixel rate values of the dark data,
            stored in a fits file.
        linearity_fits_filename : string
            The filename for the linearity response of the CCD, stored as a
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
        self._mask_b_fits_filename = mask_b_fits_filename
        # Flat files, per filter.
        self._flat_c_fits_filename = flat_c_fits_filename
        self._flat_g_fits_filename = flat_g_fits_filename
        self._flat_r_fits_filename = flat_r_fits_filename
        self._flat_i_fits_filename = flat_i_fits_filename
        self._flat_z_fits_filename = flat_z_fits_filename
        self._flat_1_fits_filename = flat_1_fits_filename
        self._flat_2_fits_filename = flat_2_fits_filename
        self._flat_b_fits_filename = flat_b_fits_filename
        # Bias, filter independent.
        self._bias_fits_filename = bias_fits_filename
        # Dark rate, filter independent.
        self._dark_current_fits_filename = dark_current_fits_filename
        # Linearity, filter independent.
        self._linearity_fits_filename = linearity_fits_filename
        # Reading the fits file data. There are inner functions for mask and
        # flats for organizational purposes.
        self.__init_read_bias_data()
        self.__init_read_dark_current_data()
        self.__init_read_mask_data()
        self.__init_read_flat_data()
        # Reading the linearity data and create the linearity function.
        self.__init_read_linearity_data()

        # All done.

    def __init_read_bias_data(self) -> None:
        """This function reads the bias data from the fits file.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        # We try and read the file, if it exists.
        if not os.path.exists(self._bias_fits_filename):
            error.warn(
                warn_class=error.InputWarning,
                message=(
                    f"Bias filename does not exist: {self._bias_fits_filename}"
                ),
            )
        # Otherwise we read then apply the bias file. We do not care about the
        # header.
        __, bias = library.fits.read_fits_image_file(
            filename=self._bias_fits_filename,
        )
        self.bias = bias

    def __init_read_dark_current_data(self) -> None:
        """This function reads the dark current data from the fits file.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        # We try and read the file, if it exists.
        if not os.path.exists(self._dark_current_fits_filename):
            error.warn(
                warn_class=error.InputWarning,
                message=(
                    "Dark current filename does not exist:"
                    f" {self._dark_current_fits_filename}"
                ),
            )
        # Otherwise we read then apply the dark current file. We do not care
        # about the header.
        __, dark_current = library.fits.read_fits_image_file(
            filename=self._dark_current_fits_filename,
        )
        self.dark_current = dark_current

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

        # Internal reading function so we can handle logging warnings and the
        # like.
        def read_mask_wrapper(
            filename: str,
            filter_name: str = "?",
        ) -> hint.ndarray:
            """Read a mask FITS file.

            Parameters
            ----------
            filename : str
                The filename of the mask we are going to read.
            filter_name : str, default = ?
                The filter name which we are going to use for any warnings or
                errors. Not required but useful for debugging.

            Returns
            -------
            mask_data : ndarray
                The mask.

            """
            # We try and read the file, if it exists.
            if not os.path.exists(filename):
                error.warn(
                    warn_class=error.InputWarning,
                    message=(
                        f"Filter mask {filter_name} filename does not exist:"
                        f" {filename}"
                    ),
                )

            # Lastly, we read the file. We do not care about the header.
            __, mask_data_raw = library.fits.read_fits_image_file(
                filename=filename,
            )
            # Adding the masks to this solution so the fits files need not be
            # accessed again. A pixel is considered mask if the value is True.
            mask_data = np.array(mask_data_raw, dtype=bool)
            return mask_data

        # Reading all of the mask files.
        self.mask_c = read_mask_wrapper(
            filename=self._mask_c_fits_filename,
            filter_name="c",
        )
        self.mask_g = read_mask_wrapper(
            filename=self._mask_g_fits_filename,
            filter_name="g",
        )
        self.mask_r = read_mask_wrapper(
            filename=self._mask_r_fits_filename,
            filter_name="r",
        )
        self.mask_i = read_mask_wrapper(
            filename=self._mask_i_fits_filename,
            filter_name="i",
        )
        self.mask_z = read_mask_wrapper(
            filename=self._mask_z_fits_filename,
            filter_name="z",
        )
        self.mask_1 = read_mask_wrapper(
            filename=self._mask_1_fits_filename,
            filter_name="1",
        )
        self.mask_2 = read_mask_wrapper(
            filename=self._mask_2_fits_filename,
            filter_name="2",
        )
        self.mask_b = read_mask_wrapper(
            filename=self._mask_b_fits_filename,
            filter_name="b",
        )
        # All done.

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

        # Internal reading function so we can handle logging warnings and the
        # like.
        def read_flat_wrapper(
            filename: str,
            filter_name: str = "?",
        ) -> hint.ndarray:
            """Read a flat FITS file.

            Parameters
            ----------
            filename : str
                The filename of the flat we are going to read.
            filter_name : str, default = ?
                The filter name which we are going to use for any warnings or
                errors. Not required but useful for debugging.

            Returns
            -------
            flat_data : ndarray
                The flat.

            """
            # We try and read the file, if it exists.
            if not os.path.exists(filename):
                error.warn(
                    warn_class=error.InputWarning,
                    message=(
                        f"Filter flat {filter_name} filename does not exist:"
                        f" {filename}"
                    ),
                )

            # Lastly, we read the file. We do not care about the header.
            __, flat_data_raw = library.fits.read_fits_image_file(
                filename=filename,
            )
            # Adding the masks to this solution so the fits files need not be
            # accessed again. A pixel is considered mask if the value is True.
            flat_data = np.array(flat_data_raw)
            return flat_data

        # Reading all of the mask files.
        self.flat_c = read_flat_wrapper(
            filename=self._flat_c_fits_filename,
            filter_name="c",
        )
        self.flat_g = read_flat_wrapper(
            filename=self._flat_g_fits_filename,
            filter_name="g",
        )
        self.flat_r = read_flat_wrapper(
            filename=self._flat_r_fits_filename,
            filter_name="r",
        )
        self.flat_i = read_flat_wrapper(
            filename=self._flat_i_fits_filename,
            filter_name="i",
        )
        self.flat_z = read_flat_wrapper(
            filename=self._flat_z_fits_filename,
            filter_name="z",
        )
        self.flat_1 = read_flat_wrapper(
            filename=self._flat_1_fits_filename,
            filter_name="1",
        )
        self.flat_2 = read_flat_wrapper(
            filename=self._flat_2_fits_filename,
            filter_name="2",
        )
        self.flat_b = read_flat_wrapper(
            filename=self._flat_b_fits_filename,
            filter_name="b",
        )
        # All done.

    def __init_read_linearity_data(self) -> None:
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
        # We try and read the file, if it exists.
        if not os.path.exists(self._linearity_fits_filename):
            error.warn(
                warn_class=error.InputWarning,
                message=(
                    "Linearity data filename does not exist:"
                    f" {self._linearity_fits_filename}"
                ),
            )

        # Obtaining the saturation function via the points provided.
        unsaturated_signal, saturated_signal = np.genfromtxt(
            self._linearity_fits_filename,
        ).T

        # Using just 2nd order linearity correction to fit the saturation
        # function.
        def _polynomial(
            x: hint.array,
            a: float,
            b: float,
            c: float,
        ) -> hint.array:
            return a + b * x + c * x**2

        # Fitting.
        self.linearity_factors, __ = sp_optimize.curve_fit(
            _polynomial,
            saturated_signal,
            unsaturated_signal,
        )

        # Using the fitted parameters to derive the linearity curve. Using
        # keywords here may be unnecessary.
        self.linearity_function = lambda r: _polynomial(
            r,
            *self.linearity_factors,
        )
        # All done.

    def preprocess_data_image(
        self,
        raw_data: hint.array,
        exposure_time: float,
        filter_name: str,
    ) -> hint.array:
        """The formal reduction algorithm for data from Opihi. It follows
        preprocessing instructions for CCDs.

        Parameters
        ----------
        raw_data : array-like
            The raw image data from the Opihi telescope.
        exposure_time : float
            The exposure time of the image in seconds.
        filter_name : string
            The name of the filter which the image was taken in, used to
            select the correct flat and mask file.

        Returns
        -------
        preprocess_data : array
            The data, after it has been preprocessed.

        """
        # Get the needed mask and flat files based on the provided filter.
        # Being a little clever so a very long if/else statement is not used.
        try:
            mask = self.__dict__.get(f"mask_{filter_name}", None)
            flat = self.__dict__.get(f"flat_{filter_name}", None)
            if mask is None or flat is None:
                raise error.IntentionalError(
                    "Intentional raise to trigger other error.",
                )
        except error.IntentionalError:
            # The filters are not in this class itself as per the structure of
            # this class and its initialization. Likely, the filter name is
            # wrong.
            raise error.InputError(
                f"The filter name {filter_name} is not a filter name that is a"
                " part of the OpihiExarata system and this class does not a"
                " flat or mask for said filter for reduction purposes.",
            )

        # All of the arrays must be the same shape for the Numpy array math
        # to work out.
        if (
            raw_data.shape
            == self.bias.shape
            == self.dark_current.shape
            == flat.shape
            == mask.shape
        ):
            # All good.
            pass
        else:
            raise error.InputError(
                "The data array does not have the same shape as all of the"
                " other data reduction arrays.",
            )

        # Reducing it based on the documentation method. Inverting  the
        # linearity and then removing the dark and bias then flat field
        # correction.
        unmasked_preprocess_data = (
            self.linearity_function(raw_data)
            - self.bias
            - exposure_time * self.dark_current
        ) / flat
        # Adding the mask to the data.
        preprocess_data = copy.deepcopy(unmasked_preprocess_data)
        preprocess_data[mask] = np.nan
        return preprocess_data

    def preprocess_fits_file(
        self,
        raw_filename: str,
        out_filename: str = None,
        overwrite: bool = False,
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
        overwrite : bool, default = False
            If overwrite is True, the filename is overwritten in the event of
            a collision.

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
        raw_header, raw_data = library.fits.read_fits_image_file(
            filename=raw_filename,
        )
        # The exposure time is needed for reducing the image data. (The fits
        # file uses integration time as the name.)
        raw_exposure_time = float(raw_header["ITIME"])
        # Filter name.
        filter_header_string = str(raw_header["FWHL"])
        filter_name = library.conversion.filter_header_string_to_filter_name(
            header_string=filter_header_string,
        )

        # Preprocessing the data.
        preprocess_data = self.preprocess_data_image(
            raw_data=raw_data,
            exposure_time=raw_exposure_time,
            filter_name=filter_name,
        )

        # Adding helpful preprocessing information to the header, we follow
        # the convention for all OpihiExarata data.
        preprocess_header_entries = {
            "OXM_REDU": True,
        }
        # Adding it using the library function so that the defaults may be
        # added as well.
        preprocess_header = library.fits.update_opihiexarata_fits_header(
            header=raw_header,
            entries=preprocess_header_entries,
        )
        # If the user wanted to save the preprocessed data as a file.
        if isinstance(out_filename, str):
            # Assume it is a valid path, if it is not, the writing function or
            # Astropy will likely bark.
            library.fits.write_fits_image_file(
                filename=out_filename,
                header=preprocess_header,
                data=preprocess_data,
                overwrite=overwrite,
            )
        elif out_filename is not None:
            # The outgoing filename is entered but it was not an acceptable
            # path as a string, this is an error (likely on the development
            # side).
            raise error.InputError(
                "The out filename provided is not a string; therefore, it"
                " cannot be interpreted as a path where which the preprocessed"
                " file would be saved.",
            )
        else:
            # The file is not to be saved.
            pass

        # All done.
        return preprocess_header, preprocess_data
