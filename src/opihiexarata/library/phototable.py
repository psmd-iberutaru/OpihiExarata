"""This is a module for uniform handling of the photometric star table.
Many different databases will have their own standards and so functions and
classes helpful for unifying all of their different entries into one uniform
table which the software can expect are detailed here."""

import numpy as np
import astropy.table as ap_table

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

# The general template of the photometric table.
OPIHI_FILTERS = ("c", "g", "r", "i", "z", "1", "2", "b")
__PHOTOMETRY_TABLE_NAME_TYPE_PAIR = {
    "ra_photo": float,
    "dec_photo": float,
    "c_mag": float,
    "c_err": float,
    "g_mag": float,
    "g_err": float,
    "r_mag": float,
    "r_err": float,
    "i_mag": float,
    "i_err": float,
    "z_mag": float,
    "z_err": float,
    "1_mag": float,
    "1_err": float,
    "2_mag": float,
    "2_err": float,
    "b_mag": float,
    "b_err": float,
}
PHOTOMETRY_TABLE_COLUMN_NAMES = list(__PHOTOMETRY_TABLE_NAME_TYPE_PAIR.keys())
PHOTOMETRY_TABLE_COLUMN_TYPES = list(__PHOTOMETRY_TABLE_NAME_TYPE_PAIR.values())

# The general template of the photometric table. Honestly, this is just a
# sorting thing and may actually not even be needed in the future. However,
# we have it here just in case.
__INTERSECTION_ASTROPHOTO_TABLE_NAME_TYPE_PAIR = {
    "ra_astro": float,
    "dec_astro": float,
    "ra_photo": float,
    "dec_photo": float,
    "pixel_x": float,
    "pixel_y": float,
    "separation": float,
    "c_mag": float,
    "c_err": float,
    "g_mag": float,
    "g_err": float,
    "r_mag": float,
    "r_err": float,
    "i_mag": float,
    "i_err": float,
    "z_mag": float,
    "z_err": float,
    "1_mag": float,
    "1_err": float,
    "2_mag": float,
    "2_err": float,
    "b_mag": float,
    "b_err": float,
    "counts": float,
}
INTERSECTION_ASTROPHOTO_TABLE_COLUMN_NAMES = list(
    __INTERSECTION_ASTROPHOTO_TABLE_NAME_TYPE_PAIR.keys()
)
INTERSECTION_ASTROPHOTO_TABLE_COLUMN_TYPES = list(
    __INTERSECTION_ASTROPHOTO_TABLE_NAME_TYPE_PAIR.values()
)


def blank_photometry_table() -> hint.Table:
    """Creates a blank table which contains the columns which are the unified
    photometry table.

    Parameters
    ----------
    None

    Returns
    -------
    blank_table : Astropy Table
        The table with only the column headings; no records are in the table.
    """
    # The names of the columns
    column_names = PHOTOMETRY_TABLE_COLUMN_NAMES
    data_types = PHOTOMETRY_TABLE_COLUMN_TYPES
    blank_table = ap_table.Table(names=column_names, dtype=data_types)
    return blank_table


def fill_incomplete_photometry_table(partial_table: hint.Table) -> hint.Table:
    """This function takes a photometry table which is partially standardized
    but may be missing a few columns or rows and fills in the missing values
    with NaNs so that the resulting table is a standardized table for the
    OpihiExarata software.

    Metadata is added to the resulting table to signify that it is a complete
    photometry table as standardized by OpihiExarata.

    Parameters
    ----------
    partial_table : Table
        A table which partially covers the photometry table standard but is
        otherwise missing a few records.

    complete_table : Table
        A completed form of the partial table which is standardized to the
        expectations of the photometry table.
    """
    # A totally blank column for the cases where there are no observations of
    # a given filter for either the magnitude or error in the magnitude.
    table_length = len(partial_table)
    nan_column = np.full(table_length, np.nan)

    # Extracting the available columns (filters) and information from these
    # columns. If there is missing data, we fill it in as a blank column.
    photometry_table_dict = {}
    for colnamedex in PHOTOMETRY_TABLE_COLUMN_NAMES:
        # Instantiating the variables else a NameError may arise.
        column_name = None
        column_data = None
        try:
            # Attempting to extract the information, if this partial table has
            # the information of course.
            column_name = colnamedex
            column_data = partial_table[colnamedex].data
        except KeyError:
            # This partial table does not have a column for the information
            # about this particular photometry column, using blanks.
            column_name = colnamedex
            column_data = nan_column
        except Exception:
            # If there is another error, then it is likely something is very
            # wrong with the table, but we do not know.
            raise error.UndiscoveredError(
                "For some reason, the partial table cannot be accessed as expected for"
                " a partial photometry table. Check the error stack."
            )
        finally:
            # The information to be added to the photometry table. We do check
            # that the name and data was extracted, somehow.
            if column_name is None and column_data is None:
                raise error.DevelopmentError(
                    "For some reason, the information about {col} from the partial"
                    " table was not extracted or detected to be missing.".format(
                        col=colnamedex
                    )
                )
            else:
                # Adding the information.
                photometry_table_dict[column_name] = column_data

    # Compile the dictionary into an Astropy table.
    complete_table = ap_table.Table(photometry_table_dict)
    # Double checking that all of the columns are there as expected by the
    # standard table.
    if complete_table.colnames != PHOTOMETRY_TABLE_COLUMN_NAMES:
        raise error.DevelopmentError(
            "The standard photometry table derived from the partial table does not have"
            " the same columns as expected from a standard photometry table."
        )
    # All done.
    return complete_table
