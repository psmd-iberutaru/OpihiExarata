"""Functions to help with image and array manipulations."""

import os
import numpy as np
import PIL.Image

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


def scale_image_array(
    array: hint.ArrayLike,
    minimum: float,
    maximum: float,
    lower_percent_cut: float = 0,
    upper_percent_cut: float = 0,
) -> hint.ArrayLike:
    """This function scales the array to the provided minimum and maximum
    ranges after the percentile masks are taken.

    Parameters
    ----------
    array : array-like
        The array to be scaled.
    minimum : float
        The minimum value of the scaling axis. This will be equal to the
        minimum value of the scaled array after accounting for the percentile
        cuts.
    maximum : float
        The maximum value of the scaling axis. This will be equal to the
        maximum value of the scaled array after accounting for the percentile
        cuts.
    lower_percent_cut : float
        The percent of values that will be masked from the lower end. Must be
        between 0-100.
    upper_percent_cut : float
        The percent of values that will be masked from the upper end. Must be
        between 0-100.

    Returns
    -------
    scaled_array : array-like
        The array, after the scaling.
    """
    # Ensure that the percentile values are within percentile ranges.
    if not 0 <= lower_percent_cut <= 100:
        raise error.InputError(
            "The lower percentile cut should be between 0 <= x <= 100. You provided:"
            " {value}".format(value=lower_percent_cut)
        )
    if not 0 <= upper_percent_cut <= 100:
        raise error.InputError(
            "The upper percentile cut should be between 0 <= x <= 100. You provided:"
            " {value}".format(value=upper_percent_cut)
        )
    # Find where to mask out using the percentile cuts.
    lower_cut = np.nanpercentile(array, lower_percent_cut)
    upper_cut = np.nanpercentile(array, 100 - upper_percent_cut)
    invalid_pixels = np.where(
        np.logical_and(lower_cut <= array, array <= upper_cut), False, True
    )
    # Mask out those values which are invalid.
    array = np.array(array, copy=True)
    array[invalid_pixels] = np.nan
    array[~np.isfinite(array)] = np.nan
    # Scale the array via linear interpolation.
    a_min = np.nanmin(array)
    a_max = np.nanmax(array)
    scaled_array = np.interp(array, (a_min, a_max), (minimum, maximum))
    # Ensuring the invalid pixels are still invalid.
    scaled_array[invalid_pixels] = np.nan
    return scaled_array


def save_array_as_png_grayscale(
    array: hint.ArrayLike, filename: str, overwrite: bool = False
) -> None:
    """This converts an array to a grayscale PNG file.

    The PNG specification requires that the data values be integer. Note that
    if you are saving an array as a PNG, then data may be lost during the
    conversion between float to integer.

    Parameters
    ----------
    array : array-like
        The array that will be saved as a png.
    filename : string
        The filename where the png will be saved. If the filename does not have
        the appropriate filename extension, it will be appended.
    overwrite : boolean
        If the file already exists, should it be overwritten?
    """
    # Check the extension.
    user_ext = library.path.get_file_extension(pathname=filename)
    valid_ext = ("png",)
    if user_ext not in valid_ext:
        # Adding the extension.
        preferred_ext = valid_ext[-1]
        filename_png = library.path.merge_pathname(
            filename=filename, extension=preferred_ext
        )
    else:
        filename_png = filename
    # Check if the file already exists, if it does, check if overwriting was
    # allowed.
    if os.path.isfile(filename_png):
        if overwrite:
            # Overwrite the file by deleting it.
            os.remove(filename_png)
        else:
            raise error.FileError(
                "The png file already exists. Overwrite is False. The image cannot be"
                " saved at the specified path: {path}".format(path=filename_png)
            )
    # Finally, scale the file.
    image_object = PIL.Image.fromarray(array).convert("L")
    image_object.save(filename_png)
    return None
