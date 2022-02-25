"""
The primary GUI window.
"""

import PyQt6 as PyQt
from PyQt6 import QtCore, QtWidgets, QtGui

import sys
import random

import matplotlib.figure as mpl_figure
# Using Qt backends.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint
import opihiexarata.gui as gui

class OpihiPrimaryWindow(QtWidgets.QMainWindow):

    def __init__(self):
        """The primary GUI window for OpihiExarata. This interacts directly 
        with the total solution object of Opihi.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Creating the GUI itself using the Qt framework and the converted
        # Qt designer files.s
        super(OpihiPrimaryWindow, self).__init__()
        self.ui = gui.qtui.Ui_PrimaryWindow()
        self.ui.setupUi(self)

        # Preparing the image area for Opihi sky images.
        self.__init_opihi_image()

    def __init_opihi_image(self):
        """Create the image area which will display what Opihi took from the 
        sky. This takes advantage of a reserved image vertical layout in the 
        design of the window.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # The figure, canvas, and navigation toolbar of the image plot 
        # using a Matplotlib Qt widget backend. We will add these to the 
        # layout later.
        self._opihi_figure = mpl_figure.Figure()
        self._opihi_canvas = FigureCanvas(self._opihi_figure)
        self._opihi_nav_toolbar = NavigationToolbar(self._opihi_canvas, self)

        # Just some button connected to `plot` method
        self.button = QtWidgets.QPushButton('Plot')
        self.button.clicked.connect(self.update_opihi_image)

        # Setting the layout, it is likely better to have the toolbar below 
        # rather than above to avoid conflicts with the reset buttons in the 
        # event of a misclick.
        self.ui.image_vertical_layout.addWidget(self._opihi_canvas)
        self.ui.image_vertical_layout.addWidget(self._opihi_nav_toolbar)
        self.ui.image_vertical_layout.addWidget(self.button)
        return None

    def update_opihi_image(self):
        """Update the Opihi image given that new results may have been added
        because some solutions were completed. This modifies the GUI in-place.
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # random data
        data = [random.random() for i in range(10)]

        # instead of ax.hold(False)
        self._opihi_figure.clear()

        # create an axis
        ax = self._opihi_figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.plot(data, '*-')

        # A tight layout to improve realestate efficiency.
        self._opihi_figure.tight_layout()
        # Update and redraw the image via redrawing the canvas.
        self._opihi_canvas.draw()
        return None



def main():
    app = QtWidgets.QApplication([])

    application = OpihiPrimaryWindow()

    application.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()