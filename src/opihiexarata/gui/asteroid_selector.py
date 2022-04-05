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


class AsteroidSelectorWindow(QtWidgets.QWidget):
    def __init__(self, data_array: hint.array = None) -> None:
        """Create the asteroid selector window.

        Parameters
        ----------
        data_array : array
            The data from Opihi which is the image that it took. The user will
            use this image to select the location of the asteroid.

        Returns
        -------
        None
        """
        # Initialization of the parent class window.
        super().__init__()

        ##### TESTING
        delta = 0.025
        x = y = np.arange(-3.0, 3.0, delta)
        X, Y = np.meshgrid(x, y)
        Z1 = np.exp(-(X**2) - Y**2)
        Z2 = np.exp(-((X - 1) ** 2) - (Y - 1) ** 2)
        data_array = (Z1 - Z2) * 2

        # The data from which will be shown to the user which they will use
        # to find the location of the asteroid.
        self.data_array = data_array
        # The location of the asteroid, the user did not provide it so
        # blank currently.
        self.asteroid_x = None
        self.asteroid_y = None
        # Making the plot itself.
        self.figure = mpl_figure.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.subplots()
        self.redraw_image()

        # Setting up the mouse click action for the matplotlib image.
        self.canvas.mpl_connect("button_press_event", self.image_mouse_press)
        self.canvas.mpl_connect("button_release_event", self.image_mouse_release)

        # Building the window with the matplotlib plot and the done button.
        self.setWindowTitle("OpihiExarata Asteroid Selector")
        # Using a vertical layout style.
        layout = QtWidgets.QVBoxLayout()

        # The done/exit button.
        self.done_button = QtWidgets.QPushButton("Done")
        self.done_button.clicked.connect(self.close_window)

        # Assembling the different elements of this GUI window.
        # The image for plotting.
        layout.addWidget(self.canvas)
        layout.addWidget(self.done_button)

        self.setLayout(layout)
        # All done.
        return None

    def image_mouse_press(self, event: hint.MouseEvent) -> None:
        """A function to describe what would happen when a mouse press is
        done on the image.

        Parameters
        ----------
        event : MouseEvent
            The event of the click itself.

        Returns
        -------
        None
        """
        # Assign the potential location of the asteroid to the location
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
        # Assign the potential location of the asteroid to the location
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

        # Find the asteroid location based on the search area just determined.
        self.asteroid_x, self.asteroid_y = self.find_asteroid_location(
            x0=self.search_x0, x1=self.search_x1, y0=self.search_y0, y1=self.search_y1
        )

        # Redrawing the image to have the location be visible.
        self.redraw_image()
        return None

    def find_asteroid_location(
        self, x0: float, x1: float, y0: float, y1: float
    ) -> tuple[float, float]:
        """Find the location of an asteroid by using a guessed location.
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
        asteroid_x : float
            The location of the asteroid, based on the guess.
        asteroid_y : float
            The location of the asteroid, based on the guess.
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

        # Find the location of the asteroid. Using the maximum pixel value as
        # it.
        search_y, search_x = np.unravel_index(
            np.nanargmax(search_array), search_array.shape
        )
        # Transform it back into the total array coordinates.
        asteroid_x = x0 + search_x
        asteroid_y = y0 + search_y
        # Define the location of the asteroid as the center of the maximum
        # pixel, not its edge.
        asteroid_x += 0.5
        asteroid_y += 0.5

        # All done.
        return asteroid_x, asteroid_y

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
        # Clearing the axes, starting fresh and anew as this entire function
        # does a whole redraw. It may not be needed but small performance
        # hit to ensure it all works normally.
        self.ax.clear()

        # Creating the image of the image data.
        self.ax.imshow(self.data_array, zorder=-1)

        # If there is an asteroid location, put it on the map.
        if isinstance(self.asteroid_x, (int, float)) and isinstance(
            self.asteroid_y, (int, float)
        ):
            # Represent the marker as an approximation to the search area for
            # the asteroid. Matplotlib defines the size as the area parameter.
            size = 50
            self.ax.scatter(
                self.asteroid_x,
                self.asteroid_y,
                s=size,
                marker="^",
                color="r",
                facecolors="None",
            )
            # If there is an asteroid, then the bounding box created must have
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

        print(self.asteroid_x, self.asteroid_y)
        # A tight layout to save space.
        self.figure.tight_layout()
        # And finally, drawing the image.
        self.canvas.draw()
        # All done.
        return None


def ask_user_asteroid_selector() -> tuple[float, float]:
    """Use the asteroid selector window to have the user provide the
    information needed to determine the location of the asteroid.
    
    Parameters
    ----------
    None

    Returns
    -------
    asteroid_x : float
        The location of the asteroid in the x axis direction.
    asteroid_y : float
        The location of the asteroid in the y axis direction.
    """
    # Create the asteroid selector viewer window and let the user interact with
    # it until they let the answer be found.
    asteroid_selector_window = AsteroidSelectorWindow()
    # Freeze all other processes until the location of the asteroid has been 
    # determined. This is a blocking process because everything else requires
    # this to be done.
    asteroid_selector_window.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
    asteroid_selector_window.show()
    # Using an event loop to wait until the widget closes.
    loop = QtCore.QEventLoop()
    asteroid_selector_window.destroyed.connect(loop.quit)
    loop.exec()

    # The extracted asteroid pixel location values.
    asteroid_x = asteroid_selector_window.asteroid_x
    asteroid_y = asteroid_selector_window.asteroid_y
    # All done.
    return asteroid_x, asteroid_y


if __name__ == "__main__":
    application = QtWidgets.QApplication([])

    x, y = ask_user_asteroid_selector()
    print("res",x,y)

    sys.exit()
