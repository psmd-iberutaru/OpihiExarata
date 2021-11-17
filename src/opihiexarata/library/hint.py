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
from astropy.table import Table
from astropy.wcs import WCS
from numpy.typing import ArrayLike, DTypeLike

# Importing the engines and the solutions.
from opihiexarata.library.engine import *
from opihiexarata.astrometry.solution import AstrometricSolution
from opihiexarata.photometry.solution import PhotometricSolution