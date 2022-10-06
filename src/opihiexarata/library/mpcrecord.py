import astropy as ap
import astropy.coordinates as ap_coordinates
import astropy.table as ap_table
import astropy.units as ap_units

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

__MPC_TABLE_NAME_TYPE_PAIR = {
    "minor_planet_number": str,
    "provisional_number": str,
    "discovery": bool,
    "publishable_note": str,
    "observing_note": str,
    "year": int,
    "month": int,
    "day": float,
    "ra": float,
    "dec": float,
    "blank_1": str,
    "magnitude": float,
    "bandpass": str,
    "blank_2": str,
    "observatory_code": str,
}
MPC_MINOR_PLANET_TABLE_COLUMN_NAMES = list(__MPC_TABLE_NAME_TYPE_PAIR.keys())
MPC_MINOR_PLANET_TABLE_COLUMN_TYPES = list(__MPC_TABLE_NAME_TYPE_PAIR.values())


def blank_minor_planet_table() -> hint.Table:
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
    data_types = MPC_MINOR_PLANET_TABLE_COLUMN_TYPES
    blank_table = ap_table.Table(names=column_names, dtype=data_types)
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
    # A reusable function to extract the data from the a record to a list of
    # parameters.
    def _record_to_row_dictionary(line_string: str) -> dict:
        """Creating a table row from the data found in a record."""
        # Raw values from the record.
        raw_minor_planet_number = line_string[0:5]
        raw_provincial_designation = line_string[5:12]
        raw_discovery_asterisk = line_string[12]
        raw_publishable_note = line_string[13]
        raw_observing_note = line_string[14]
        raw_obs_date = line_string[15:32]
        raw_obs_ra = line_string[32:44]
        raw_obs_dec = line_string[44:56]
        raw_blank_1 = line_string[56:65]
        raw_mag_and_band = line_string[65:71]
        raw_blank_2 = line_string[71:77]
        raw_observatory_code = line_string[77:80]
        # Convert these raw extracted values into more typical and standard values
        # which is more prosessable. They are done as follows.
        # The minor planet number.
        minor_planet_number = raw_minor_planet_number
        # The provincial designation of the asteroid.
        provincial_designation = raw_provincial_designation
        # The discovery asterisk can be converted to a boolean.
        discovery = True if raw_discovery_asterisk == "*" else False
        # Publishing note flag.
        publishable_note = str(raw_publishable_note)
        # Observeing note flag.
        observing_note = str(raw_observing_note)
        # The observation date can be split.
        year, month, day = raw_obs_date.split()
        year = int(year)
        month = int(month)
        day = float(day)
        # Converting the RA to DEC to decimal degrees, leveraging Astropy.
        skycoord = ap_coordinates.SkyCoord(
            raw_obs_ra,
            raw_obs_dec,
            frame="icrs",
            unit=(ap_units.hourangle, ap_units.deg),
        )
        ra = skycoord.ra.value
        dec = skycoord.dec.value
        # First blank reservation. This is supposed to be reserved blank space.
        # But, it seems some people use it for whatever. Keeping it to string.
        blank_1 = str(raw_blank_1)
        # The magnitude and the bandpass can be split.
        mag_str = str(raw_mag_and_band[:-1]).strip()
        magnitude = float(mag_str) if len(mag_str) != 0 else float("nan")
        bandpass = str(raw_mag_and_band[-1])
        # Second blank reservation. This is supposed to be reserved blank space.
        # But, it seems some people use it for whatever. Keeping it to string.
        blank_2 = str(raw_blank_2)
        # Observatory code, it is not always a number and can have letters in it.
        observatory_code = str(raw_observatory_code)

        # Constructing a dictionary representing the row which can then be used to
        # add it to the table. The entries must be in order. We use the
        # constant column names.
        ordered_entries = [
            minor_planet_number,
            provincial_designation,
            discovery,
            publishable_note,
            observing_note,
            year,
            month,
            day,
            ra,
            dec,
            blank_1,
            magnitude,
            bandpass,
            blank_2,
            observatory_code,
        ]
        record_dict = dict(zip(MPC_MINOR_PLANET_TABLE_COLUMN_NAMES, ordered_entries))
        return record_dict

    # It is easier to make the Table from a list of rows representative
    # objects.
    table_rows_list = []
    # Going through each of the rows to extract the information into their
    # string representations.
    for linedex in records:
        # Extract the information
        try:
            temp_record_dict = _record_to_row_dictionary(line_string=linedex)
        except Exception:
            # For some reason, some of the lines in an 80-column MPC entry do
            # not seem to obey the format as understood by Sparrow.
            # TODO.
            continue
        # Add it to the records.
        table_rows_list.append(temp_record_dict)

    # Construct the Astropy Table. If nothing was provided, still provide a
    # blank table as there are still keyword expectations.
    table = ap_table.Table(rows=table_rows_list)
    table = table if len(table) != 0 else blank_minor_planet_table()
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
    def _record_to_row_string(row: hint.Row) -> str:
        # Every thing needs to be a string. This is a wrapper function which
        # helps with the spacing and column widths.
        def _construct_string(entry: str, exact_length: int, justify: str) -> str:
            """A unified function to create a string for the entry provided.
            This function handles justification and string clipping for too
            long strings. Provided the entry, the maximum length allowed by
            the 80-column specification, and how the string ought to be
            justified.
            """
            entry_str = str(entry)[:exact_length]
            # Determine justification.
            justify = justify.casefold()
            if justify == "left":
                justified_entry_str = entry_str.ljust(exact_length, " ")
            elif justify == "right":
                justified_entry_str = entry_str.rjust(exact_length, " ")
            else:
                raise error.DevelopmentError(
                    "The justification option provided is not supported."
                )
            # All done.
            assert len(justified_entry_str) == exact_length
            return justified_entry_str

        # Obtain each of the parameters and employ the needed constraints upon
        # them so that they match the 80-column standard format.
        # The minor planet number.
        raw_minor_planet_number = str(row["minor_planet_number"])
        str_minor_planet_number = _construct_string(
            entry=raw_minor_planet_number, exact_length=5, justify="left"
        )
        # The provisional designation.
        raw_provisional_number = str(row["provisional_number"])
        str_provisional_number = _construct_string(
            entry=raw_provisional_number, exact_length=7, justify="left"
        )
        # The discovery asterisk flag.
        raw_discovery = bool(row["discovery"])
        str_discovery = "*" if raw_discovery else " "
        # The publishing note.
        raw_publishable_note = str(row["publishable_note"])
        str_publishable_note = _construct_string(
            entry=raw_publishable_note, exact_length=1, justify="right"
        )
        # The observational note.
        raw_observing_note = str(row["observing_note"])
        str_observing_note = _construct_string(
            entry=raw_observing_note, exact_length=1, justify="right"
        )
        # The date of observation. The month and days need leading zeros if
        # it is not a double digit date.
        raw_year = str(row["year"])
        raw_month = "0" + str(row["month"]) if row["month"] < 10 else str(row["month"])
        raw_day = "0" + str(row["day"]) if row["day"] < 10 else str(row["day"])
        raw_observing_date = " ".join([raw_year, raw_month, raw_day])
        str_observing_date = _construct_string(
            entry=raw_observing_date, exact_length=17, justify="left"
        )
        # The right ascension and declination.
        skycoord = ap_coordinates.SkyCoord(
            float(row["ra"]), float(row["dec"]), frame="icrs", unit="deg"
        )
        raw_str_ra = skycoord.ra.to_string(
            ap_units.hour, sep=":", pad=True, precision=None
        )
        raw_str_dec = skycoord.dec.to_string(
            ap_units.deg, sep=":", pad=True, precision=None, alwayssign=True
        )
        # MPC record uses spaces as seperator.
        raw_str_ra = raw_str_ra.replace(":", " ")
        raw_str_dec = raw_str_dec.replace(":", " ")
        str_ra = _construct_string(entry=raw_str_ra, exact_length=12, justify="left")
        str_dec = _construct_string(entry=raw_str_dec, exact_length=12, justify="left")
        # Space which is defined to be blank by the specification.
        raw_blank_1 = str(row["blank_1"])
        str_blank_1 = _construct_string(
            entry=raw_blank_1, exact_length=9, justify="left"
        )
        # The magnitude; this way we can handle both blank strings and numbers.
        raw_magnitude = str(row["magnitude"]).strip()
        if len(raw_magnitude) == 0 or raw_magnitude.casefold() == "nan":
            # There is no magnitude data so just have it blank.
            raw_mag_synth = "     "
        else:
            # Magnitude value string must be centered on the decimal point.
            raw_mag_whole, raw_mag_frac = raw_magnitude.split(".")
            raw_mag_whole = _construct_string(
                entry=raw_mag_whole, exact_length=2, justify="right"
            )
            raw_mag_frac = _construct_string(
                entry=raw_mag_frac, exact_length=2, justify="left"
            )
            raw_mag_synth = raw_mag_whole + "." + raw_mag_frac
        str_magnitude = _construct_string(
            entry=raw_mag_synth, exact_length=5, justify="left"
        )
        # The bandpass.
        raw_bandpass = str(row["bandpass"]).strip()
        str_bandpass = _construct_string(
            entry=raw_bandpass, exact_length=1, justify="left"
        )
        # The pseudo blank area, which is defined to be blank but is often not
        # for some reason.
        raw_blank_2 = str(row["blank_2"])
        str_blank_2 = _construct_string(
            entry=raw_blank_2, exact_length=6, justify="left"
        )
        # The observetory code.
        raw_observatory_code = str(row["observatory_code"])
        str_observatory_code = _construct_string(
            entry=raw_observatory_code, exact_length=3, justify="left"
        )
        # Done.
        # From the length controlled strings, the record which encodes the
        # information about this row can be derived.
        record = (
            str_minor_planet_number
            + str_provisional_number
            + str_discovery
            + str_publishable_note
            + str_observing_note
            + str_observing_date
            + str_ra
            + str_dec
            + str_blank_1
            + str_magnitude
            + str_bandpass
            + str_blank_2
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
        temp_record = _record_to_row_string(row=rowdex)
        records.append(temp_record)
    # All done.
    return records


def clean_minor_planet_record(records:list[str]) -> list[str]:
    """This function cleans up an input MPC record. 
    
    It...

    - Removes duplicate entries
    - Entries not 80-characters long.
    - Sorts based off of observation time.

    Parameters
    ----------
    records : list
        The records to be sorted and cleaned up.

    Returns
    -------
    clean_records : list 
        The records after they have been cleaned.
    """
    # First, we remove any duplicate entries.
    cleaner_records = list(set(records))

    # If any of the entries are not long enough, they are also discarded.
    cleaner_records = [recorddex for recorddex in cleaner_records if len(recorddex) == 80]

    # It is a lot easier to sort using Astropy tables as the dates are in the 
    # middle of the entries.
    cleaner_table = minor_planet_record_to_table(records=cleaner_records)
    cleaner_table.sort(["year", "month", "day"])
    # Returning the sorted table back to a record.
    cleaner_records = minor_planet_table_to_record(table=cleaner_table)

    # All of the cleaning has finished.
    return cleaner_records