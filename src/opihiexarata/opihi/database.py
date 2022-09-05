"""The database solution for storing and recording zero point data. 
We use a flat file database here with ordered directories to make it easily 
transversal by other tools and to have it be simple. A single instance of 
this class should monitor its own database."""

import os
import datetime
import glob
import astropy.table as ap_table
import plotly.express as px

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

DATABASE_CHECK_FILE_BASENAME = "exarata_zero_point_database"
DATABASE_CHECK_FILE_EXTENSION = "check"


class OpihiZeroPointDatabaseSolution(library.engine.ExarataSolution):
    """The flat file database solution which provides an API-like solution to
    interacting with a flat-file database with nested folders for all of the
    zero point entries.

    Attributes
    ----------
    database_directory : string
        The path to the directory where the flat file database is.
    """

    def __init__(self, database_directory: str) -> None:
        """Creating the instance of the database for which we will use to
        manage the directory.

        We check if the directory provided is a valid directory by checking for
        the existence of a file that indicates so. If the directory is
        blank, we assume a new database is to be created and so we add the
        file ourselves.

        Parameters
        ----------
        database_directory : string
            The path to the directory where the flat file database is. A database
            check file exists to ensure that it is a directory which follows
            the conventions of this class.

        Returns
        -------
        None
        """
        # If the directory does not exist, we assume that we can make it.
        # The file checking step will prepare a blank directory.
        if not os.path.isdir(database_directory):
            absolute_database_directory = os.path.abspath(database_directory)
            os.makedirs(absolute_database_directory)

        # We check if the database follows the expected design assumptions by
        # checking if the check file is there. If it is not, then we may need
        # format the database ourselves.
        check_filename = library.path.merge_pathname(
            directory=database_directory,
            filename=DATABASE_CHECK_FILE_BASENAME,
            extension=DATABASE_CHECK_FILE_EXTENSION,
        )
        if os.path.isfile(check_filename):
            pass
        else:
            # If the directory is empty, we assume to start a new database.
            if len(os.listdir(database_directory)) == 0:
                # Creating the check file.
                with open(check_filename, "w") as __:
                    pass
                # We can still continue with the database
            else:
                raise error.DirectoryError(
                    "The directory provided {dir} is not a directory which is detected"
                    " to be a proper database directory for zero point recording;"
                    " neither is it an empty directory to start a new database.".format(
                        dir=database_directory
                    )
                )
        # Keeping the record.
        self.database_directory = os.path.abspath(database_directory)

        # All done.
        return None

    @classmethod
    def clean_record_text_file(
        cls, filename: str, garbage_filename: str = None
    ) -> None:
        """This function takes a record file and cleans it up. Sorting it by
        time and deleting any lines which do not conform to the expected
        formatting.

        This is a class method because cleaning the database files does not
        rely on the database per-say or adding data to it. It could be
        performed by a third-party script without issue. It can also be
        dangerous to clean a database so we detach ourselves from the
        database we are managing just in case.

        Parameters
        ----------
        filename : str
            The text record filename which will have its entries cleaned up.
        garbage_filename : str, default = None
            A path to a text file where all of the garbage lines detected by
            this cleaning routine should be saved to instead of being deleted
            as default.

        Returns
        -------
        None
        """
        # We need to read every line.
        with open(filename, "r") as file:
            record_lines = file.readlines()
        # The extra new line characters get in the way of cleaning and we
        # will add them back later.
        record_lines = [linedex.removesuffix("\n") for linedex in record_lines]

        # We check if the record is the correct line length, if not, return
        # False.
        RECORD_LINE_LENGTH = 60

        def __record_check_line_length(record: str) -> bool:
            """Checking that the line record is the correct length."""
            return len(record) == RECORD_LINE_LENGTH

        # We go through every line, checking for many things which would make
        # it a bad line. The checking functions have been written above.
        valid_records = []
        garbage_records = []
        for linedex in record_lines:
            # Each of these if statements check one aspect of the lines to
            # ensure only valid records are passed through.
            if not __record_check_line_length(record=linedex):
                # The record is the wrong length and thus it is bad.
                garbage_records.append(linedex)
            else:
                valid_records.append(linedex)

        # We sort the valid records via time. Conveniently, ISO formatted
        # times makes this equivalent to sorting strings.
        sorted_records = sorted(valid_records)

        # There is no other cleaning that is needed.
        cleaned_records = sorted_records

        # The records are cleaned and thus we can save them back to their
        # original file, overwriting everything else. We need to add the
        # newline characters as well.
        cleaned_records = [linedex + "\n" for linedex in cleaned_records]
        with open(filename, "w") as file:
            file.writelines(cleaned_records)

        # If a bad record outfile was provided, we also save that as well.
        if garbage_filename is not None:
            # Still need the new lines.
            garbage_records = [linedex + "\n" for linedex in garbage_records]
            with open(garbage_filename, "a") as garbage_file:
                garbage_file.writelines(garbage_records)

        # All done.
        return None

    @classmethod
    def clean_database_text_files(
        cls, database_directory: str, garbage_filename: str = None
    ) -> None:
        """This function cleans each and every file inside of the the database
        provided by the inputted database directory.

        This is a class method because cleaning the database files does not
        rely on the database per-say or adding data to it. It could be
        performed by a third-party script without issue. It can also be
        dangerous to clean a database so we detach ourselves from the
        database we are managing just in case.

        Parameters
        ----------
        database_directory : str
            We clean all database files within the directory provided.
        garbage_filename : str, default = None
            A path to a text file where all of the garbage lines detected by
            this cleaning routine should be saved to instead of being deleted
            as default.

        Returns
        -------
        None
        """
        # We need to make sure that the directory itself exists and it is a
        # database directory.
        check_filename = library.path.merge_pathname(
            directory=database_directory,
            filename=DATABASE_CHECK_FILE_BASENAME,
            extension=DATABASE_CHECK_FILE_EXTENSION,
        )
        if not os.path.isfile(check_filename):
            raise error.DirectoryError(
                "The directory {dir} provided is not a valid OpihiExarata zero point"
                " database directory as it is missing the check file. We will not"
                " attempt to clean it.".format(dir=database_directory)
            )

        # We search through all of the database files. We do not try and
        # clean non-database files.
        database_glob_search = library.path.merge_pathname(
            directory=database_directory, filename="*.zp_ox", extension="txt"
        )
        database_files = glob.glob(database_glob_search)
        # Clean every file.
        for filedex in database_files:
            cls.clean_record_text_file(
                filename=filedex, garbage_filename=garbage_filename
            )
        # All done.
        return None

    @classmethod
    def drop_database_text_files(cls, database_directory: str) -> None:
        """This function deletes all zero point record files within a given
        database. We use "drop" per database parlance.

        This is a class method because deleting the database files does not
        rely on the database per-say or adding data to it. It could be
        performed by a third-party script without issue. It can also be
        dangerous to clean a database so we detach ourselves from the
        database we are managing just in case.

        Parameters
        ----------
        database_directory : str
            We delete all database files within the directory provided.

        Returns
        -------
        None
        """
        # We need to make sure that the directory itself exists and it is a
        # database directory.
        check_filename = library.path.merge_pathname(
            directory=database_directory,
            filename=DATABASE_CHECK_FILE_BASENAME,
            extension=DATABASE_CHECK_FILE_EXTENSION,
        )
        if not os.path.isfile(check_filename):
            raise error.DirectoryError(
                "The directory {dir} provided is not a valid OpihiExarata zero point"
                " database directory. There is nothing to delete.".format(
                    dir=database_directory
                )
            )
        else:
            # We remove the check file as this directory will no longer
            # be a database.
            os.remove(check_filename)

        # We search through all of the database files. We do not delete
        # non-database files.
        database_glob_search = library.path.merge_pathname(
            directory=database_directory, filename="*.zp_ox", extension="txt"
        )
        database_files = glob.glob(database_glob_search)
        # Removing the files.
        for filedex in database_files:
            os.remove(filedex)

        # If the directory is empty, we can remove it as well.
        if len(os.listdir(database_directory)) == 0:
            os.removedirs(database_directory)

        # All done.
        return None

    def _generate_text_record_filename(self, year: int, month: int, day: int) -> str:
        """The text records which stores all of the information of the
        zero points are created in a specific way to allow for the user to
        manually navigate it with ease.

        Parameters
        ----------
        year : int
            The year of the data for this record.
        month : int
            The month of the data for this record.
        day : int
            The day of the data for this record.

        Returns
        -------
        text_record_filename : string
            The filename where the record should go in.
        """
        # The filename is really just the date.
        date = datetime.date(year=year, month=month, day=day)
        basename = "{isodate}.zp_ox".format(isodate=date.isoformat())
        # Combining it with directory and the expected text file extension.
        text_record_filename = library.path.merge_pathname(
            directory=self.database_directory, filename=basename, extension="txt"
        )
        # All done.
        return text_record_filename

    def _generate_zero_point_record_line(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        zero_point: float,
        zero_point_error: float,
        filter_name: str,
    ) -> str:
        """This function creates the string representation of a zero point
        record.

        Parameters
        ----------
        year : int
            The year of the time of this zero point measurement.
        month : int
            The month of the time of this zero point measurement.
        day : int
            The day of the time of this zero point measurement.
        hour : int
            The hour of the time of this zero point measurement.
        minute : int
            The minute of the time of this zero point measurement.
        second : int
            The second of the time of this zero point measurement.
        zero_point : float
            The zero point measurement value
        zero_point_error : float
            The error of the zero point measurement value.
        filter_name : string
            The name of the filter that this zero point corresponds to.

        Returns
        -------
        zero_point_record : string
            The string representation of the zero point record.
        """
        # We check that the data provided is a proper date. The smallest
        # precision is a second so anything lower than that we do not need.
        second = int(second)
        try:
            record_datetime = datetime.datetime(
                year=year, month=month, day=day, hour=hour, minute=minute, second=second
            )
        except ValueError:
            raise error.InputError(
                "The time and date values provided cannot be composed to a real life"
                " date and time. Input is: {yr}-{mn}-{dy}  {hr}:{mi}:{sc}.".format(
                    yr=year, mn=month, dy=day, hr=hour, mi=minute, sc=second
                )
            )
        else:
            datetime_string = record_datetime.isoformat(timespec="seconds")

        # We compose the zero point string, both the value and the error.
        ASCII_PLUS_MINUS_SYMBOL = "+/-"
        ZERO_POINT_DIGIT_LENGTH = 12
        zero_point_string = "{zp:{ln}.{zp_f}f}  {pm}  {zpe:{ln}.{zpe_f}f}".format(
            zp=zero_point,
            zpe=zero_point_error,
            pm=ASCII_PLUS_MINUS_SYMBOL,
            ln=ZERO_POINT_DIGIT_LENGTH,
            zp_f=ZERO_POINT_DIGIT_LENGTH - 3 - 1,
            zpe_f=ZERO_POINT_DIGIT_LENGTH - 1 - 1,
        )

        # We compose the filter name string.
        filter_string = "{flt:>2}".format(flt=filter_name)

        # Combing it all together now.
        zero_point_record = "{time}    {zp_e}    {flt}".format(
            time=datetime_string, zp_e=zero_point_string, flt=filter_string
        )
        # All done.
        return zero_point_record

    def _parse_zero_point_record_line(self, record: str) -> dict:
        """This function parses the zero point record line to return a
        dictionary which is much more helpful in working with the data.

        Parameters
        ----------
        record : string
            The record line which will be converted to a dictionary.

        Returns
        -------
        record_dictionary : dictionary
            The record dictionary containing the information from the record
            line.
        """
        # We break up the record into its parts. We do not care about the
        # plus minus symbol.
        (
            datetime_str,
            zero_point_str,
            __,
            zero_point_error_str,
            filter_name_str,
        ) = record.split()

        # We use datetime to better format the ISO date time string.
        record_datetime = datetime.datetime.fromisoformat(datetime_str)

        # Converting to numbers.
        zero_point = float(zero_point_str)
        zero_point_error = float(zero_point_error_str)

        # We can compile the dictionary from here. We include the datatime for
        # ease of handling.
        record_dictionary = {
            "datetime": datetime_str,
            "year": record_datetime.year,
            "month": record_datetime.month,
            "day": record_datetime.day,
            "hour": record_datetime.hour,
            "minute": record_datetime.minute,
            "second": record_datetime.second,
            "zero_point": zero_point,
            "zero_point_error": zero_point_error,
            "filter_name": filter_name_str,
        }
        # All done
        return record_dictionary

    def write_zero_point_record(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        zero_point: float,
        zero_point_error: float,
        filter_name: str,
        clean_file: bool = False,
    ) -> str:
        """This function writes a zero point measurement to the database.

        Parameters
        ----------
        year : int
            The year of the time of this zero point measurement.
        month : int
            The month of the time of this zero point measurement.
        day : int
            The day of the time of this zero point measurement.
        hour : int
            The hour of the time of this zero point measurement.
        minute : int
            The minute of the time of this zero point measurement.
        second : int
            The second of the time of this zero point measurement.
        zero_point : float
            The zero point measurement value
        zero_point_error : float
            The error of the zero point measurement value.
        filter_name : string
            The name of the filter that this zero point corresponds to.
        clean_file : bool, default = False
            If True, along with appending the zero point record to the
            current file, we sort the file by time and clean up any bad
            entries.

        Returns
        -------
        None
        """
        # We need to compose the record from the information provided.
        zero_point_record = self._generate_zero_point_record_line(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            zero_point=zero_point,
            zero_point_error=zero_point_error,
            filter_name=filter_name,
        )

        # We need to derive the correct filename.
        record_filename = self._generate_text_record_filename(
            year=year, month=month, day=day
        )

        # We add our entry to the file, we add the newline here.
        with open(record_filename, "a", encoding="utf-8") as file:
            file.write(zero_point_record + "\n")

        # If the file is to be cleaned up.
        if clean_file:
            self.clean_record_text_file(filename=record_filename)

        # All done.
        return None

    def write_zero_point_record_julian_day(
        self,
        jd: float,
        zero_point: float,
        zero_point_error: float,
        filter_name: str,
        clean_file: bool = False,
    ) -> None:
        """This function writes a zero point measurement to the database.
        However, it is also a wrapper around the standard function to allow
        for inputting times as Julian days, the convention for the OpihiExarata
        software.

        Parameters
        ----------
        jd : float
            The time of the zero point measurement, in Julian days.
        zero_point : float
            The zero point of the measurement.
        zero_point_error : float
            The error of the zero point measurement.
        filter_name : float
            The name of the filter that the zero point measurement
            corresponds to.
        clean_file : bool, default = False
            If True, along with appending the zero point record to the
            current file, we sort the file by time and clean up any bad
            entries.

        Returns
        -------
        None
        """
        # We take the Julian day and convert it to the civil time so we can
        # use the other function.
        (
            year,
            month,
            day,
            hour,
            minute,
            second,
        ) = library.conversion.julian_day_to_full_date(jd=jd)
        # Seconds are minimally an integer. There is no reason to have a higher
        # amount of precision. But this function handles it for us anyways.
        self.write_zero_point_record(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            zero_point=zero_point,
            zero_point_error=zero_point_error,
            filter_name=filter_name,
            clean_file=clean_file,
        )
        # All done.
        return None

    def read_zero_point_record_list(self, filename: str) -> list[str]:
        """This reads a zero point record file and converts it to a list for
        each row is a a row in the record file itself.

        Parameters
        ----------
        filename : string
            The zero point record filename to be read.

        Returns
        -------
        record_list : Table
            The representation of all of the zero point data in a list.
        """
        # Check that the file is a zero point record file assuming the
        # extension.
        if filename[-10:] != ".zp_ox.txt":
            raise error.FileError(
                "The filename {f} is not detected to be an OpihiExarata zero point"
                " record file based on its extension.".format(f=filename)
            )
        elif not os.path.isfile(filename):
            raise error.FileError(
                "The filename {f} does not exist in the database and thus it cannot be"
                " read.".format(f=filename)
            )
        else:
            # We need to read the zero point record file.
            with open(filename, "r") as file:
                record_lines = file.readlines()
            # We do not need the new line characters.
            record_list = [linedex.removesuffix("\n") for linedex in record_lines]
        # All done.
        return record_list

    def read_zero_point_record_table(self, filename: str) -> hint.Table:
        """This reads a zero point record file and converts it into a nice
        table for easier reading and manipulation.

        Parameters
        ----------
        filename : string
            The zero point record filename to be read.

        Returns
        -------
        record_table : Table
            The representation of all of the zero point data in a table.
        """
        # Pulling all of the lines from the file.
        record_lines = self.read_zero_point_record_list(filename=filename)

        # We use Astropy data tables as we already have them as a requirement.
        # Constructing the rows.
        record_dict_rows = [
            self._parse_zero_point_record_line(record=linedex)
            for linedex in record_lines
        ]
        # Creating the table.
        record_table = ap_table.Table(rows=record_dict_rows)
        # All done.
        return record_table

    def read_zero_point_record_database(self) -> hint.Table:
        """This function reads all record files in the database that the
        instance is managing. Depending on the amount of data, this can be
        a little slow and take up a lot of memory, but it should be fine.

        Parameters
        ----------
        None

        Returns
        -------
        database_table : Table
            A table of all of the zero point data from files contained within
            the database.
        """
        # We need to grab all of the zero point files in the database.
        database_glob_search = library.path.merge_pathname(
            directory=self.database_directory, filename="*.zp_ox", extension="txt"
        )
        database_files = glob.glob(database_glob_search)

        # Reading every single file. We are basically combining all of the
        # files to a single object.
        database_lines = []
        for filedex in database_files:
            database_lines += self.read_zero_point_record_list(filename=filedex)

        # We parse every single line so that we can arrange it as a table.
        database_dict_rows = [
            self._parse_zero_point_record_line(record=linedex)
            for linedex in database_lines
        ]
        # We use Astropy data tables as we already have them as a requirement.
        database_table = ap_table.Table(rows=database_dict_rows)
        # All done.
        return database_table

    def query_database_between_datetimes(
        self,
        begin_year: int,
        begin_month: int,
        begin_day: int,
        begin_hour: int,
        begin_minute: int,
        begin_second: int,
        end_year: int,
        end_month: int,
        end_day: int,
        end_hour: int,
        end_minute: int,
        end_second: int,
    ) -> hint.Table:
        """This queries the database and returns a table with all entries in
        the database in between two given dates and times.

        Parameters
        ----------
        begin_year : int
            Begin querying from this year of the date.
        begin_month : int
            Begin querying from this month of the date.
        begin_day : int
            Begin querying from this day of the date.
        begin_hour : int
            Begin querying from this hour of the date.
        begin_minute : int
            Begin querying from this minute of the date.
        begin_second : int
            Begin querying from this second of the date.
        end_year : int
            End querying from this year of the date.
        end_month : int
            End querying from this month of the date.
        end_day : int
            End querying from this day of the date.
        end_hour : int
            End querying from this hour of the date.
        end_minute : int
            End querying from this minute of the date.
        end_second : int
            End querying from this second of the date.

        Returns
        -------
        query_record_table : Table
            A table containing the data as queried from the database.
        """
        # Datetimes are the best way to handle this.
        begin_datetime = datetime.datetime(
            year=begin_year,
            month=begin_month,
            day=begin_day,
            hour=begin_hour,
            minute=begin_minute,
            second=int(begin_second),
        )
        end_datetime = datetime.datetime(
            year=end_year,
            month=end_month,
            day=end_day,
            hour=end_hour,
            minute=end_minute,
            second=int(end_second),
        )

        # Something to store all of the record lines in.
        database_record_list = []
        # We loop over all relevant dates to extract all relevant files for
        # the query. This allows us to sort for only those days relevant and
        # saves us time.
        def datetime_range(start_dt, end_dt):
            """A generator for iterating between datetimes. We include the 
            end point."""
            for incrementdex in range(int((end_dt - start_dt).days) + 1):
                yield start_dt + datetime.timedelta(days=incrementdex)

        # Search for any other days, other than the beginning day, that we 
        # need to pull data from.
        for datedex in datetime_range(start_dt=begin_datetime, end_dt=end_datetime):
            # Getting the database file name for this date.
            database_filename = self._generate_text_record_filename(
                year=datedex.year, month=datedex.month, day=datedex.day
            )
            # Attempt to read the file.
            try:
                database_record_list += self.read_zero_point_record_list(
                    filename=database_filename
                )
            except error.FileError:
                # The file likely does not exist so there is nothing to read.
                continue

        # Fine tune the search for hours, minutes and seconds. Datetimes
        # handle the entire date so we can also double check for that.
        valid_record_rows = []
        for recorddex in database_record_list:
            record_dictionary = self._parse_zero_point_record_line(record=recorddex)
            record_datetime = datetime.datetime(
                year=record_dictionary["year"],
                month=record_dictionary["month"],
                day=record_dictionary["day"],
                hour=record_dictionary["hour"],
                minute=record_dictionary["minute"],
                second=record_dictionary["second"],
            )
            # We see if this record is within the date range and thus valid.
            if begin_datetime <= record_datetime <= end_datetime:
                # A valid time for the query.
                valid_record_rows.append(record_dictionary)
            else:
                # Not valid.
                continue

        # We parse all of these valid entries into a table.
        query_record_table = ap_table.Table(rows=valid_record_rows)
        # All done.
        return query_record_table

    def query_database_between_julian_days(
        self, begin_jd: float, end_jd: float
    ) -> hint.Table:
        """This queries the database and returns a table with all entries in
        the database in between two given dates and times. The date and times
        are given in Julian days as per convention. This is a wrapper around
        the original implementation to account for the needed conversion.

        Parameters
        ----------
        begin_jd : float
            The Julian day after which, in time, records from the database
            should be returned.
        end_jd : float
            The Julian day before which, in time, records from the database
            should be returned.

        Returns
        -------
        query_record_table : Table
            A table containing the data as queried from the database.
        """
        # We need to convert the Julian days to the default full time date
        # representation.
        b_yr, b_mn, b_dy, b_hr, b_mi, b_sc = library.conversion.julian_day_to_full_date(
            jd=begin_jd
        )
        e_yr, e_mn, e_dy, e_hr, e_mi, e_sc = library.conversion.julian_day_to_full_date(
            jd=end_jd
        )
        # Sending it to the original query function.
        query_record_table = self.query_database_between_datetimes(
            begin_year=b_yr,
            begin_month=b_mn,
            begin_day=b_dy,
            begin_hour=b_hr,
            begin_minute=b_mi,
            begin_second=b_sc,
            end_year=e_yr,
            end_month=e_mn,
            end_day=e_dy,
            end_hour=e_hr,
            end_minute=e_mi,
            end_second=e_sc,
        )
        # All done.
        return query_record_table

    def create_plotly_monitoring_html_plot(
        self,
        html_filename: str,
        plot_query_begin_jd: float,
        plot_query_end_jd: float,
        plot_lower_zero_point:float = None,
        plot_upper_zero_point:float = None,
        include_plotlyjs: str = True,
    ) -> None:
        """This function creates the monitoring plot for the monitoring
        service webpage. It plots data from the zero point database depending
        on the range of times desires.

        Parameters
        ----------
        html_filename : string
            The filename where the html file will be saved to.
        plot_query_begin_jd : float
            The starting time from which the database should be queried until
            for plotting. This is in Julian days as per convention.
        plot_query_end_jd : float
            The starting time from which the database should be queried until
            for plotting. This is in Julian days as per convention.
        plot_lower_zero_point : float, default = None
            This sets the lower limit of the zero point plot. If it and the 
            upper limit is not set, we default to Plotly's best judgement.
        plot_upper_zero_point : float, default = None
            This sets the upper limit of the zero point plot. If it and the 
            lower limit is not set, we default to Plotly's best judgement.
        include_plotlyjs : string, default = True
            The setting for how the plotly javascript file will be included.
            Consult the plotly documentation for available options.

        Returns
        -------
        None
        """
        # We need to fetch the data to query. We query just a little outside
        # of the range provided so that the plots are continuous and connect
        # to points outside of the range. A day is more than enough.
        zero_point_record_table = self.query_database_between_julian_days(
            begin_jd=plot_query_begin_jd - 1, end_jd=plot_query_end_jd + 1
        )

        # We group similar filters into lines.
        symbol_group_table_key = "filter_name"

        # The color of the lines are based on the filter being observed. We
        # supply a color map so that it derives the colors from the filter
        # names themselves.
        symbol_color_table_key = "filter_name"
        plot_color_map = {
            "c": library.config.MONITOR_PLOT_FILTER_C_LINE_COLOR,
            "g": library.config.MONITOR_PLOT_FILTER_G_LINE_COLOR,
            "r": library.config.MONITOR_PLOT_FILTER_R_LINE_COLOR,
            "i": library.config.MONITOR_PLOT_FILTER_I_LINE_COLOR,
            "z": library.config.MONITOR_PLOT_FILTER_Z_LINE_COLOR,
            "1": library.config.MONITOR_PLOT_FILTER_1_LINE_COLOR,
            "2": library.config.MONITOR_PLOT_FILTER_2_LINE_COLOR,
            "b": library.config.MONITOR_PLOT_FILTER_B_LINE_COLOR,
        }

        # We define the order the filters are plotted just by the verbal
        # order of their name. Done as per `category_orders` documentation.
        symbol_order_specification = {
            "filter_name": ["c", "g", "r", "i", "z", "1", "2", "b"]
        }

        # The symbol for plotting. Large markers are not needed and the
        # error bars already provide some marker. As we all use the same
        # symbol, we do not really need to use an array.
        #marker = None

        # We provide additional context for custom data that should be
        # available to the plotting resources.
        custom_data_headers = []

        # The table records for the data and errors.
        line_x_table_key = "datetime"
        line_y_table_key = "zero_point"
        line_y_error_table_key = "zero_point_error"

        # We make the plot here. Further visual and aesthetic formatting is
        # done below.
        fig = px.scatter(
            zero_point_record_table.to_pandas(),
            x=line_x_table_key,
            y=line_y_table_key,
            error_y=line_y_error_table_key,
            symbol=symbol_group_table_key,
            color=symbol_color_table_key,
            color_discrete_map=plot_color_map,
            custom_data=custom_data_headers,
            category_orders=symbol_order_specification,
        )

        # The overall title of the figure. It is helpful to put the UTC time
        # of when the figure was made. We are using a more human readable
        # version of ISO 8601 time formatting.
        iso_8601_time_format = R"%Y-%m-%d %H:%M:%S"
        # Datetime only takes seconds as an integer.
        int_only = lambda array: [int(valuedex) for valuedex in array]
        utc_now_tuple = library.conversion.julian_day_to_full_date(
            jd=library.conversion.current_utc_to_julian_day()
        )
        utc_now_datetime = datetime.datetime(*int_only(utc_now_tuple))
        utc_time_string = utc_now_datetime.strftime(iso_8601_time_format)
        fig.update_layout(
            title_text="Opihi Zero Point Trends (Now: {now} UTC)".format(
                now=utc_time_string
            )
        )
        # All datetimes should have the same formatting. We rotate it so it
        # is a little more readable.
        tick_rotation = 15
        fig.update_xaxes(tickformat=iso_8601_time_format, tickangle=tick_rotation)

        # We configure the message when hovering to be a little bit more clear.
        hover_message_template = R"%{x}<br>     %{y}"
        fig.update_traces(hovertemplate=hover_message_template)

        # A unified x-axis label is a little bit more clear to understand
        # and locate because of all of the different filters (lines) which
        # are plotted.
        fig.update_layout(hovermode="x unified")
        # We also fix the x-axis and y-axis and legend title.
        fig.update_layout(
            xaxis_title="Time", yaxis_title="Zero Point", legend_title_text="Filter"
        )

        # We only want to plot between the provided time range. We queried
        # outside of that range so that we could be continuous for our plot
        # lines.
        begin_datetime_tuple = library.conversion.julian_day_to_full_date(
            jd=plot_query_begin_jd
        )
        end_datetime_tuple = library.conversion.julian_day_to_full_date(
            jd=plot_query_end_jd
        )
        # We use integer seconds only for the datetimes, the best way to do
        # this is to just trim off the decimal seconds.
        datetime_lower_limit = datetime.datetime(*int_only(begin_datetime_tuple))
        datetime_upper_limit = datetime.datetime(*int_only(end_datetime_tuple))
        fig.update_layout(xaxis_range=[datetime_lower_limit, datetime_upper_limit])

        # The upper and lower zero point plot limits.
        if plot_lower_zero_point is not None and plot_upper_zero_point is not None:
            fig.update_layout(yaxis_range=[plot_lower_zero_point, plot_upper_zero_point])
        else:
            # Use Plotly's interpretation, however, with inverted axes.
            # per the magnitude system.
            fig.update_yaxes(autorange="reversed")

        # The configuration file specifies how to handle the inclusion of the
        # Plotly javascript file.
        fig.write_html(html_filename, include_plotlyjs=include_plotlyjs)
        # All done.
        return None

    def create_plotly_monitoring_html_plot_via_configuration(self) -> None:
        """This is a wrapper function around
        `create_plotly_monitoring_html_plot` where the parameters of said
        function are supplied by the assumptions in the configuration file.

        Namely, the duration that the database is queried is where the end
        query time is the current time (as of the function call) and the
        beginning time is some amount of hours ago. The resulting html plot
        file is saved to some location specified by the configuration file
        and the handling of the plotly javascript file is also detailed.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # The current time, as per the function call.
        current_time_jd = library.conversion.current_utc_to_julian_day()
        # The amount of hours (then converted to days to subtract from) ago
        # to query the database.
        QUERY_DAYS_AGO = library.config.MONITOR_PLOT_QUERY_X_HOURS_AGO / 24
        # The times which to query the database for plotting.
        query_begin_jd = current_time_jd - QUERY_DAYS_AGO
        query_end_jd = current_time_jd

        # The zero point y-axis limits.
        lower_zero_point = library.config.MONITOR_PLOT_ZERO_POINT_AXIS_LOWER_LIMIT
        upper_zero_point = library.config.MONITOR_PLOT_ZERO_POINT_AXIS_UPPER_LIMIT

        # The path where the html file will be saved to along with instructions
        # on how to handle the javascript file.
        html_filename = library.config.MONITOR_PLOT_HTML_FILENAME
        # And, the setting for how to handle the javascript.
        include_plotlyjs = library.config.MONITOR_PLOT_PLOTLY_JAVASCRIPT_METHOD

        # Create the plot using this configuration parameters.
        self.create_plotly_monitoring_html_plot(
            html_filename=html_filename,
            plot_query_begin_jd=query_begin_jd,
            plot_query_end_jd=query_end_jd,
            plot_lower_zero_point=lower_zero_point,
            plot_upper_zero_point=upper_zero_point,
            include_plotlyjs=include_plotlyjs,
        )
        # All done.
        return None
