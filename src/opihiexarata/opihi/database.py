"""The database solution for storing and recording zero point data. 
We use a flat file database here with ordered directories to make it easily 
transversal by other tools and to have it be simple. A single instance of 
this class should monitor its own database."""


import os
import datetime
import glob

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
        # We check if the database follows the expected design assumptions by
        # checking if the check file is there. If it is not, then we may need
        # format the database ourselves.
        check_filename = library.path.merge_pathname(
            directory=database_directory, filename=DATABASE_CHECK_FILE_BASENAME, extension=DATABASE_CHECK_FILE_EXTENSION
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
        self.database_directory = database_directory

        # All done.
        return None


    @classmethod
    def clean_text_record_file(cls, filename: str, garbage_filename: str = None) -> None:
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
    def clean_database_files(cls, database_directory:str, garbage_filename: str = None) -> None:
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
            directory=database_directory, filename=DATABASE_CHECK_FILE_BASENAME, extension=DATABASE_CHECK_FILE_EXTENSION
        )
        if not os.path.isfile(check_filename):
            raise error.DirectoryError("The directory {dir} provided is not a valid OpihiExarata zero point database directory as it is missing the check file. We will not attempt to clean it.".format(dir=database_directory))

        # We search through all of the database files. We do not try and 
        # clean non-database files.
        database_glob_search = library.path.merge_pathname(directory=database_directory, filename="*.zp_ox", extension="txt")
        database_files = glob.glob(database_glob_search)
        # Clean every file.
        for filedex in database_files:
            cls.clean_text_record_file(filename=filedex, garbage_filename=garbage_filename)
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

    def _generate_zero_point_record(
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
                " date and time."
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

    def add_zero_point_record(
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
        clean_file : bool, default = False
            If True, along with appending the zero point record to the
            current file, we sort the file by time and clean up any bad
            entries.

        Returns
        -------
        None
        """
        # We need to compose the record from the information provided.
        zero_point_record = self._generate_zero_point_record(
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
            self.clean_text_record_file(filename=record_filename)

        # All done.
        return None
