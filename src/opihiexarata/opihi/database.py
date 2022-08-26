"""The database solution for storing and recording zero point data. 
We use a flat file database here with ordered directories to make it easily 
transversal by other tools and to have it be simple. A single instance of 
this class should monitor its own database."""


import os 
import datetime

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

class OpihiZeroPointDatabaseSolution(library.engine.ExarataSolution):
    """The flat file database solution which provides an API-like solution to
    interacting with a flat-file database with nested folders for all of the 
    zero point entries.
    
    Attributes
    ----------
    database_directory : string
        The path to the directory where the flat file database is.
    """

    def __init__(self, database_directory:str) -> None:
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
        check_filename = library.path.merge_pathname(directory=database_directory, filename="exarata_database", extension="check")
        if os.path.isfile(check_filename):
            pass
        else:
            # If the directory is empty, we assume to start a new database.
            if len(os.listdir(database_directory)) == 0:
                # Creating the check file.
                with open(check_filename, "w"):
                    pass
                # We can still continue with the database
            else:
                raise error.DirectoryError("The directory provided {dir} is not a directory which is detected to be a proper database directory for zero point recording; neither is it an empty directory to start a new database.".format(dir=database_directory))
        # Keeping the record.
        self.database_directory = database_directory

    
    def _generate_zero_point_record(self, year:int, month:int, day:int, hour:int, minute:int, second:int, zero_point:float, zero_point_error:float, filter_name:str) -> str:
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
            record_datetime = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        except ValueError:
            raise error.InputError("The time and date values provided cannot be composed to a real life date and time.")
        else:
            datetime_string = record_datetime.isoformat(timespec="seconds")

        # We compose the zero point string, both the value and the error.
        ascii_plus_minus_symbol = "+/-"
        length = 12
        zero_point_string = "{zp:{ln}.{zp_f}f}  {pm}  {zpe:{ln}.{zpe_f}f}".format(zp=zero_point, zpe=zero_point_error, pm=ascii_plus_minus_symbol, ln=length, zp_f = length - 3 - 1, zpe_f=length-1-1)

        # We compose the filter name string.
        filter_string = "{flt:>2}".format(flt=filter_name)

        # Combing it all together now.
        zero_point_record = "{time}    {zp_e}    {flt}".format(time=datetime_string, zp_e=zero_point_string, flt=filter_string)
        # All done.
        return zero_point_record