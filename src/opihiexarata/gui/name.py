"""This window is for allowing the user to fill out the name of the object
which they are observing, used when doing new targets.

This is just a simple input dialog.
"""

import sys

from PySide6 import QtCore, QtWidgets, QtGui


import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

import opihiexarata.gui as gui


class TargetNameWindow(QtWidgets.QWidget):
    """This is the pop up window which will ask for the name of the target.
    Some sanitization of the name also happens here to make sure it is proper.

    Really, this class is a little bit of a wrapper around the InputDialog
    widget.

    Attributes
    ----------
    _raw_target_name : string
        The raw string input from the user.
    target_name : string
        The entered name as specified by the user after input sanitization.
    status : bool
        The status of the entry. If it was exited with a proper input and
        submission, this is true. If it was canceled or closed in any other
        way it is False.
    """

    def __init__(self) -> None:
        """Setting up the window for the user prompt.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Initialization of the parent class window.
        super().__init__()
        # Window icon, we use the default for now.
        gui.functions.apply_window_icon(window=self, icon_path=None)

        # Preparing the input dialog which we wrap around.
        input_dialog = QtWidgets.QInputDialog(self)
        input_dialog.setWindowTitle("OpihiExarata Target Name Entry")
        input_dialog.setLabelText("Enter New Target Name: ")
        input_dialog.setOkButtonText("Submit")
        input_dialog.setCancelButtonText("Cancel")
        # Run the input dialog.
        status = input_dialog.exec()
        self._raw_target_name = input_dialog.textValue()
        self.target_name = self._sanitize_input(raw_input=self._raw_target_name)
        self.status = bool(status)
        # All done.
        return None

    @staticmethod
    def _sanitize_input(raw_input: str = None) -> str:
        """Sanitization of the raw input to the proper input.

        Parameters
        ----------
        raw_input : string
            The raw input to be sanitized.

        Returns
        -------
        sanitized_input : string
            The sanitized input.
        """
        # Nothing for now, something that needs to be done.
        sanitized_input = str(raw_input)
        return sanitized_input


def ask_user_target_name_window(default: str = None) -> str:
    """Use the target name window to prompt the user for the name of the
    object that they are studying.

    Parameters
    ----------
    default : string
        The default name to provide should the user interact with the dialog
        box to submit a name. (That is, they cancel or close it.)

    Returns
    -------
    target_name : string
        The target name as specified (or the default if something went amiss.)
    """
    # Use the input dialog class to ask the user.
    target_name_window = TargetNameWindow()
    # Derive the results from the input.
    input_name = target_name_window.target_name
    submit_status = target_name_window.status

    # If the name was provided correctly, then give them the proper name.
    # Otherwise return the default name if it exists; otherwise, we give
    # difference to the user's submission and hope it does not break
    # anything.
    target_name = None
    if submit_status:
        target_name = str(input_name)
    else:
        if default is not None:
            target_name = default
        else:
            target_name = str(input_name)
    # All done.
    return target_name


def main() -> None:
    # This is really just to test the GUI, to actually use the GUI, please use
    # the proper function.
    application = QtWidgets.QApplication([])

    default = "default"

    name = ask_user_target_name_window(default=default)
    print("Test target name: ", name)
    sys.exit()


if __name__ == "__main__":
    main()
