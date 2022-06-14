"""This is where the automatic mode window is implemented."""

import sys
import os

from PySide6 import QtCore, QtWidgets, QtGui

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import opihiexarata
import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

import opihiexarata.astrometry as astrometry
import opihiexarata.photometry as photometry
import opihiexarata.propagate as propagate
import opihiexarata.orbit as orbit
import opihiexarata.ephemeris as ephemeris

import opihiexarata.gui as gui


class OpihiAutomaticWindow(QtWidgets.QMainWindow):
    """The GUI that is responsible for the implementation of the automatic mode
    of Opihi, fetching images automatically based on time and solving for both
    the astrometry and photometry.

    Only non-GUI attributes are listed here.

    Attributes
    ----------
    fits_fetch_directory : string
        The directory which the fits files should be automatically pulled from.
    working_fits_filename : string
        The filename of the fits file which is being worked on, or will be 
        worked on.
    results_fits_filename : string
        The filename of the fits file which has already been solved. The 
        results of which is posted.
    working_opihi_solution : OpihiSolution
        The OpihiSolution of the current working fits file. The results fits 
        file solution, when determined to be solved, should be saved to disk
        automatically.
    active_status : bool
        The flag which determines if the software is still considered in 
        automatic mode and should be still solving images. If True, the process
        assumes that it is still active.
    """

    def __init__(self) -> None:
        """The automatic GUI window for OpihiExarata. This interacts with 
        the user with regards to the automatic solving mode of Opihi.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Creating the GUI itself using the Qt framework and the converted
        # Qt designer files.
        super(OpihiAutomaticWindow, self).__init__()
        self.ui = gui.qtui.Ui_AutomaticWindow()
        self.ui.setupUi(self)

        # Establishing the defaults for all of the relevant attributes.
        self.fits_fetch_directory = None
        self.working_fits_filename = None
        self.results_fits_filename = None
        self.working_opihi_solution = None
        self.active_status = False

        # Preparing the buttons, GUI, and other functionality.
        self.__init_gui_connections()

        # All done.
        return None

    def __init_gui_connections(self) -> None:
        """Creating the function connections for the GUI interface.
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """


    def __connect_push_button_change_directory(self) -> None:
        """The connection for the button to change the automatic fetch 
        directory.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        


    def refresh_window(self) -> None:
        """Refreshes the GUI window with new information where available."""
    