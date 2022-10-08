import sys
import os
import copy

import numpy as np

from PySide6 import QtCore, QtWidgets, QtGui

import matplotlib.patches as mpl_patches
import matplotlib.pyplot as plt

# Using Qt backends.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

import opihiexarata.gui as gui


class TargetSelectorWindow(QtWidgets.QWidget):
    """This is the general class for the target selector window. The whole
    purpose of this class is for the ease of finding an asteroid.

    The GUI attribute elements are too numerous to list.

    Attributes
    ----------
    current_filename : string
        The fits filename of the image which the position of the asteroid is
        going to be derived from.
    current_header : Header
        The fits header of the current fits image file.
    current_data : array
        The data of the of the current fits image file.
    reference_filename : string
        The fits filename of the image which is used to serve as an image to
        compare the current one to so that the asteroid is easier to find.
    reference_header : Header
        The fits header of the reference fits image file.
    reference_data : array
        The fits data of the reference fits image file.
    subtract_none : array
        The data after the comparison operation of doing nothing was applied.
        This serves mostly as a cache so that it only needs to be computed
        once.
    subtract_sidereal : array
        The data after the comparison operation of subtracting the two images.
        This serves mostly as a cache so that it only needs to be computed
        once.
    subtract_non_sidereal : array
        The data after the comparison operation of doing shifting then
        subtracting the two images. This serves mostly as a cache so that it
        only needs to be computed once. The non-sidereal rates of the
        current image are used.
    target_x : float
        The x pixel location of the asteroid in the current image.
    target_y : float
        The y pixel location of the asteroid in the current image.
    subtraction_method : string
        The method of subtraction (comparison) between the current image and
        the reference image.
    autoscale_1_99 : bool
        A flag to determine if, after every operation, the data's color bars
        should be scaled so that it is 1 - 99%, a helpful scaling.
    plotted_data : array
        The data as is plotted in the GUI.
    colorbar_scale_low : float
        The lower value for which the color bar determines as its 0, the lowest
        color value.
    colorbar_scale_high : float
        The higher value for which the color bar determines as its 1, the
        highest color value.
    opihi_figure : Figure
        The matplotlib figure class of the displayed image in the GUI.
    opihi_axes : Axes
        The matplotlib axes class of the displayed image in the GUI.
    opihi_canvas : FigureCanvasQTAgg
        The matplotlib canvas class of the displayed image in the GUI. This
        uses matplotlib's built-in Qt support.
    opihi_nav_toolbar : NavigationToolbar2QT
        The matplotlib navigation bar class of the displayed image in the
        GUI. This uses matplotlib's built-in Qt support.
    _opihi_coordinate_formatter : CoordinateFormatter
        A class to wrap around the imshow formatter for fancy printing.
    """

    def __init__(
        self, current_fits_filename: str, reference_fits_filename: str = None
    ) -> None:
        """Create the target selector window. Though often used for asteroids,
        there is no reason why is should specific to them; so we use a general
        name.

        Parameters
        ----------
        current_fits_filename : string
            The current fits filename which will be used to determine where the
            location of the target is.
        reference_fits_filename : string, default = None
            The reference fits filename which will be used to compare against the
            current fits filename to determine where the location of the target
            is. If None, then no image will be loaded until manually specified.

        Returns
        -------
        None
        """
        # Creating the GUI itself using the Qt framework and the converted
        # Qt designer files.
        super(TargetSelectorWindow, self).__init__()
        self.ui = gui.qtui.Ui_SelectorWindow()
        self.ui.setupUi(self)
        # Window icon, we use the default for now.
        gui.functions.apply_window_icon(window=self, icon_path=None)

        # Window design parameters, just for show.
        self.setWindowTitle("OpihiExarata Target Selector")

        # The data from which will be shown to the user which they will use
        # to find the location of the target.
        current_header, current_data = library.fits.read_fits_image_file(
            filename=current_fits_filename
        )
        self.current_filename = current_fits_filename
        self.current_header = current_header
        self.current_data = current_data
        # The reference data, if the fits file has been provided. Need to
        # take into account if the reference filename is not provided.
        if isinstance(reference_fits_filename, str) and os.path.isfile(
            reference_fits_filename
        ):
            reference_header, reference_data = library.fits.read_fits_image_file(
                filename=reference_fits_filename
            )
            self.reference_filename = str(reference_fits_filename)
            self.reference_header = reference_header
            self.reference_data = reference_data
        else:
            # No data has been provided, just using sensible defaults.
            self.reference_filename = str(reference_fits_filename)
            self.reference_header = current_header.copy()
            self.reference_data = np.zeros_like(self.current_data)
        # Precompute the translated image array values to ensure the
        # cache speedup and subtraction capability.
        self._recompute_subtraction_arrays()

        # The location of the target, the user did not provide it so
        # blank currently.
        self.target_x = None
        self.target_y = None

        # There is currently no subtraction method provided. We assume
        # no subtraction so that the image can be shown. (Both None the type
        # and the string is valid as no subtraction. The type just means
        # that it has not been formally specified using the GUI.)
        self.subtraction_method = None

        # The data, as it is plotted. This will change with different
        # subtraction methodology. But, as the subtraction is defined as None,
        # the current data is fine.
        self.plotted_data = np.array(self.current_data)

        # We default the scale to the 1-99 automatic linear scale. It is
        # just an easier system and it makes the user think of it as a default.
        low, high = np.percentile(self.plotted_data, [1, 99])
        self.colorbar_scale_low = float(low)
        self.colorbar_scale_high = float(high)

        # Making the plot itself.
        self.__init_opihi_image()

        # Adding the GUI connections.
        self.__init_gui_connections()

        # Redrawing the window before finishing up.
        self.refresh_window()

        # All done.
        return None

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
        dpi = self.logicalDpiY()
        pix_to_in = lambda p: p / dpi
        dummy_edge_size_px = self.ui.dummy_selector_image.maximumHeight()
        edge_size_in = pix_to_in(dummy_edge_size_px)

        # The figure, canvas, and navigation toolbar of the image plot
        # using a Matplotlib Qt widget backend. We will add these to the
        # layout later.
        fig, ax = plt.subplots(figsize=(edge_size_in, edge_size_in), constrained_layout=True)
        self.opihi_figure = fig
        self.opihi_axes = ax
        self.opihi_canvas = FigureCanvas(self.opihi_figure)
        self.opihi_nav_toolbar = NavigationToolbar(self.opihi_canvas, self)
        # The flag for determining if autoscaling should always be applied.
        # The default, from Qt, is False.
        self.autoscale_1_99 = False

        # For ease of usage, a custom navigation bar coordinate formatter
        # function/class is used.
        class CoordinateFormatter:
            """A simple function class to properly format the navigation bar
            coordinate text. This assumes the current structure of the GUI."""

            def __init__(self, gui_instance: TargetSelectorWindow) -> None:
                self.gui_instance = gui_instance
                return None

            def __call__(self, x, y) -> str:
                """The coordinate string going to be put onto the navigation
                bar."""
                # The pixel locations.
                x_index = int(x)
                y_index = int(y)
                x_coord_string = "{x_int:d}".format(x_int=x_index)
                y_coord_string = "{y_int:d}".format(y_int=y_index)
                # Extracting the data.
                try:
                    z_float = self.gui_instance.plotted_data[y_index, x_index]
                except AttributeError:
                    # There is no data to index.
                    z_coord_string = "NaN"
                except IndexError:
                    # The mouse is just outside of the boundary.
                    z_coord_string = "NaN"
                else:
                    # Parse the string from the number provided.
                    z_coord_string = "{z_flt:.2f}".format(z_flt=z_float)

                # Compiling it all together.
                coord_string = "[{x_str}, {y_str}] = {z_str}".format(
                    x_str=x_coord_string, y_str=y_coord_string, z_str=z_coord_string
                )
                return coord_string

        # Assigning the coordinate formatter derived.
        self._opihi_coordinate_formatter = CoordinateFormatter(self)
        self.opihi_axes.format_coord = self._opihi_coordinate_formatter

        # Setting the layout, it is likely better to have the toolbar below
        # rather than above to avoid conflicts with the reset buttons in the
        # event of a mis-click.
        self.ui.vertical_layout_image.addWidget(self.opihi_canvas)
        self.ui.vertical_layout_image.addWidget(self.opihi_nav_toolbar)

        # Setting the size of the canvas to be more representative of the 
        # designer file.
        self.opihi_canvas.setMinimumHeight(dummy_edge_size_px)
        self.opihi_canvas.setMaximumHeight(dummy_edge_size_px)
        self.opihi_canvas.setMinimumWidth(dummy_edge_size_px)
        self.opihi_canvas.setMaximumWidth(dummy_edge_size_px)
        # And setting the navigation bar.
        self.opihi_nav_toolbar.setMaximumWidth(dummy_edge_size_px)

        # Remove the dummy spacers otherwise it is just extra unneeded space.
        self.ui.vertical_layout_image.removeWidget(self.ui.dummy_selector_image)
        self.ui.vertical_layout_image.removeWidget(self.ui.dummy_selector_navbar)
        self.ui.dummy_selector_image.hide()
        self.ui.dummy_selector_navbar.hide()
        self.ui.dummy_selector_image.deleteLater()
        self.ui.dummy_selector_navbar.deleteLater()
        del self.ui.dummy_selector_image
        del self.ui.dummy_selector_navbar
        # A little hack to ensure the default zoom limits that are saved when
        # redrawing the figure is not 0-1 in both x and y but instead the image
        # itself.
        self.opihi_axes.set_xlim(0, self.current_data.shape[1])
        self.opihi_axes.set_ylim(0, self.current_data.shape[0])
        # Redraw the image.
        self.refresh_window()
        return None

    def __init_gui_connections(self):
        """A initiation set of functions that attach to the buttons on the
        GUI.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # The connections for the fits file selection.
        self.ui.push_button_change_reference_filename.clicked.connect(
            self.__connect_push_button_change_reference_filename
        )

        # The figure connections for dragging of the search box. The Opihi
        # image initialization should be done first.
        self.opihi_canvas.mpl_connect(
            "button_press_event", self.__connect_matplotlib_mouse_press_event
        )
        self.opihi_canvas.mpl_connect(
            "button_release_event", self.__connect_matplotlib_mouse_release_event
        )

        # The subtraction method connections for comparing the current
        # and release fits images. These buttons really just set the
        # subtraction method flag.
        self.ui.push_button_mode_none.clicked.connect(
            self.__connect_push_button_mode_none
        )
        self.ui.push_button_mode_reference.clicked.connect(
            self.__connect_push_button_mode_reference
        )
        self.ui.push_button_mode_sidereal.clicked.connect(
            self.__connect_push_button_mode_sidereal
        )
        self.ui.push_button_mode_non_sidereal.clicked.connect(
            self.__connect_push_button_mode_non_sidereal
        )

        # The scale and colorbar connections for determining the scale and
        # color bar information, along with the automatic way.
        self.ui.line_edit_dynamic_scale_low.editingFinished.connect(
            self.__connect_line_edit_dynamic_scale_low
        )
        self.ui.line_edit_dynamic_scale_high.editingFinished.connect(
            self.__connect_line_edit_dynamic_scale_high
        )
        self.ui.push_button_scale_1_99.clicked.connect(
            self.__connect_push_button_scale_1_99
        )
        self.ui.check_box_autoscale_1_99.stateChanged.connect(
            self.__connect_check_box_autoscale_1_99
        )

        # The pixel location submission button connection.
        self.ui.push_button_submit_target.clicked.connect(
            self.__connect_push_button_submit_target
        )

        return None

    def __connect_push_button_change_reference_filename(self) -> None:
        """This function provides a popup dialog to prompt the user to change
        the reference fits filename.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # We assume, as a good jumping off point, that the reference filename
        # is in the same directory as the current image.
        current_image_directory = library.path.get_directory(
            pathname=self.current_filename
        )
        # Use the build-in OS dialog box.
        new_reference_filename, __ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Open New Reference Opihi Image",
            dir=current_image_directory,
            filter="FITS Files (*.fits)",
        )
        # If no file was provided, then there is nothing to do.
        if os.path.isfile(new_reference_filename):
            # Extracted the needed information provided this new fits file.
            reference_header, reference_data = library.fits.read_fits_image_file(
                filename=new_reference_filename
            )
            self.reference_filename = new_reference_filename
            self.reference_header = reference_header
            self.reference_data = reference_data
        else:
            # Nothing to do.
            pass

        # Precompute the translated image array values to ensure the
        # cache speedup and subtraction capability.
        self._recompute_subtraction_arrays()
        # Redraw and refresh the window to use this new updated information.
        self.refresh_window()
        return None

    def __connect_matplotlib_mouse_press_event(self, event: hint.MouseEvent) -> None:
        """A function to describe what would happen when a mouse press is
        done on the Matplotlib image.

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
        if self.opihi_nav_toolbar.mode.value != "":
            # We proxy the middle button and left mouse button together for 
            # zooming. We just allow it in addition. This is a band aid 
            # solution.
            if event.button == 2 and self.opihi_nav_toolbar.mode.value == "zoom rect":
                event.button = 1
                self.opihi_nav_toolbar.press_zoom(event=event)
            return None

        # If the button click was from the middle mouse button, a box is
        # being drawn for defining the box of the asteroid.
        if event.button == 2:
            # Assign the potential location of the target to the location
            # of the mouse.
            if event.xdata is None or event.ydata is None:
                # The user likely clicked outside of the canvas area. Ignore.
                pass
            else:
                # One of the bounds of the search rectangle.
                self.box_search_x0 = float(event.xdata)
                self.box_search_y0 = float(event.ydata)
        return None

    def __connect_matplotlib_mouse_release_event(self, event: hint.MouseEvent) -> None:
        """A function to describe what would happen when a mouse press is
        released done on the Matplotlib image.

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
        if self.opihi_nav_toolbar.mode.value != "":
            # We proxy the middle button and left mouse button together for 
            # zooming. This is a band aid solution.
            if event.button == 2 and self.opihi_nav_toolbar.mode.value == "zoom rect":
                event.button = 1
                self.opihi_nav_toolbar.release_zoom(event=event)
            return None


        # If the button click was from the middle mouse button, a box is
        # being drawn for defining the box of the asteroid.
        if event.button == 2:
            # Assign the potential location of the target to the location
            # of the mouse.
            if event.xdata is None or event.ydata is None:
                # The user likely clicked outside of the canvas area. Ignore.
                pass
            else:
                # One of the bounds of the search rectangle.
                self.box_search_x1 = float(event.xdata)
                self.box_search_y1 = float(event.ydata)
            # By convention, the x0 <= x1 and vice versa for y. If the user drew
            # a backwards square, then we fix it here.
            if self.box_search_x1 < self.box_search_x0:
                lower_x = min([self.box_search_x0, self.box_search_x1])
                upper_x = max([self.box_search_x0, self.box_search_x1])
                self.box_search_x0 = lower_x
                self.box_search_x1 = upper_x
            if self.box_search_y1 < self.box_search_y0:
                lower_y = min([self.box_search_y0, self.box_search_y1])
                upper_y = max([self.box_search_y0, self.box_search_y1])
                self.box_search_y0 = lower_y
                self.box_search_y1 = upper_y
            # Find the target location based on the search area just determined.
            self.target_x, self.target_y = self.find_target_location(
                x0=self.box_search_x0,
                x1=self.box_search_x1,
                y0=self.box_search_y0,
                y1=self.box_search_y1,
            )

        # Redrawing the image to have the location be visible.
        self.refresh_window()
        return None

    def __connect_push_button_mode_none(self) -> None:
        """This function sets the subtraction method to None, for comparing
        the current image from the reference image.

        Both None the type and the string is valid as no subtraction. The
        type just means that it has not been formally specified using the GUI.

        This method has no subtraction and thus no comparison to the reference
        image.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # As the mode is being set by the GUI, we use the string form.
        self.subtraction_method = "none"
        # Because the subtraction mode changed, the data which is used to plot
        # should also be changed.
        self.plotted_data = self.subtract_none
        # Refresh the window because the method changed.
        self.refresh_window()
        return None

    def __connect_push_button_mode_reference(self) -> None:
        """This function sets the subtraction method to Reference, plotting
        the reference image instead of the current image.

        This method has no subtraction and thus no comparison to the current
        image.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # As the mode is being set by the GUI, we use the string form.
        self.subtraction_method = "reference"
        # Because the subtraction mode changed, the data which is used to plot
        # should also be changed.
        self.plotted_data = self.subtract_reference
        # Refresh the window because the method changed.
        self.refresh_window()
        return None

    def __connect_push_button_mode_sidereal(self) -> None:
        """This function sets the subtraction method to sidereal, for comparing
        the current image from the reference image.

        This method assumes the approximation that both the current and
        reference images are pointing to the same point in the sky.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Setting the mode to sidereal.
        self.subtraction_method = "sidereal"
        # Because the subtraction mode changed, the data which is used to plot
        # should also be changed.
        self.plotted_data = self.subtract_sidereal
        # Refresh the window because the method changed.
        self.refresh_window()
        return None

    def __connect_push_button_mode_non_sidereal(self) -> None:
        """This function sets the subtraction method to non-sidereal, for
        comparing the current image from the reference image.

        This method assumes the approximation that the target itself did not
        move at all compared to both images, but the stars do as they are
        moving siderally.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Setting the mode to non-sidereal.
        self.subtraction_method = "non-sidereal"
        # Because the subtraction mode changed, the data which is used to plot
        # should also be changed.
        self.plotted_data = self.subtract_non_sidereal
        # Refresh the window because the method changed.
        self.refresh_window()
        return None

    def __connect_line_edit_dynamic_scale_low(self) -> None:
        """A function to operate on the change of the text of the low scale.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Saving the old lower bound scale value in the event that the text
        # entered cannot be properly converted.
        old_low_value = copy.deepcopy(self.colorbar_scale_low)

        # Try to get the new value.
        try:
            # Extracting the value the user provided in the text block.
            input_text = self.ui.line_edit_dynamic_scale_low.text()
            new_low_value = float(input_text)
        except Exception:
            # Something is wrong, the value entered is a valid entry; reverting
            # back to the defaults.
            new_low_value = old_low_value
        finally:
            self.colorbar_scale_low = new_low_value

        # If maximum value is less than the minimum value, it is likely the
        # user swapped them by mistake. We correct for the swapping here.
        if self.colorbar_scale_high <= self.colorbar_scale_low:
            # Storing to swap...
            raw_low = self.colorbar_scale_low
            raw_high = self.colorbar_scale_high
            # ...and swap.
            self.colorbar_scale_low = raw_high
            self.colorbar_scale_high = raw_low

        # Redraw the image with this new low colorbar. (Refreshing the
        # image itself is likely fine too.)
        self.refresh_window()
        # All done.
        return None

    def __connect_line_edit_dynamic_scale_high(self) -> None:
        """A function to operate on the change of the text of the high scale.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Saving the old higher bound scale value in the event that the text
        # entered cannot be properly converted.
        old_high_value = copy.deepcopy(self.colorbar_scale_high)

        # Try to get the new value.
        try:
            # Extracting the value the user provided in the text block.
            input_text = self.ui.line_edit_dynamic_scale_high.text()
            new_high_value = float(input_text)
        except Exception:
            # Something is wrong, the value entered is a valid entry; reverting
            # back to the defaults.
            new_high_value = old_high_value
        finally:
            self.colorbar_scale_high = new_high_value

        # If maximum value is less than the minimum value, it is likely the
        # user swapped them by mistake. We correct for the swapping here.
        if self.colorbar_scale_high <= self.colorbar_scale_low:
            # Storing to swap...
            raw_low = self.colorbar_scale_low
            raw_high = self.colorbar_scale_high
            # ...and swap.
            self.colorbar_scale_low = raw_high
            self.colorbar_scale_high = raw_low

        # Redraw the image with this new low colorbar. (Refreshing the
        # image itself is likely fine too.)
        self.refresh_window()
        # All done.
        return None

    def __connect_push_button_scale_1_99(self) -> None:
        """A function set the scale automatically to 1-99 within the
        region currently displayed on the screen.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # We can autoscale to these values by recomputing the colorbar values.
        self._recompute_colorbar_autoscale(lower_percentile=1, higher_percentile=99)
        # Redraw the image with this new colorbar range. (Refreshing the
        # image itself is likely fine too.)
        self.refresh_window()
        # All done.
        return None

    def __connect_check_box_autoscale_1_99(self) -> None:
        """This check box allows the user to force the autoscaling of images
        when the subtraction method changes.

        Parameters
        ----------
        None

        Return
        ------
        None
        """
        # Get the state of the check box.
        checkbox_state = self.ui.check_box_autoscale_1_99.isChecked()
        # As the mode is being set by the GUI, we use the string form.
        self.autoscale_1_99 = bool(checkbox_state)
        # Because this checkbox itself is expected to trigger scaling as well.
        if self.autoscale_1_99:
            self._recompute_colorbar_autoscale(lower_percentile=1, higher_percentile=99)
        # Refresh the window because the scaling has changed.
        self.refresh_window()
        return None

    def __connect_push_button_submit_target(self) -> None:
        """This button submits the current location of the target and closes
        the window. (The target information is saved within the class
        instance.)

        If the text within the line edits differ than what the box selection
        has selected, then this prioritizes the values as manually defined.
        Although this should be rare as any time a box is drawn, the values
        and text boxes should be updated.

        If no entry is properly convertible, we default to center of the image.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # The pixel locations as derived from the box mode.
        box_pixel_x = self.target_x
        box_pixel_y = self.target_y
        # The pixel locations as derived from the text entry. If they can
        # be converted into actual pixel locations, we prioritize them.

        try:
            entry_pixel_x = float(self.ui.line_edit_dynamic_target_x.text())
            entry_pixel_y = float(self.ui.line_edit_dynamic_target_y.text())
        except Exception:
            # The conversion cannot happen, the entry provided is not a valid
            # entry, going to use the box values instead.
            using_pixel_x = box_pixel_x
            using_pixel_y = box_pixel_y
        else:
            # Prioritizing the entered values.
            using_pixel_x = entry_pixel_x
            using_pixel_y = entry_pixel_y
        finally:
            # Type checking the currently assumed pixel values.
            if isinstance(using_pixel_x, (int, float)) and isinstance(
                using_pixel_y, (int, float)
            ):
                # The pixel values provided either through manual or box entry
                # is valid; prioritization has already been done.
                pass
            else:
                # The currently derived values are incorrect. Falling back on
                # an assumption of the beyond the origin to signify that it
                # was not provided while still giving a numerical value to
                # work with.
                using_pixel_x = -1
                using_pixel_y = -1

        # The target values updated to reflect this prioritization and
        # conversation.
        self.target_x = using_pixel_x
        self.target_y = using_pixel_y
        # All done, closing the window as we can now let the primary part of
        # the program continue.
        self.close_window()
        return None

    def refresh_window(self) -> None:
        """Refresh the text content of the window given new information.
        This refreshes both the dynamic label text and redraws the image.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Rewriting the text...
        self.__refresh_image()
        # ...redrawing the image plot...
        self.__refresh_text()
        # All done.
        return None

    def __refresh_image(self) -> None:
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
        xmin, xmax = self.opihi_axes.get_xlim()
        ymin, ymax = self.opihi_axes.get_ylim()

        # If the user has set for autoscaling, then we apply the default
        # 1-99 % autoscaling. This must be done before the figure it cleared
        # before redrawing else it computes it from a single pixel image.
        if self.autoscale_1_99:
            self._recompute_colorbar_autoscale(lower_percentile=1, higher_percentile=99)

        # This is a function to replace the coordinate formatting in
        # favor of our own.
        def empty_string(string: str) -> str:
            return str()

        # Clearing the axes, starting fresh and anew as this entire function
        # does a whole redraw. It may not be needed but small performance
        # hit to ensure it all works normally.
        self.opihi_axes.clear()

        # Customizing the colorbar of our plotting image to match what the
        # current values are set at.
        image = self.opihi_axes.imshow(
            self.plotted_data,
            cmap="gray",
            vmin=self.colorbar_scale_low,
            vmax=self.colorbar_scale_high,
            zorder=-1,
        )
        # Disable their formatting in favor of ours.
        image.format_cursor_data = empty_string

        # If there is a specified target location, put it on the map.
        if isinstance(self.target_x, (int, float)) and isinstance(
            self.target_y, (int, float)
        ):
            # Represent the marker as the targets location as defined by the
            # search box and the target finding function.
            MARKER_SIZE = float(
                library.config.GUI_SELECTOR_IMAGE_PLOT_TARGET_MARKER_SIZE
            )
            self.opihi_axes.scatter(
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
                xy=(self.box_search_x0, self.box_search_y0),
                width=self.box_search_x1 - self.box_search_x0,
                height=self.box_search_y1 - self.box_search_y0,
                facecolor="None",
                edgecolor="b",
            )
            self.opihi_axes.add_patch(search_rectangle)
        else:
            # No need, there is no current valid location specified.
            pass

        # Reinstate the zoom and pan settings via the previous limits.
        self.opihi_axes.set_xlim(xmin, xmax)
        self.opihi_axes.set_ylim(ymin, ymax)
        # Make sure the coordinate formatter does not change.
        self.opihi_axes.format_coord = self._opihi_coordinate_formatter
        # And finally, drawing the image.
        self.opihi_canvas.draw()
        # All done.
        return None

    def __refresh_text(self) -> None:
        """This function just refreshes the GUI text based on the current
        actual values.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Refreshing the current and reference fits filenames. No directory
        # information.
        current_bare_filename = library.path.get_filename_with_extension(
            pathname=self.current_filename
        )
        reference_bare_filename = library.path.get_filename_with_extension(
            pathname=self.reference_filename
        )
        self.ui.label_dynamic_current_fits_filename.setText(current_bare_filename)
        self.ui.label_dynamic_reference_fits_filename.setText(reference_bare_filename)

        # Refreshing the scale value text as set. Formatting the numerical
        # values into strings.
        scale_low_str = "{lo:.5f}".format(lo=self.colorbar_scale_low)
        scale_high_str = "{hi:.5f}".format(hi=self.colorbar_scale_high)
        self.ui.line_edit_dynamic_scale_low.setText(scale_low_str)
        self.ui.line_edit_dynamic_scale_high.setText(scale_high_str)

        # Refreshing the target pixel location in the manual entry. Formatting
        # the numerical values into strings.
        target_x = self.target_x if self.target_x is not None else np.nan
        target_y = self.target_y if self.target_y is not None else np.nan
        target_x_str = "{x:.3f}".format(x=target_x)
        target_y_str = "{y:.3f}".format(y=target_y)
        self.ui.line_edit_dynamic_target_x.setText(target_x_str)
        self.ui.line_edit_dynamic_target_y.setText(target_y_str)

        # All done.
        return None

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
        plt.close(self.opihi_figure)
        # Close the window.
        self.close()
        return None

    def _recompute_subtraction_arrays(self) -> None:
        """This computes the subtracted arrays for both none, sidereal, and
        non-sidereal subtractions. This is done mostly for speed considerations
        as the values can be computed and stored during image loading.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Begin with computing no subtraction. This is really just the same
        # as the current data.
        self.subtract_none = self.current_data

        # The reference image mode is just the reference data without
        # any comparison to the current data.
        self.subtract_reference = self.reference_data

        # Subtracting sidereally implies that the center of the two images are
        # the same, so no translation is needed.
        self.subtract_sidereal = self.current_data - self.reference_data

        # Subtracting non-sidereally means that the centers are offset based
        # on the non-sidereal motion and time difference. We find the 
        # translation vector between the two images. Because we are shifting 
        # the reference image forward, the current data is the reference 
        # for translation.
        x_pix_change, y_pix_change = library.image.determine_translation_image_array(translate_array=self.reference_data, reference_array=self.current_data)
        # We shift the reference image forward in time as translation splines
        # and it is best not to interpolate the real data. We assume nothing
        # about the outside parts of the image, so there is no data for them.
        shifted_reference_data = library.image.translate_image_array(
            array=self.reference_data,
            shift_x=x_pix_change,
            shift_y=y_pix_change,
            pad_value=np.nan,
        )
        self.subtract_non_sidereal = self.current_data - shifted_reference_data

        # All done.
        return None

    def _recompute_colorbar_autoscale(
        self, lower_percentile: float = 1, higher_percentile: float = 99
    ) -> None:
        """This is a function to recompute the autoscaling of the colorbar.

        This function needs to be split from the connection buttons otherwise
        an infinite loop occurs because of their inherent and expected calls
        to refresh the window.

        Parameters
        ----------
        lower_percentile : float, default = 1
            The lower percentile value which will be defined at the zero point
            for the colorbar.
        higher_percentile : float, default = 99
            The higher (upper) percentile value which will be defined as the
            one point for the colorbar.

        Returns
        -------
        None
        """
        # Percentiles must be between 0 <= p <= 100.
        if not (0 <= lower_percentile <= 100 and 0 <= higher_percentile <= 100):
            raise error.InputError(
                "The percentiles given for the colorbar scaling are not between 0 and"
                " 100 as expected of percentiles."
            )

        # The subset of the data that is currently displayed on the screen.
        xmin, xmax = self.opihi_axes.get_xlim()
        ymin, ymax = self.opihi_axes.get_ylim()
        displayed_plotted_image = self.plotted_data[
            int(ymin) : int(ymax), int(xmin) : int(xmax)
        ]
        # Calculate the percentile values from this subarray as the colorbar
        # bounds. If the images was translated, there will be NaNs to deal
        # with.
        low, high = np.nanpercentile(
            displayed_plotted_image.flatten(), [lower_percentile, higher_percentile]
        )
        self.colorbar_scale_low = low
        self.colorbar_scale_high = high
        # All done.
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
        search_array = self.current_data[
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


def ask_user_target_selector_window(
    current_fits_filename, reference_fits_filename: str = None
) -> tuple[float, float]:
    """Use the target selector window to have the user provide the
    information needed to determine the location of the target.

    Parameters
    ----------
    current_fits_filename : string
        The current fits filename which will be used to determine where the
        location of the target is.
    reference_fits_filename : string, default = None
        The reference fits filename which will be used to compare against the
        current fits filename to determine where the location of the target
        is. If None, then no image will be loaded until manually specified.

    Returns
    -------
    target_x : float
        The location of the target in the x axis direction.
    target_y : float
        The location of the target in the y axis direction.
    """
    # Create the target selector viewer window and let the user interact with
    # it until they let the answer be found.
    target_selector_window = TargetSelectorWindow(
        current_fits_filename=current_fits_filename,
        reference_fits_filename=reference_fits_filename,
    )
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


def main():
    app = QtWidgets.QApplication([])

    target_x, target_y = ask_user_target_selector_window()

    application.show()
    sys.exit(app.exec())
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
