.. _technical-algorithms-photometric-zero-point:

======================
Photometric Zero Point
======================

The primary result of a photometric solution is the detector zero point. 
It relates the magnitude of a star or other object in a given band to the 
DN counts of an object. It is given by:

.. math::

    m = 100^\frac{1}{5} \log_{10} \left( \frac{D}{t} \right) + Z_p 

Where :math:`m` is the magnitude of an object which has a total integrated
signal of :math:`D` over some time :math:`t`. The magnitude zero point is 
given by :math:`Z_p`. (The multiplicative constant is 
:math:`100^\frac{1}{5} \approx 2.51189`.)

We can reverse this calculation by consulting a photometric database. The 
photometric database gives us the magnitudes for a given band and we can 
use aperture photometry to determine the total counts of the objects.

This way, we can calculate an average zero point value :math:`Z_p` which can 
be used for other photometric calculations. We use medians to avoid issues 
with outliers. The zero-point itself also has an error of :math:`Z_e` as 
determined from the variation between the different calculated zero-point 
values from each photometric star.

Specifically for our collective set of zero points :math:`\mathbf{Z} = {{Z_{p,1}, {Z_{p,2}, ...}`, we have our averaged zero point given by the median:

.. math::

    Z_p = \text{median}(\mathbf{Z})

And the error on the average provided by the standard error of the median. To 
avoid possible contamination from outliers in either the observations or the 
photometric database, we estimate the deviation using the median absolute 
deviation, thus (for :math:`n` being the total number of observations)...

.. math::

    \sigma_{Z_p} = \frac{1}{n} \text{MAD}(\mathbf{Z}) 

Important considerations must be taken to remove overly bright and overly dim 
objects. These otherwise skew the zero point measurement because of saturation
or noise effects.


Calculating Magnitude
=====================

Once the zero-point :math:`Z_p` and its error :math:`Z_e` is determined, the 
original equation as provided above, can be used to determine the photometric 
magnitude of stars or other targets using PSF photometry.

Provided the counts (integrated over some time :math:`t`) of the target which the magnitude is to be determined as :math:`F`, and the error to be 
:math:`E = \sqrt{F}` as per Poisson statistics, the magnitude is given as: 

.. math::

    m = - 100^\frac{1}{5} \log_{10} \left( \frac{D}{t} \right) + Z_p 

Propagating the errors, we have that the error in the magnitude :math:`m_\sigma` 
(or rather its variance :math:`m_\sigma^2`) is given by:

.. math::

    m_\sigma^2 = \left( 100^\frac{1}{5} \frac{\sqrt{F}}{F \ln 10} \right)^2 + Z_e^2 + \sigma_{F,Z_p}

We assume that the covariance between :math:`F` and :math:`Z_p` is 
:math:`\sigma_{F,Z_p} = 0`. The propagated error itself, is of course 
:math:`m_\sigma = \sqrt{m_\sigma^2}`.


Filtering Considerations
========================

We account for overly bright and overly dim stars and other problematic 
targets by filtering the results from the photometric database 
(the PhotometryEngine). We describe the methods that we use to filter the 
inappropriate stars. Configuring these methods can be done by tuning their 
corresponding configuration files.

Limiting by Magnitude
---------------------

We limit the stars considered for calculating the zero point based on 
magnitude. If a star has a filter magnitude (as determined by the 
photometric database) exceeding :math:`m_\text{max}`, then it is not included
in the determination of the zero point. They are excluded from the set which 
when averaged determines the zero point and its errors.

(To "exceed" a filter magnitude, the magnitude must be less than the reference 
one because magnitudes are a backwards system.)
