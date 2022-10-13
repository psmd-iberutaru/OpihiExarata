"""These are redefinitions and wrapping variables for type hints. Its purpose 
is for just uniform hinting types.

This should only be used for types which are otherwise not native and would
require an import, including the typing module. The whole point of this is to
be a central collection of types for the purpose of type hinting.

This module should never be used for anything other than hinting. Use proper
imports to access these classes. Otherwise, you will likely get circular 
imports and other nasty things.
"""

from typing import *
from collections import *
from collections.abc import *

from argparse import ArgumentParser, Namespace

from astropy.io.fits import Header, FITS_rec
from astropy.table import Table, Row
from astropy.wcs import WCS

from matplotlib.backend_bases import MouseEvent

from subprocess import CompletedProcess

# Arrays. This is done because ArrayLike casts a rather larger union
# documentation.
from numpy import ndarray
from numpy.typing import ArrayLike, DTypeLike

array = ndarray

# The windows.
from PySide6 import QtCore, QtWidgets, QtGui

widget = QtWidgets.QWidget
window = QtWidgets.QMainWindow

# Importing the engines and the solutions. It is important that all other
# third-party type definitions are before this to prevent circular imports.
from opihiexarata.library.engine import *
from opihiexarata.astrometry.solution import AstrometricSolution
from opihiexarata.photometry.solution import PhotometricSolution
from opihiexarata.orbit.solution import OrbitalSolution
from opihiexarata.ephemeris.solution import EphemeriticSolution
from opihiexarata.propagate.solution import PropagativeSolution

# And the solutions themselves.
from opihiexarata.opihi.preprocess import OpihiPreprocessSolution
from opihiexarata.opihi.solution import OpihiSolution
from opihiexarata.opihi.database import OpihiZeroPointDatabaseSolution
