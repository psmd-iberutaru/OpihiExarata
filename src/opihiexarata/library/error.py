"""Errors pertinent to the function of Exarata."""

# Halting errors
####################

class ExarataBaseException(BaseException):
    """The base exception class. This is for exceptions that should never be 
    caught and should bring everything to a halt."""
    def __init__(self, message:str=None)-> None:
        # The user's message.
        message = message if message is not None else ""
        # There also defined is two extra lines of text, this helps with 
        # giving the user more information as to how to proceed.
        prefix = "(OpihiExarata) TERMINAL - "
        suffix ="\n" + ">> Contact the maintainers of OpihiExarata to fix this issue."
        self.message = prefix + message + suffix
    def __str__(self) -> str:
        return self.message



# Handled errors
####################

class ExarataException(Exception):
    """The main inheriting class which all exceptions use as their base. This 
    is done for ease of error handling and is something that can and should be 
    managed."""
    def __init__(self, message:str=None)->None:
        # The user's message.
        message = message if message is not None else ""
        # Note that these errors are from OpihiExarata.
        prefix = "(OpihiExarata) - "
        self.message = prefix + message
    def __str__(self) -> str:
        return self.message

class FileError(ExarataException):
    """An error to be used when obtaining data files or configuration files
    and something fails."""
    pass

class ConfigurationError(ExarataException):
    """An error to be used where the expectation of how configuration files 
    and configuration parameters are structures are violated."""


# Warnings
####################