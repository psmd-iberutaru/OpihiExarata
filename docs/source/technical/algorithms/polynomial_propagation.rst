.. _technical-algorithms-polynomial-propagation:

======================
Polynomial Propagation
======================

Polynomial propagation is one of the different implemented propagation engines 
(see :ref:`technical-architecture-services-engines`). Conceptually it is one 
of the easiest methods. Simply put, it just computes the rate of right 
ascension and declination change as independent rates from a collection of 
previous observations. 

The use of polynomial propagation assumes the following:

- The set of taken asteroid observations (and desired future positions) are within a relatively short timespan, usually within 24 hours.
- The tangent plane projection of the sky is valid and the effects of curvature because of the spherical sky are negligible.
- The motion of the asteroid across the sky within the provided time span is small enough such that the aforementioned tangent plane projection still holds.


Coordinate Conversion
=====================

The only required observational data for this method of propagation is the 
RA and DEC of the observations, :math:`\alpha` and :math:`\delta`, along with 
the time of observations :math:`t`. Because of the conventions of OpihiExarata
(see :ref:`technical-conventions`) the units of these are degrees and Julian 
days. (For notation purposes, the variables stand for all taken observations.)

We found that using these units for fitting the rates were inadequate and 
suffered from two different problems.

1. The Julian day time difference was often much less than one and so the fitting algorithms became unstable and could properly not fit the observations.
2. Angles are cyclical and the fitting a function to cyclical points are not stable using quick methods.

To solve the first problem, we converted the time of observations to UNIX time.
Because it is in seconds, the numerical difference between each data point is 
much larger and it seems that this change produces more accurate results. Of 
course the propagation function itself (which has Julian days as input) needs 
to covert the input date to UNIX time as the fitting constants are now in 
the UNIX time domain.

To solve the second problem, we convert the angles so that they can be treated 
linearly. More specifically, as the angular coordinates provided are between 
:math:`0 \leq \angle \leq 360` or :math:`-90 \leq \angle \leq 90`, if the 
maximum difference is (numerically) greater than :math:`\approx 135` degrees 
in either coordinate, then it guaranteed that a loop around happened for that 
coordinate. If it was motion that caused this difference, then it must have 
violated one of the assumptions and so this method is useless for propagation. 
We use the most recent observation to set the range, the other points are 
cycled until no wrap around occurs.


Fitting Coordinates
===================

We treat both :math:`\alpha` and :math:`\delta` as separate and independent
coordinates and we also treat their on-sky rates as independent of each other.
This is valid as long as the timescales are relatively small and the 
tangent plane projection of the sky holds.

As such, we have two functions :math:`A(f)` and :math:`D(f)` which is the 
path of the asteroid across the sky over time :math:`f` in right ascension 
(:math:`A`) and declination (:math:`D`).

We can approximate these functions using polynomials. We fit our :math:`n` 
order polynomial :math:`P_n` for both right ascension and declination to get 
approximations to these functions:

.. math::

    \text{fit}[P_n(t) = \alpha] \implies A(f) \approx P_{n,A}(f) \mapsto (f, \alpha) \\
    \text{fit}[P_n(t) = \delta] \implies D(f) \approx P_{n,D}(f) \mapsto (f, \delta)

Simply put, when we have a fit to the :math:`(t, \alpha)` and 
:math:`(t, \delta)` pairs using polynomial functions, we use these functions as 
approximations to :math:`A` and :math:`D` and use these approximations to 
derive the future location.

Provided the future time :math:`f` where the user wants to predict the future 
right ascension :math:`\alpha_f` and declination :math:`\delta_f`, we can 
easily compute our estimations as:

.. math::

    P_{n,A}(f) = \alpha_f \\
    P_{n,D}(f) = \delta_f

We use low order polynomials as they are simple functions to both fit and 
interpret. We implement both first order (linear) polynomial 
(:py:class:`opihiexarata.propagate.polynomial.LinearPropagationEngine`) and 
second order (quadratic) polynomial 
(:py:class:`opihiexarata.propagate.polynomial.QuadraticPropagationEngine`). 
Higher order polynomials and more complicated functions often over-fit (and 
are otherwise overcomplicated) as typically there are only a few observations 
and thus few :math:`(\alpha, \delta, t)` sets for fitting.

Wrap Around
-----------

In some cases, the approximate angular coordinates given by :math:`P_{n,A}(f)`
and :math:`P_{n,D}(f)` may exceed the standard angular bounds of 
:math:`0 \leq \angle \leq 360` or :math:`-90 \leq \angle \leq 90` for right 
ascension and declination respectively. As such, we can convert the angles 
back into this range :math:`R` (in degrees) using:

.. math::

    \alpha_{f,R} = (\alpha_f + 360) \mod 360 \\
    \delta_{f,R} = \left| ((\delta_f - 90) \mod 360) - 180 \right| - 90

These values, still in degrees per :ref:`technical-conventions`, are then 
passed to the systems which need this prediction of the asteroid's location.