"""These are redefinitions and wrapping variables for type hints. Its purpose 
is for just uniform hinting types.

This should only be used for types which are otherwise not native and would
require an import, including the typing module. The whole point of this is to
be a central collection of types for the purpose of type hinting.
"""

from typing import *
from collections import *
from collections.abc import *

from astropy.io.fits import Header, FITS_rec
from astropy.table import Table, Row
from astropy.wcs import WCS


# Arrays. This is done because ArrayLike casts a rather larger union
# documentation.
from numpy import ndarray
from numpy.typing import ArrayLike, DTypeLike

array = ndarray

# Importing the engines and the solutions. It is important that all other
# third-party type definitions are before this to prevent circular imports.
from opihiexarata.library.engine import *
from opihiexarata.astrometry.solution import AstrometricSolution
from opihiexarata.photometry.solution import PhotometricSolution
from opihiexarata.orbit.solution import OrbitSolution
from opihiexarata.propagate import PropagationSolution
