"""This many wrapper functions for dealing with MPC 80 column standard 
records."""

import astropy as ap
import astropy.table as ap_table

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

MPC_MINOR_PLANET_TABLE_COLUMN_NAMES = [
    "packed_mpc_number",
    "packed_provisional_number",
    "discovery_asterisk",
    "publishable_note",
    "observing_note",
    "date",
    "ra",
    "dec",
    "blank",
    "magnitude_and_band",
    "pseudo_blank",
    "observatory_code",
]


def minor_planet_blank_table() -> hint.Table:
    """Creates a blank table which contains the columns which are recognized by
    the MPC standard 80-column record format.

    Parameters
    ----------
    None

    Returns
    -------
    blank_table : Astropy Table
        The table with only the column headings; no records are in the table.
    """
    # The names of the columns
    column_names = MPC_MINOR_PLANET_TABLE_COLUMN_NAMES
    blank_table = ap_table.Table(names=column_names)
    return blank_table


def minor_planet_record_to_table(records: list[str]) -> hint.Table:
    """This converts an 80 column record for minor planets to a table
    representing the same data.

    The documentation for how the columns are assigned is provided by the
    Minor Planet Center:
    https://www.minorplanetcenter.net/iau/info/OpticalObs.html

    Parameters
    ----------
    records : list
        The records in MPC format. Each entry of the list should be an 80
        column string representing an observed record, a single line.

    Returns
    -------
    table : Astropy Table
        A table containing the same information that is in the MPC record
        format in an easier interface.
    """
    # Each line of the record should be 80 characters long.
    for linedex in records:
        if len(linedex) != 80:
            raise error.InputError(
                "At least one of the lines is not 80 characters in length. It is not a"
                " standard MPC 80-column format."
            )

    # The table which the information will be added into.
    column_names = MPC_MINOR_PLANET_TABLE_COLUMN_NAMES
    # It is easier to make the Table from lists representing rows.
    table_rows = []
    # Going through each of the rows to extract the information into their
    # string representations.
    for linedex in records:
        # Extract the information
        tmp_packed_mp_number = linedex[0:5]
        tmp_packed_prov_desig = linedex[5:12]
        tmp_discovery_asterisk = linedex[12]
        tmp_publish_note = linedex[13]
        tmp_observe_note = linedex[14]
        tmp_obs_date = linedex[15:32]
        tmp_obs_ra = linedex[32:44]
        tmp_obs_dec = linedex[44:56]
        tmp_blank_1 = linedex[56:65]
        tmp_mag_and_band = linedex[65:71]
        tmp_blank_2 = linedex[71:77]
        tmp_observatory_code = linedex[77:80]
        # Apply it as a row to the table rows, it will be converted to a table
        # later.
        table_rows.append(
            [
                tmp_packed_mp_number,
                tmp_packed_prov_desig,
                tmp_discovery_asterisk,
                tmp_publish_note,
                tmp_observe_note,
                tmp_obs_date,
                tmp_obs_ra,
                tmp_obs_dec,
                tmp_blank_1,
                tmp_mag_and_band,
                tmp_blank_2,
                tmp_observatory_code,
            ]
        )
    # Construct the Astropy Table.
    table = ap_table.Table(rows=table_rows, names=column_names)
    return table


def minor_planet_table_to_record(table: hint.Table) -> list[str]:
    """This converts an 80 column record for minor planets to a table
    representing the same data.

    This function provides a minimal amount of verification that the input
    table is correct. If the provided entry of the table is too long, the text
    is striped of whitespace and then ususally cut.

    The documentation for how the columns are assigned is provided by the
    Minor Planet Center:
    https://www.minorplanetcenter.net/iau/info/OpticalObs.html

    Parameters
    ----------
    table : Astropy Table
        A table containing the same information that can be written as the
        standard 80-column record.

    Returns
    -------
    records : list
        The records in MPC format. Each entry is 80 characters long and are in
        the standard format. The entries are derived from the provided table
        with information cut to fit into the format.
    """
    # Check that the table has the required column headers. Although the order
    # is not required to be the same, ensuring the same order ensures the
    # blank table was used as a template.
    column_names = MPC_MINOR_PLANET_TABLE_COLUMN_NAMES
    if table.colnames != column_names:
        raise error.InputError(
            "The headers of the table do not match the expected column names. This"
            " function only can handle tables with the expected names."
        )
    # An inner function to convert a table row to a record 80-col string.
    # It is easier to understand this way despite the performance hit.
    def _row_to_record(row: hint.Row) -> str:
        # Obtain each of the parameters and employ the needed constraints upon
        # them so that they match the 80-column standard format.
        # The minor planet number.
        in_pack_mpc_num = str(row["packed_mpc_number"])
        str_packed_mpc_number = in_pack_mpc_num.strip()[-5:].rjust(5)
        # The packed provisional designation.
        in_pack_prov_desig = str(row["packed_provisional_number"])
        str_packed_provisional_number = in_pack_prov_desig.strip()[-7:].rjust(7)
        # The discovery asterisk.
        in_discov_aster = str(row["discovery_asterisk"])
        str_discovery_asterisk = "*" if in_discov_aster == "*" else " "
        # The publishable note.
        in_publish_note = str(row["publishable_note"])
        str_publish_note = in_publish_note.strip()[-1:].rjust(1)
        # The observational note.
        in_obs_note = str(row["observing_note"])
        str_observing_note = in_obs_note.strip()[-1:].rjust(1)
        # The date of observation.
        in_obs_date = str(row["date"])
        str_date = in_obs_date.strip()[:17].ljust(17)
        # The right ascension.
        in_ra = str(row["ra"])
        str_ra = in_ra.strip()[:12].ljust(12)
        # The declination.
        in_dec = str(row["dec"])
        str_dec = in_dec.strip()[:12].ljust(12)
        # Space which is defined to be blank by the specification.
        in_blank = str(row["blank"])
        str_blank = in_blank.strip()[-9:].rjust(9)
        # The magnitude and its accompanying band.
        in_mag_band = str(row["magnitude_and_band"])
        band_char = in_mag_band[-1]
        mag_str = in_mag_band.strip()[-6:-1].ljust(5)
        str_magnitude_and_band = mag_str + band_char
        # The pseudo blank area, which is defined to be blank but is often not
        # for some reason.
        in_psu_blank = str(row["pseudo_blank"])
        str_pseudo_blank = in_psu_blank.strip()[-6:].rjust(6)
        # The observetory code.
        in_obs_code = str(row["observatory_code"])
        str_observatory_code = in_obs_code.strip()[-3:].rjust(3)
        # Done.
        # From the length controlled strings, the record which encodes the
        # information about this row can be derived.
        record = (
            str_packed_mpc_number
            + str_packed_provisional_number
            + str_discovery_asterisk
            + str_publish_note
            + str_observing_note
            + str_date
            + str_ra
            + str_dec
            + str_blank
            + str_magnitude_and_band
            + str_pseudo_blank
            + str_observatory_code
        )
        # Ensure that the record is exactly 80 columns long.
        if len(record) != 80:
            raise error.DevelopmentError(
                "The row derived record string is not 80 columns. The current record"
                " string: `{rec}`.".format(rec=record)
            )
        else:
            # The record is assumed to be good.
            return record
        # The code should not reach here.
        raise error.LogicFlowError
        return None

    # Creating the records via the table.
    records = []
    for rowdex in table:
        # The length of the records are checked in the subfunction.
        temp_record = _row_to_record(row=rowdex)
        records.append(temp_record)
    # All done.
    return records
