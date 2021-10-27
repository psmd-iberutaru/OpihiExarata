"""Error, warning, and logging functionality pertinent to the function of Exarata."""

import warnings

# Halting errors
####################


class ExarataBaseException(BaseException):
    """The base exception class. This is for exceptions that should never be
    caught and should bring everything to a halt."""

    def __init__(self, message: str = None) -> None:
        """The initialization of a base exception for OpihiExarata.

        Parameters
        ----------
        message : string
            The message of the error message.

        Returns
        -------
        None
        """
        # The user's message.
        message = message if message is not None else "Unrecoverable error!"
        # There also defined is two extra lines of text, this helps with
        # giving the user more information as to how to proceed.
        prefix = "(OpihiExarata) TERMINAL - "
        suffix = "\n" + ">> Contact the maintainers of OpihiExarata to fix this issue."
        self.message = prefix + message + suffix

    def __str__(self) -> str:
        return self.message


class DevelopmentError(ExarataBaseException):
    """This is an error where the development of OpihiExarata is not correct and
    something is not coded based on the expectations of the software itself.
    This is not the fault of the user."""

class LogicFlowError(ExarataBaseException):
    """This is an error to ensure that the logic does not flow to a point to a 
    place where it is not supposed to. This is helpful in making sure changes 
    to the code do not screw up the logical flow of the program."""

class UndiscoveredError(ExarataBaseException):
    """This is an error used in cases where the source of the error has not 
    been determined and so a more helpful error message or mitigation strategy 
    cannot be devised."""

# Handled errors
####################


class ExarataException(Exception):
    """The main inheriting class which all exceptions use as their base. This
    is done for ease of error handling and is something that can and should be
    managed."""

    def __init__(self, message: str = None) -> None:
        """The initialization of a normal exception.

        Parameters
        ----------
        message : string
            The message of the error message.

        Returns
        -------
        None
        """
        # The user's message.
        message = message if message is not None else "Error."
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

    pass

class ReadOnlyError(ExarataException):
    """An error where variables or files are assumed to be read only, this 
    enforces that notion."""

class WebRequestError(ExarataException):
    """An error to be used when a web request to some API fails, either because
    of something from their end, or our end."""

    pass


# Warnings
####################


class ExarataWarning(UserWarning):
    pass


def warn(
    warn_class: type[ExarataWarning] = ExarataWarning,
    message: str = "",
    stacklevel: int = 2,
):
    """The common method to use to warn for any OpihiExarata based warnings.

    This is used because it has better context manager wrappers.

    Parameters
    ----------
    warn_class : type, default = ExarataWarning
        The warning class, it must be a subtype of a user warning.
    message : string, default = ""
        The warning message.
    stacklevel : integer, default = 2
        The location in the stack that the warning call will highlight.

    Returns
    -------
    None
    """
    # The warning class must be a subset of the OpihiExarata warnings as that
    # is all this function is supposed to use.
    if not issubclass(warn_class, ExarataWarning):
        raise DevelopmentError(
            "The OpihiExarata warning system is build only for user defined errors"
            " coming from OpihiExarata."
        )
    else:
        warnings.warn(message=message, category=warn_class, stacklevel=stacklevel)
    return None


# Logging
####################


# Context manegers
####################
