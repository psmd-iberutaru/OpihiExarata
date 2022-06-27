.. _technical-conventions:

===========
Conventions
===========

In order for the entire software to be self-consistent, a few conventions 
have been established to help develop it. We detail these conventions here.


Units
=====

Although there are many packages like Astropy which help deal with different 
units and the conversion between the two, we decided that it is easier to 
conform to a single set of units for the values within the software and 
converting only where needed via a module (see 
:ref:`technical-architecture-library-conversion`). We describe the units used 
in the following table. 

+------------------+---------------------+
| Quantity         | Unit                |
+==================+=====================+
| Angles           | Degrees             |
| Date-time        | Julian days         |
| Delta time       | Days or seconds     |
| Orbital elements | (Convention)        |
+------------------+---------------------+

- We use degrees for angles because, unlike angular hours, it is much easier to use mathematically. Radians were considered but were ultimately not used because declination already used degrees and it is far less prevalent than degrees in astronomy.
- Date time, the measurement of an absolute time relative to an epoch, uses Julian days (JD). UNIX time is not as prevalent in astronomy compared to JD and MJD for the services encountered. JPL Horizons (see :ref:`technical-architecture-services-engines-ephemerisengines-jpl-horizons`) uses JD and because conversion between JD and MJD is trivial, we stuck with JD. 
- Delta time, the measurement of time between two different times, is either in days (for times on the order or hours or days) or seconds (for times on the order of seconds or minutes). We primarily use days except in cases where the numerical value is too small (for example, with :ref:`technical-algorithms-polynomial-propagation`). The usage of which unit is documented.
- The Keplerian orbital elements are in the units that they are conventionally in. The semi-major axis :math:`a` is in AU, the eccentricity :math:`e` is unit-less, the inclination :math:`i` is in degrees, the longitude of ascending node :math:`\Omega` is in degrees, the argument of perihelion :math:`\omega` is in degrees, and the mean anomaly :math:`M` is in degrees. The epoch of these orbital elements is in Julian days, as is the convention for date-times.


Code Style
==========

Formatting Style
----------------

For consistency, the Python code style that this project uses is the 
`black <https://pypi.org/project/black/>`_ code style. This style is enforced 
by the aforementioned package, the auxillary script from 
:ref:`technical-installation-automated-scripts` will trigger proper code 
formatting.

Type Hinting
------------

Type hinting allows for many text and development environments to infer 
specific properties of code to provide better suggestions and other 
programming tools. Python supports type hinting (see :pep:`483` and :pep:`484`) 
and this software adapts type hinting. Although it is not required for the 
program to run, it both makes the code easier to work with because of the 
added programming tool functionality along with conveying more information 
about the code to future maintainers. There is very little downside. There 
is existing infrastructure for making using type hinting easier to use from 
:ref:`technical-architecture-library-hint`.



