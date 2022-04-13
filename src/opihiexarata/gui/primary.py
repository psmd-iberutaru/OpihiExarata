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
    """The GUI that is responsible for interaction between the user and the
    two primary Opihi solutions, the image (OpihiPreprocessSolution) and the 
    results (OpihiSolution).
    """


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

        # Preparing the new file buttons.
        self.__init_new_file_buttons()

        # Preparing the image area for Opihi sky images.
        self.__init_opihi_image()

    def __init_new_file_buttons(self) -> None:
        """Assign the action bindings for the buttons which get new
        file(names).

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Assigning actions to the buttons.
        self.ui.button_new_image_automatic.clicked.connect(
            lambda: self.get_new_fits_image(filename_mode="automatic")
        )
        self.ui.button_new_image_manual.clicked.connect(
            lambda: self.get_new_fits_image(filename_mode="manual")
        )

    def __init_opihi_image(self) -> None:
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
        self.button = QtWidgets.QPushButton("Plot")
        self.button.clicked.connect(self.redraw_opihi_image)

        # Setting the layout, it is likely better to have the toolbar below
        # rather than above to avoid conflicts with the reset buttons in the
        # event of a misclick.
        self.ui.image_vertical_layout.addWidget(self._opihi_canvas)
        self.ui.image_vertical_layout.addWidget(self._opihi_nav_toolbar)
        self.ui.image_vertical_layout.addWidget(self.button)
        # Remove the dummy spacer otherwise it is just extra unneeded space.
        self.ui.image_vertical_layout.removeWidget(self.ui.dummy_opihi_image)
        self.ui.dummy_opihi_image.deleteLater()
        self.ui.dummy_opihi_image = None
        return None

    def redraw_opihi_image(self) -> None:
        """Redraw the Opihi image given that new results may have been added
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
        ax.plot(data, "*-")

        # A tight layout to improve realestate efficiency.
        self._opihi_figure.tight_layout()
        # Update and redraw the image via redrawing the canvas.
        self._opihi_canvas.draw()
        return None

    def get_new_fits_image(self, filename_mode: str = "automatic") -> str:
        """Automatically get the most recent file taken from the area where the
        fits files are to be stored.

        Parameters
        ----------
        filename_mode : string
            This function can get the new image filename automatically or
            manually.

                - `automatic` : Fetch the most recent image from the
                  configured directory automatically.
                - `manual` : Have the user select the file using a file
                  dialog pop up.

        Returns
        -------
        new_image : str
            The absolute path of the new fits file.
        """

        def _get_new_fits_filename(mode:str):
            # Different methods based on the different modes.
            filename_mode = filename_mode.casefold()
            if filename_mode == "automatic":
                # Find the file name automatically using the most recent image.
                # TODO
                new_filename = "pie"
            elif filename_mode == "manual":
                # Use a file dialog box to get the file name. We do not need the
                # filter information.
                new_filename, __ = QtWidgets.QFileDialog.getOpenFileName(
                    parent=self,
                    caption="Open Opihi Image",
                    directory="./",
                    filter="FITS Files (*.fits)",
                )
            else:
                raise error.InputError(
                    "The filename mode of getting the filename is not supported."
                )
            return new_filename


def main():
    app = QtWidgets.QApplication([])

    application = OpihiPrimaryWindow()

    application.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
