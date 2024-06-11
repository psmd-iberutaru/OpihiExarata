"""These are redefinitions and wrapping variables for type hints. Its purpose
is for just uniform hinting types.

This should only be used for types which are otherwise not native and would
require an import, including the typing module. The whole point of this is to
be a central collection of types for the purpose of type hinting.

This module should never be used for anything other than hinting. Use proper
imports to access these classes. Otherwise, you will likely get circular
imports and other nasty things.
"""

from argparse import ArgumentParser
from argparse import Namespace
from collections import *
from collections.abc import *
from datetime import *
from subprocess import CompletedProcess
from typing import *

from astropy.io.fits import FITS_rec
from astropy.io.fits import Header
from astropy.table import Row
from astropy.table import Table
from astropy.wcs import WCS
from matplotlib.backend_bases import MouseEvent
from numpy import generic as numpy_generic

# Arrays. This is done because ArrayLike casts a rather larger union
# documentation.
from numpy import ndarray
from numpy.typing import ArrayLike
from numpy.typing import DTypeLike

array = ndarray

# The windows.
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

widget = QtWidgets.QWidget
window = QtWidgets.QMainWindow

# Importing the engines and the solutions. It is important that all other
# third-party type definitions are before this to prevent circular imports.
from opihiexarata.astrometry.solution import AstrometricSolution
from opihiexarata.ephemeris.solution import EphemeriticSolution
from opihiexarata.library.engine import *
from opihiexarata.opihi.database import OpihiZeroPointDatabaseSolution

# And the solutions themselves.
from opihiexarata.opihi.preprocess import OpihiPreprocessSolution
from opihiexarata.opihi.solution import OpihiSolution
from opihiexarata.orbit.solution import OrbitalSolution
from opihiexarata.photometry.solution import PhotometricSolution
from opihiexarata.propagate.solution import PropagativeSolution
