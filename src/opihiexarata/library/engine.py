"""Where the base classes of the solvers and engines lie."""

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


# The solution classes.
class ExarataSolution:
    """The base class for all of the solution classes which use engines to
    solve particular problems."""

    def __init__(self):
        raise error.DevelopmentError(
            "This is a base solution class. The {sol} class should only be used for"
            " type hinting and subclassing.".format(sol=self.__class__)
        )


# The engine classes
class ExarataEngine:
    """The base class for all of the engines which power the interfaces for
    the OpihiExarata system. This should not used for anything other than
    type hinting and subclassing."""

    def __init__(self):
        raise error.DevelopmentError(
            "This is a base engine class. The {engine} class should only be used for"
            " type hinting and subclassing.".format(engine=self.__class__)
        )


class AstrometryEngine(ExarataEngine):
    """The base class where the Astrometry engines are derived from. Should
    not be used other than for type hinting and subclassing."""


class EphemerisEngine(ExarataEngine):
    """The base class for all of the Ephemeris determination engines. Should not
    be used other than for type hinting and subclassing."""


class OrbitEngine(ExarataEngine):
    """The base class for all of the Orbit determination engines. Should not
    be used other than for type hinting and subclassing."""


class PhotometryEngine(ExarataEngine):
    """The base class where the Photometry engines are derived from. Should
    not be used other than for type hinting and subclassing."""


class PropagationEngine(ExarataEngine):
    """The base class where the Propagation engines are derived from. Should
    not be used other than for type hinting and subclassing."""
