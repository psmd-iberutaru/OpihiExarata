"""Functions to help with image and array manipulations."""

import os
import numpy as np
import PIL.Image
import scipy.ndimage as sp_ndimage
import skimage.registration as ski_registration

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


def slice_array_boundary(
    array: hint.array, x_min: int, x_max: int, y_min: int, y_max: int
) -> hint.array:
    """Slice an image array such that it stops at the boundaries and does not
    exceed past it. This function basically handels runtime slicing, but it
    returns a copy.

    This function does not wrap around slices.

    Parameters
    ----------
    array : array-like
        The base array which the slice will access.
    x_min : int
        The lower index bound of the x-axis slice.
    x_max : int
        The upper index bound of the x-axis slice.
    y_min : int
        The lower index bound of the y-axis slice.
    y_max : int
        The upper index bound of the y-axis slice.

    Returns
    -------
    boundary_sliced_array : array-like
        The array, sliced while adhering to the boundary of the slices.
    """
    # The maximum value that a slice can have is determined by their column
    # and row count.
    n_rows, n_cols = array.shape
    # Negative slices are already invalid and out of bounds.
    x_min = 0 if x_min <= 0 else x_min
    x_max = n_cols if x_max <= 0 else x_max
    y_min = 0 if y_min <= 0 else y_min
    y_max = n_rows if y_max <= 0 else y_max
    # Likewise, if any of the indexes exceed the bounds of the array, force
    # them back.
    x_max = n_cols if n_cols < x_max else x_max
    y_max = n_rows if n_rows < y_max else y_max
    # Return the slice with these bounds.
    boundary_sliced_array = array[y_min:y_max, x_min:x_max]
    return boundary_sliced_array


def scale_image_array(
    array: hint.array,
    minimum: float,
    maximum: float,
    lower_percent_cut: float = 0,
    upper_percent_cut: float = 0,
) -> hint.array:
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


def translate_image_array(
    array: hint.array, shift_x: float = 0, shift_y: float = 0, pad_value: float = np.nan
) -> hint.array:
    """This function translates an image or array in some direction. The image
    is treated as value padded so pixels beyond the scope of the image after
    translation are given by the value specified.

    Parameters
    ----------
    array : array
        The image array which is going to be translated.
    shift_x : float, default = 0
        The number of pixels the image will be shifted in the x direction.
    shift_y : float, default = 0
        The number of pixels the image will be shifted in the y direction.
    pad_value : float, default = np.nan
        The value to pad around the image.

    Returns
    -------
    shifted_image : array
        The image array after shifting.
    """
    # The padded values, assumed to be NaN.
    # Using Scipy's built-in shifting function.
    shifted_array = sp_ndimage.shift(
        array,
        (shift_y, shift_x),
        order=2,
        mode="constant",
        cval=pad_value,
    )
    # All done
    return shifted_array


def determine_translation_image_array(translate_array:hint.array, reference_array:hint.array) -> tuple[float, float]:
    """This function determines the cross-correlated translation 
    required to determine the translation which occurred to the translated 
    array image from the reference array image. 

    This function deals with only translation, it does not handle scaling 
    or rotation. More sophisticated methods are needed for that. This 
    algorithm finds the mode of all translation vectors between star-points 
    in the images.
    
    Parameters
    ----------
    translate_array : array-like
        The array which was translated from the reference array. We are 
        computing the translation of this array.
    reference_array : array-like
        The array before the translation. Inverting the translation on 
        the translate_array returns back to this array.

    Returns
    -------
    delta_x : float
        The x-axis length, in pixels, of the translation vector determined 
        which would translate the translation array back onto the reference
        array.
    delta_y : float
        The y-axis length, in pixels, of the translation vector determined 
        which would translate the translation array back onto the reference
        array.
    """
    # Using scikit's implementation of FFT/DFT. Too high of an up-sample factor
    # leads to slow computation time. 1/100 of a pixel is more than good enough 
    # here.
    translation = ski_registration.phase_cross_correlation(reference_array, translate_array, upsample_factor=100, return_error=False)
    # The function has the axis order in Numpy's convention, we break it up 
    # to match the return signature of this function.
    delta_y, delta_x = translation
    return delta_x, delta_y

def create_circular_mask(
    array: hint.array, center_x: int, center_y: int, radius: float
) -> hint.array:
    """Creates an array which is a circular mask of some radius centered at a
    custom index value location. This process is a little intensive so using
    smaller subsets of arrays are preferred.

    Method inspired by https://stackoverflow.com/a/44874588.

    Parameters
    ----------
    array : array-like
        The data array which the mask will base itself off of. The data in the
        array is not actually modified but it is required for the shape
        definition.
    center_x : integer
        The x-axis coordinate where the mask will be centered.
    center_y : integer
        The y-axis coordinate where the mask will be centered.
    radius : float
        The radius of the circle of the mask in pixels.

    Returns
    -------
    circular_mask : array-like
        The mask; it is the same dimensions of the input data array. If True,
        the the mask should be applied.
    """
    # Creating an array to make the circle, it should be just big enough to
    # create the circle but not too big to have unneeded calculations. To
    # ensure that it is centered, the array should have odd widths.
    width = int(2 * radius) + 3
    width += 1 - (width % 2)
    working_array = np.full((width, width), False)

    # Performing the circular mask calculation on this middle region.
    near_n_rows, near_n_cols = working_array.shape
    near_center_x = near_n_rows // 2
    near_center_y = near_n_cols // 2
    grid_y, grid_x = np.ogrid[:near_n_rows, :near_n_cols]
    dist_sq = (grid_x - near_center_x) ** 2 + (grid_y - near_center_y) ** 2
    near_mask = dist_sq <= radius**2

    # The circular mask is local and should be expanded to the full array's
    # size. Padding is needed in the event that the center pixel is on the
    # edge as the arrays are co-aligned.
    center_x = int(center_x)
    center_y = int(center_y)
    half_width = width // 2
    base_mask = np.full_like(array, False, dtype=bool)
    padded_mask = np.pad(base_mask, width, mode="constant", constant_values=False)
    center_x = int(center_x) + width
    center_y = int(center_y) + width
    padded_mask[
        center_y - half_width : center_y + half_width + 1,
        center_x - half_width : center_x + half_width + 1,
    ] = near_mask
    # Reshape the padded mask to the proper size, the same as the input array.
    circular_mask = padded_mask[width:-width, width:-width]
    # As per Numpy, masked values are considered True in the mask. The current
    # method above creates a circle of True values, so the real mask is the
    # inverse.
    circular_mask = ~circular_mask
    return circular_mask


def save_array_as_png_grayscale(
    array: hint.array, filename: str, overwrite: bool = False
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
