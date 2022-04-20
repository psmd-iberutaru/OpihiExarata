import sys

import numpy as np

import PyQt6 as PyQt
from PyQt6 import QtCore, QtWidgets, QtGui

import matplotlib.figure as mpl_figure
import matplotlib.patches as mpl_patches
import matplotlib.pyplot as plt

# Using Qt backends.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


class TargetSelectorWindow(QtWidgets.QWidget):
    def __init__(self, data_array: hint.array = None) -> None:
        """Create the target selector window. Though often used for asteroids,
        there is no reason why is should specific to them; so we use a general
        name.

        Parameters
        ----------
        data_array : array
            The data from Opihi which is the image that it took. The user will
            use this image to select the location of the target/asteroid.

        Returns
        -------
        None
        """
        # Initialization of the parent class window.
        super().__init__()

        # The data from which will be shown to the user which they will use
        # to find the location of the target.
        self.data_array = data_array
        # The location of the target, the user did not provide it so
        # blank currently.
        self.target_x = None
        self.target_y = None
        # Making the plot itself.
        self.figure = mpl_figure.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ax = self.figure.subplots()
        # A little hack to ensure the default zoom limits that are saved when 
        # redrawing the figure is not 0-1 in both x and y but instead the image
        # itself.
        self.ax.set_xlim(0, self.data_array.shape[1])
        self.ax.set_ylim(0, self.data_array.shape[0])
        # Redrawing the image.
        self.redraw_image()

        # Setting up the mouse click action for the matplotlib image.
        self.canvas.mpl_connect("button_press_event", self.image_mouse_press)
        self.canvas.mpl_connect("button_release_event", self.image_mouse_release)

        # Building the window with the matplotlib plot and the done button.
        self.setWindowTitle("OpihiExarata Target Selector")
        # Using a vertical layout style.
        vertical_layout = QtWidgets.QVBoxLayout()

        # The done/exit button.
        self.done_button = QtWidgets.QPushButton("Done")
        self.done_button.clicked.connect(self.close_window)

        # Assembling the different elements of this GUI window.
        # The image for plotting.
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(self.toolbar)
        vertical_layout.addWidget(self.done_button)

        self.setLayout(vertical_layout)
        # All done.
        return None

    def image_mouse_press(self, event: hint.MouseEvent) -> None:
        """A function to describe what would happen when a mouse press is
        done on the image.

        This function defaults to the toolbar functionality when the toolbar
        is considered active.

        Parameters
        ----------
        event : MouseEvent
            The event of the click itself.

        Returns
        -------
        None
        """

        # A tool on the toolbar is wanting to be used if the mode is non-blank, 
        # prioritize the tool over the selector.
        if self.toolbar.mode.value != "":
            return None

        # Assign the potential location of the target to the location
        # of the mouse.
        if event.xdata is None or event.ydata is None:
            # The user likely clicked outside of the canvas area. Ignore.
            pass
        else:
            # One of the bounds of the search rectangle.
            self.search_x0 = float(event.xdata)
            self.search_y0 = float(event.ydata)
        return None

    def image_mouse_release(self, event: hint.MouseEvent) -> None:
        """A function to describe what would happen when a mouse click released
        on the image.

        Parameters
        ----------
        event : MouseEvent
            The event of the click itself.

        Returns
        -------
        None
        """

        # A tool on the toolbar is wanting to be used if the mode is non-blank, 
        # prioritize the tool over the selector.
        if self.toolbar.mode.value != "":
            return None

        # Assign the potential location of the target to the location
        # of the mouse.
        if event.xdata is None or event.ydata is None:
            # The user likely clicked outside of the canvas area. Ignore.
            pass
        else:
            # One of the bounds of the search rectangle.
            self.search_x1 = float(event.xdata)
            self.search_y1 = float(event.ydata)
        # By convention, the x0 <= x1 and vice versa for y. If the user drew
        # a backwards square, then we fix it here.
        if self.search_x1 < self.search_x0:
            lower_x = min([self.search_x0, self.search_x1])
            upper_x = max([self.search_x0, self.search_x1])
            self.search_x0 = lower_x
            self.search_x1 = upper_x
        if self.search_y1 < self.search_y0:
            lower_y = min([self.search_y0, self.search_y1])
            upper_y = max([self.search_y0, self.search_y1])
            self.search_y0 = lower_y
            self.search_y1 = upper_y

        # Find the target location based on the search area just determined.
        self.target_x, self.target_y = self.find_target_location(
            x0=self.search_x0, x1=self.search_x1, y0=self.search_y0, y1=self.search_y1
        )

        # Redrawing the image to have the location be visible.
        self.redraw_image()
        return None

    def find_target_location(
        self, x0: float, x1: float, y0: float, y1: float
    ) -> tuple[float, float]:
        """Find the location of a target by using a guessed location.
        The bounds of the search is specified by the rectangle.

        Parameters
        ----------
        x0 : float
            The lower x axis bound of the search area. These values are cast
            into integers upon indexing the search area.
        x1 : float
            The upper x axis bound of the search area. These values are cast
            into integers upon indexing the search area.
        y0 : float
            The lower y axis bound of the search area. These values are cast
            into integers upon indexing the search area.
        y1 : float
            The upper y axis bound of the search area. These values are cast
            into integers upon indexing the search area.

        Returns
        -------
        target_x : float
            The location of the target, based on the guess.
        target_y : float
            The location of the target, based on the guess.
        """

        # Define the search area by the search radius. Being generous on the
        # search radius.
        x0 = int(x0)
        x1 = int(x1) + 1
        y0 = int(y0)
        y1 = int(y1) + 1
        search_array = self.data_array[
            y0:y1,
            x0:x1,
        ]

        # Find the location of the target. Using the maximum pixel value as
        # it.
        search_y, search_x = np.unravel_index(
            np.nanargmax(search_array), search_array.shape
        )
        # Transform it back into the total array coordinates.
        target_x = x0 + search_x
        target_y = y0 + search_y
        # Define the location of the target as the center of the maximum
        # pixel, not its edge.
        target_x += 0.5
        target_y += 0.5

        # All done.
        return target_x, target_y

    def close_window(self) -> None:
        """Closes the window. Generally called when it is all done.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Delete the plot. This ensures that there is not memory leak with
        # many plots open over time.
        plt.close(self.figure)
        # Close the window.
        self.close()
        return None

    def redraw_image(self) -> None:
        """Redraw and refresh the image, this is mostly used to allow for the
        program to update where the user selected.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # To retain the current zoom and pan, save the limits that the image 
        # is currently at before redrawing.
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()

        # Clearing the axes, starting fresh and anew as this entire function
        # does a whole redraw. It may not be needed but small performance
        # hit to ensure it all works normally.
        self.ax.clear()

        # Creating the image of the image data.
        self.ax.imshow(self.data_array, zorder=-1)

        # If there is a specified target location, put it on the map.
        if isinstance(self.target_x, (int, float)) and isinstance(
            self.target_y, (int, float)
        ):
            # Represent the marker as the targets location as defined by the 
            # search box and the target finding function.
            MARKER_SIZE = float(library.config.SELECTOR_IMAGE_PLOT_TARGET_MARKER_SIZE)
            self.ax.scatter(
                self.target_x,
                self.target_y,
                s=MARKER_SIZE,
                marker="^",
                color="r",
                facecolors="None",
            )
            # If there is a target, then the bounding box created must have
            # also succeeded. It is helpful for the user to also draw it.
            search_rectangle = mpl_patches.Rectangle(
                xy=(self.search_x0, self.search_y0),
                width=self.search_x1 - self.search_x0,
                height=self.search_y1 - self.search_y0,
                facecolor="None",
                edgecolor="b",
            )
            self.ax.add_patch(search_rectangle)
        else:
            # No need, there is no current valid location specified.
            pass

        # Reinstate the zoom and pan settings via the previous limits.
        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)
        # A tight layout to save space.
        self.figure.tight_layout()
        # And finally, drawing the image.
        self.canvas.draw()
        # All done.
        return None


def ask_user_target_selector_window(data_array:hint.array) -> tuple[float, float]:
    """Use the target selector window to have the user provide the
    information needed to determine the location of the target.

    Parameters
    ----------
    data_array : array-like
        The image data array which will be displayed to the user to have them
        find the target.

    Returns
    -------
    target_x : float
        The location of the target in the x axis direction.
    target_y : float
        The location of the target in the y axis direction.
    """
    # Create the target selector viewer window and let the user interact with
    # it until they let the answer be found.
    data_array = np.array(data_array)
    target_selector_window = TargetSelectorWindow(data_array=data_array)
    # Freeze all other processes until the location of the target has been
    # determined. This is a blocking process because everything else requires
    # this to be done.
    target_selector_window.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
    target_selector_window.show()
    # Using an event loop to wait until the widget closes, which is when
    # the user is done selecting the target location.
    loop = QtCore.QEventLoop()
    target_selector_window.destroyed.connect(loop.quit)
    loop.exec()

    # The extracted target pixel location values.
    target_x = target_selector_window.target_x
    target_y = target_selector_window.target_y
    # All done.
    return target_x, target_y


if __name__ == "__main__":
    # This is really just to test the GUI, to actually use the GUI, please use
    # the proper function.
    application = QtWidgets.QApplication([])

    ##### TESTING
    delta = 0.025
    x = y = np.arange(-3.0, 3.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-(X**2) - Y**2)
    Z2 = np.exp(-((X - 1) ** 2) - (Y - 1) ** 2)
    data_array = (Z1 - Z2) * 2

    x, y = ask_user_target_selector_window(data_array=data_array)
    print("XY Coordinates: ", x, y)
    sys.exit()
