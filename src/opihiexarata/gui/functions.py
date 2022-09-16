"""Where helpful functions which otherwise do not belong in the library, 
for the GUIs, exist."""

import os

import matplotlib.pyplot as plt

from PySide6 import QtCore, QtWidgets, QtGui

import opihiexarata
import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

import opihiexarata.astrometry as astrometry
import opihiexarata.photometry as photometry
import opihiexarata.propagate as propagate
import opihiexarata.orbit as orbit
import opihiexarata.ephemeris as ephemeris


def apply_window_icon(
    window: hint.Union[hint.widget, hint.window], icon_path: str = None
) -> None:
    """This function just applies the window icon to the GUI interfaces.
    We break it out as a function so that it is much easier to change the
    window icons uniformly.

    Parameters
    ----------
    window : QtWidget, QtMainWindow
        The window which the image will be applied to.
    icon_path : str, default = None
        The path of the icon file. If None, then we default to the
        ``window_icon.png`` file in the qtui directory.

    Returns
    -------
    None
    """
    if icon_path is not None:
        icon_path = os.path.abspath(icon_path)
    else:
        self_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = library.path.merge_pathname(
            directory=[self_dir, "qtui"], filename="window_icon", extension="png"
        )
    # We set the window icon.
    window.setWindowIcon(QtGui.QIcon(icon_path))
    # All done.
    return None


def get_busy_image_array() -> hint.array:
    """This function gets the busy image and returns it in the form of a
    color array which can be plot with matplotlib. The image file is stored
    as per convention.

    Parameters
    ----------
    None

    Returns
    -------
    busy_image : array
        The image array which is the busy image.
    """
    # Getting the busy file image.
    self_dir = os.path.dirname(os.path.abspath(__file__))
    busy_image_path = library.path.merge_pathname(
        directory=[self_dir, "qtui"], filename="busy_image_pyukumuku", extension="png"
    )
    busy_image = plt.imread(busy_image_path)
    return busy_image


def pick_engine_class_from_name(
    engine_name: str, engine_type: hint.ExarataEngine = library.engine.ExarataEngine
) -> hint.ExarataEngine:
    """This returns a specific engine class provided its user friendly name.
    This is a convince function for both development and implementation.

    If an engine name provided is not present, this raises. This is not a
    matter of conversion because user friendly names are specific

    Parameters
    ----------
    engine_name : str
        The engine name, the user friendly version. It is case insensitive.
    engine_type : ExarataEngine
        The engine subtype, if not provided, then it searches through all
        available implemented engines.

    Returns
    -------
    engine_class : ExarataEngine
        The more specific engine class based on the engine name.
    """
    # Making the engine entry case insensitive.
    engine_name = str(engine_name).casefold()

    # Defining all of the implemented engines and their names.
    astrometry_engines = {
        "astrometry.net nova": astrometry.AstrometryNetWebAPIEngine,
    }
    photometry_engines = {
        "pan-starrs 3pi dr2 mast": photometry.PanstarrsMastWebAPIEngine,
    }
    orbit_engines = {
        "orbfit": orbit.OrbfitOrbitDeterminerEngine,
        "custom orbit": orbit.CustomOrbitEngine,
    }
    ephemeris_engines = {
        "jpl horizons": ephemeris.JPLHorizonsWebAPIEngine,
    }
    propagate_engines = {
        "linear": propagate.LinearPropagationEngine,
        "quadratic": propagate.QuadraticPropagationEngine,
    }

    # If the user provided a specific engine type to use.
    if engine_type == library.engine.AstrometryEngine:
        engine_dict_list = [astrometry_engines]
    elif engine_type == library.engine.PhotometryEngine:
        engine_dict_list = [photometry_engines]
    elif engine_type == library.engine.OrbitEngine:
        engine_dict_list = [orbit_engines]
    elif engine_type == library.engine.EphemerisEngine:
        engine_dict_list = [ephemeris_engines]
    elif engine_type == library.engine.PropagationEngine:
        engine_dict_list = [propagate_engines]
    elif issubclass(engine_type, library.engine.ExarataEngine):
        # Just search through all of them.
        engine_dict_list = [
            astrometry_engines,
            photometry_engines,
            orbit_engines,
            ephemeris_engines,
            propagate_engines,
        ]
    else:
        raise error.InputError(
            "The engine type provided to narrow down the search space is not a valid"
            " ExarataEngine."
        )

    # Searching through all of the engines to find the right one.
    for dictdex in engine_dict_list:
        for namedex, enginedex in dictdex.items():
            if engine_name == namedex:
                return enginedex
            else:
                # Not the found name.
                continue

    # If the loop did not break, then it likely means that no engine has been
    # found which matches the name provided.
    raise error.InputError(
        "There is no engine of the name `{n}` that matches any implemented engine of"
        " the `{t}` class.".format(n=engine_name, t=engine_type)
    )
    # All done.
    return None
