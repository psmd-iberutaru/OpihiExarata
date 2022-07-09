.. _technical-algorithms-photometric-zero-point:

======================
Photometric Zero Point
======================

The primary result of a photometric solution is the detector zero point. 
It relates the magnitude of a star or other object in a given band to the 
DN counts of an object. It is given by:

.. math::

    m = 2.5119 \log_{10} \left( \frac{D}{t} \right) + Z_p 

Where :math:`m` is the magnitude of an object which has a total integrated
signal of :math:`D` over some time :math:`t`. The magnitude zero point is 
given by :math:`Z_p`. (The actual multiplicative constant is 
:math:`100^\frac{1}{2}`.)

We can reverse this calculation by consulting a photometric database. The 
photometric database gives us the magnitudes for a given band and we can 
use aperture photometry to determine the total counts of the objects.

This way, we can calculate an average zero point value :math:`Z_p` which can 
be used for other photometric calculations. 

Important considerations must be taken to remove overly bright and overly dim 
objects. These otherwise skew the zero-point measurement because of saturation
or noise effects.