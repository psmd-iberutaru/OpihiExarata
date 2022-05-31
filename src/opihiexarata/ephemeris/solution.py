"""The ephemeris solution class."""

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

class EphemeriticSolution(hint.ExarataSolution):
    """This obtains the ephemeris of an asteroid using an ephemeris engine 
    provided the Keplerian orbital elements of the asteroid as determined 
    by orbital solutions.

    Attributes
    ----------
    orbital : OrbitalSolution
    ra_velocity : float
        The right ascension angular velocity of the target, in degrees per
        second.
    dec_velocity : float
        The declination angular velocity of the target, in degrees per
        second.
    """