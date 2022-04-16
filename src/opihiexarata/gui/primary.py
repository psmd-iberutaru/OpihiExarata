"""
The primary GUI window.
"""

import sys
import random
import os

import PyQt6 as PyQt
from PyQt6 import QtCore, QtWidgets, QtGui

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.figure as mpl_figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import opihiexarata
import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint
import opihiexarata.gui as gui


class OpihiPrimaryWindow(QtWidgets.QMainWindow):
    """The GUI that is responsible for interaction between the user and the
    two primary Opihi solutions, the image (OpihiPreprocessSolution) and the
    results (OpihiSolution).

    Only non-GUI attributes are listed here.

    Attributes
    ----------
    raw_fits_filename
    process_fits_filename
    preprocess_solution
    opihi_solution

    """

    def __init__(self) -> None:
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
        # Qt designer files.
        super(OpihiPrimaryWindow, self).__init__()
        self.ui = gui.qtui.Ui_PrimaryWindow()
        self.ui.setupUi(self)

        # Establishing the defaults for all of the relevant attributes.
        self.raw_fits_filename = None
        self.process_fits_filename = None
        self.preprocess_solution = None
        self.opihi_solution = None

        # Preparing the new file buttons.
        self.__init_new_file_buttons()

        # Preparing the image area for Opihi sky images.
        self.__init_opihi_image()

        # Preparing the preprocessing solution so that the raw files loaded
        # into Exarata can be instantly turned into reduced images.
        self.__init_preprocess_solution()

        # All done.
        return None

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
        self.ui.push_button_new_image_automatic.clicked.connect(
            self.__connect_new_fits_filename_automatic
        )
        self.ui.push_button_new_image_manual.clicked.connect(
            self.__connect_new_fits_filename_manual
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
        # Deriving the size of the image from the filler dummy image. The
        # figure should be a square. (Height really is the primary concern.)
        pix_to_in = lambda p: p / plt.rcParams["figure.dpi"]
        dummy_edge_size = self.ui.dummy_opihi_image.height()
        edge_size = pix_to_in(dummy_edge_size)
        # The figure, canvas, and navigation toolbar of the image plot
        # using a Matplotlib Qt widget backend. We will add these to the
        # layout later.
        fig, ax = plt.subplots(figsize=(edge_size, edge_size), constrained_layout=True)
        self._opihi_figure = fig
        self._opihi_axes = ax
        self._opihi_canvas = FigureCanvas(self._opihi_figure)
        self._opihi_nav_toolbar = NavigationToolbar(self._opihi_canvas, self)

        # For ease of usage, a custom navigation bar coordinate formatter
        # function/class is used.
        class CoordinateFormatter:
            """A simple function class to properly format the navigation bar
            coordinate text. This assumes the current structure of the GUI."""

            def __init__(self, gui_instance: OpihiPrimaryWindow) -> None:
                self.gui_instance = gui_instance
                return None

            def __call__(self, x, y) -> str:
                """The coordinate string going to be put onto the navigation
                bar."""
                x_index = int(x)
                y_index = int(y)
                coord_string = "Helllo [{x_int:d}, {y_int:d}]".format(
                    x_int=x_index, y_int=y_index
                )
                print(coord_string)
                return coord_string

        # Assigning the coordinate formatter derived.
        self._opihi_coordinate_formatter = CoordinateFormatter(self)
        self._opihi_axes.format_coord = self._opihi_coordinate_formatter
        self._opihi_axes.format_cursor_data = lambda s: "Poop"

        # The push button for redrawing/refreshing the figure.
        self.push_button_redraw_plot = QtWidgets.QPushButton("Refresh")
        self.push_button_redraw_plot.clicked.connect(self.redraw_opihi_image)

        # Setting the layout, it is likely better to have the toolbar below
        # rather than above to avoid conflicts with the reset buttons in the
        # event of a misclick.
        self.ui.vertical_layout_image.addWidget(self._opihi_canvas)
        self.ui.vertical_layout_image.addWidget(self._opihi_nav_toolbar)
        self.ui.vertical_layout_image.addWidget(self.push_button_redraw_plot)
        # Remove the dummy spacer otherwise it is just extra unneeded space.
        self.ui.vertical_layout_image.removeWidget(self.ui.dummy_opihi_image)
        self.ui.dummy_opihi_image.deleteLater()
        self.ui.dummy_opihi_image = None
        del self.ui.dummy_opihi_image
        return None

    def __init_preprocess_solution(self):
        """Initialize the preprocessing solution. The preprocessing files
        should be specified in the configuration file.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Using the configuration file to extract where the preprocessing
        # filenames are to build the solution.
        try:
            preprocess = opihiexarata.OpihiPreprocessSolution(
                mask_c_fits_filename=library.config.PREPROCESS_MASK_C_FITS_FILENAME,
                mask_g_fits_filename=library.config.PREPROCESS_MASK_G_FITS_FILENAME,
                mask_r_fits_filename=library.config.PREPROCESS_MASK_R_FITS_FILENAME,
                mask_i_fits_filename=library.config.PREPROCESS_MASK_I_FITS_FILENAME,
                mask_z_fits_filename=library.config.PREPROCESS_MASK_Z_FITS_FILENAME,
                mask_1_fits_filename=library.config.PREPROCESS_MASK_1_FITS_FILENAME,
                mask_2_fits_filename=library.config.PREPROCESS_MASK_2_FITS_FILENAME,
                mask_3_fits_filename=library.config.PREPROCESS_MASK_3_FITS_FILENAME,
                flat_c_fits_filename=library.config.PREPROCESS_FLAT_C_FITS_FILENAME,
                flat_g_fits_filename=library.config.PREPROCESS_FLAT_G_FITS_FILENAME,
                flat_r_fits_filename=library.config.PREPROCESS_FLAT_R_FITS_FILENAME,
                flat_i_fits_filename=library.config.PREPROCESS_FLAT_I_FITS_FILENAME,
                flat_z_fits_filename=library.config.PREPROCESS_FLAT_Z_FITS_FILENAME,
                flat_1_fits_filename=library.config.PREPROCESS_FLAT_1_FITS_FILENAME,
                flat_2_fits_filename=library.config.PREPROCESS_FLAT_2_FITS_FILENAME,
                flat_3_fits_filename=library.config.PREPROCESS_FLAT_3_FITS_FILENAME,
                bias_fits_filename=library.config.PREPROCESS_BIAS_FITS_FILENAME,
                dark_current_fits_filename=library.config.PREPROCESS_DARK_CURRENT_FITS_FILENAME,
                linearity_fits_filename=library.config.PREPROCESS_LINEARITY_FITS_FILENAME,
            )
        except Exception:
            # Something failed with making the preprocess solution, a
            # configuration file issue is likely the reason.
            # TODO
            preprocess = None
        finally:
            self.preprocess_solution = preprocess
        # All done.
        return None

    def __connect_new_fits_filename_automatic(self):
        """The automatic method relying on earliest fits file avaliable in
        the expected directory. This function is a connected function action to
        a button in the GUI.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # TODO
        new_fits_filename = "pie"

        # If the user did not provide a file to enter, there is nothing to be
        # changed.
        if os.path.isfile(new_fits_filename):
            # Assign the new fits filename.
            self.raw_fits_filename = os.path.abspath(new_fits_filename)
        else:
            # Exit!
            return None

        # Process the file first so that what the user sees is closer to
        # what it really is.

        # Load up the new file.
        self._load_fits_file(fits_filename=self.raw_fits_filename)
        # All done.
        return None

    def __connect_new_fits_filename_manual(self):
        """The manual method relying on earliest fits file avaliable in
        the expected directory. This function is a connected function action to
        a button in the GUI.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Ask the user for the filename via a dialog.
        new_fits_filename, __ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Open Opihi Image",
            directory="./",
            filter="FITS Files (*.fits)",
        )
        # If the user did not provide a file to enter, there is nothing to be
        # changed.
        if os.path.isfile(new_fits_filename):
            # Assign the new fits filename.
            self.raw_fits_filename = os.path.abspath(new_fits_filename)
        else:
            # Exit!
            return None

        # Process the file first so that what the user sees is closer to
        # what it really is.

        # Load up the new file.
        self._load_fits_file(fits_filename=self.raw_fits_filename)
        # All done.
        return None

    def _preprocess_fits_file(
        self, raw_filename: str, process_filename: str = None
    ) -> str:
        """Using the provided filename, preprocess the fits file listed.

        This is used primarily during the loading of a new fits file.

        Parameters
        ----------
        raw_filename : string
            The filename of the raw fits file to be preprocessed.
        process_filename : string, default = None
            The filename where the processed fits file will be saved to. If
            None, it defaults to a sensible naming convention to distinguish
            the two.

        Returns
        -------
        process_filename : string
            The filename of the preprocessed file is returned, this is just
            in case the value was derived from the naming convention. This is
            an absolute path.
        """
        # Deriving saving location of the processed fits file.
        if isinstance(process_filename, str):
            process_filename = os.path.abspath(process_filename)
        else:
            # Use a sensible naming convention to distinguish between the raw
            # and processed file.
            # TODO
            process_filename = "./process.fits"

        # Saving for later.
        self.process_fits_filename = process_filename

        # Process the fits file.
        __ = self.preprocess_solution.preprocess_fits_file(
            raw_filename=raw_filename, out_filename=process_filename
        )
        # All done.
        return process_filename

    def _load_fits_file(self, fits_filename: str) -> None:
        """Load a fits file into the GUI to derive all of the solutions needed.

        This loads the fits file into an OpihiSolution class for which this
        GUI interacts with and derives the information from.

        Parameters
        ----------
        fits_filename : str
            The fits filename which will be loaded.

        Returns
        -------
        None
        """

        # Although the OpihiSolution could derive these values from the
        # header of the filename, the solution class is built to be general.
        filter_name = "g"
        exposure_time = 10
        observing_time = 100
        asteroid_name = None
        asteroid_location = None
        asteroid_history = None

        # Creating the solution from the data.
        opihi_solution = opihiexarata.OpihiSolution(
            fits_filename=fits_filename,
            filter_name=filter_name,
            exposure_time=exposure_time,
            observing_time=observing_time,
            asteroid_name=asteroid_name,
            asteroid_location=asteroid_location,
            asteroid_history=asteroid_history,
        )
        self.opihi_solution = opihi_solution

        # Because a new image was loaded, the previous values and other
        # information derived from the last image is invalid, reset and replot.
        self.reset_dynamic_label_text()
        self.redraw_opihi_image()
        return None

    def reset_dynamic_label_text(self) -> None:
        """Reset all of the dynamic label text, this is traditionally done
        just before a new image is going to be introduced.

        This resets the text back to their defaults.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
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
        # This is a function which allows for the disabling of other axes 
        # formatting their data values and messing with the formatter class.
        def empty_string(string:str) -> str:
            return str()

        # Clear the information before replotting, it is easier just to draw
        # it all again.
        self._opihi_axes.clear()

        # Attempt to plot the image data if it exists.
        if self.opihi_solution is not None:
            image = self._opihi_axes.imshow(self.opihi_solution.data)
            image.format_cursor_data = empty_string

        # TESTING
        rand = np.random.rand(5)
        self._opihi_axes.plot(rand, 1 / rand)

        # Make sure the coordinate formatter does not change.
        self._opihi_axes.format_coord = self._opihi_coordinate_formatter
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
