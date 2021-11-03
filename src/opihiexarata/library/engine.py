"""Where the base classes of the engines lie."""

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

class ExarataEngine:
    """The base class for all of the engines which power the interfaces for 
    the OpihiExarata system. This should not used for anything other than 
    type hinting and subclassing."""
    def __init__(self):
        raise error.DevelopmentError(
            "This is a base engine class. The {engine} class should only be used for type hinting and subclassing.".format(engine=self.__class__)
        )

class AstrometryEngine(ExarataEngine):
    """The base class where the Astrometry engines are derived from. Should
    not be used other than for type hinting and subclassing."""
class PhotometricEngine(ExarataEngine):
    """The base class where the Photometric engines are derived from. Should
    not be used other than for type hinting and subclassing."""