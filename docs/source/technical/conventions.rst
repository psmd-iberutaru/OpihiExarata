.. _technical-conventions:

===========
Conventions
===========

In order for the entire software to be self-consistent, a few conventions 
have been established to help develop it. We detail these conventions here.

Sky-Coordinate Systems
======================

By convention, and for future proofing, we use and rely on the International 
Celestial Reference System (ICRS) to define our coordinates. 

For the purposes of this project we assume that the ICRS system and the 
FK5 J2000 system are equivalent. Converting between these two systems is 
seen as a waste of time and unnecessary complexity provided the small 
difference between the two.


Units
=====

Although there are many packages like Astropy which help deal with different 
units and the conversion between the two, we decided that it is easier to 
conform to a single set of units for the values within the software and 
converting only where needed via a module (see 
:ref:`technical-architecture-library-conversion`). We describe the units used 
in the following table. 

+----------------------+--------------------------------+
| Quantity             | Unit                           |
+======================+================================+
| Angles               | Degrees                        |
+----------------------+--------------------------------+
| Date-time            | Julian days                    |
+----------------------+--------------------------------+
| Time difference      | Days or seconds                |
+----------------------+--------------------------------+
| Orbital elements     | (Convention, see below)        |
+----------------------+--------------------------------+
| Pixel scale          | Arcseconds per pixel           |
+----------------------+--------------------------------+
| On-sky velocity      | Degrees per second             |
+----------------------+--------------------------------+
| On-sky acceleration  | Degrees per second squared     |
+----------------------+--------------------------------+

- We use degrees for angles because, unlike angular hours, it is much easier to use mathematically. Radians were considered but were ultimately not used because declination already used degrees and it is far less prevalent than degrees in astronomy.
- Date time, the measurement of an absolute time relative to an epoch, uses Julian days (JD). UNIX time is not as prevalent in astronomy compared to JD and MJD for the services encountered. JPL Horizons (see :ref:`technical-architecture-services-engines-ephemerisengines-jpl-horizons`) uses JD and because conversion between JD and MJD is trivial; we stuck with JD. 
- Time difference, the measurement of time between two different date times, is either in days (for times on the order of hours or days) or seconds (for times on the order of seconds or minutes). We primarily use days except in cases where the numerical value is too small (for example, with :ref:`technical-algorithms-polynomial-propagation`). The usage of which unit is documented.
- The Keplerian orbital elements are in the units that they are conventionally in. The semi-major axis :math:`a` is in AU, the eccentricity :math:`e` is unit-less, the inclination :math:`i` is in degrees, the longitude of ascending node :math:`\Omega` is in degrees, the argument of perihelion :math:`\omega` is in degrees, and the mean anomaly :math:`M` is in degrees. The epoch of these orbital elements is in Julian days, as is the convention for date-times.
- The pixel scale, as is traditionally given in most other contexts, is provided as arcseconds per pixel.
- The on-sky first order motion (i.e. the "velocity") in RA and DEC of an asteroid or other target is given in degrees per second. Degrees are used to keep both the angular units the same as the standard convention and seconds are use because they are a much more reasonable unit for the motion than days (the other time difference unit.)
- The on-sky second order motion (i.e. the "acceleration") in RA and DEC of an asteroid or other target is given in degrees per second squared. The reasoning for using both degrees and seconds is the same as provided for the on-sky first order motion.


Code Style
==========

Formatting Style
----------------

For consistency, the Python code style that this project uses is the 
`black <https://pypi.org/project/black/>`_ code style. This style is enforced 
by the aforementioned package, the auxillary script from 
:ref:`technical-installation-automated-scripts` will trigger automated code 
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


Documentation Files
===================

The documentation is automatically generated using Sphinx. Because of this, 
there are some peculiarities when writing the documentation, we document them 
here.

Main Body Files
---------------

The main body of documentation uses reStructuredText files as markup. A 
Sphinx specific primer can be found on 
`their website <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_. A more complete reference for reStructuredText can be found in 
`their documentation <https://docutils.sourceforge.io/rst.html>`_.

Image Files
-----------

Images are important in providing additional information in documentation. 
Because the documentation can be built into either HTML or LaTeX forms, special 
care should be exercised for images as both take different file formats.

When calling an image or figure file, the file path in the reStructuredText 
should have the file extension as a wildcard so that the Sphinx builders
can choose the file format best suited for the form the documentation is 
going to be built into. 

When creating images, please adhere to the following:

- If the image is a raster image, save the image as a PNG file. 
- If the image is a vector graphics file, save the image as both a SVG and PDF file. (HTML supports only SVG and LaTeX supports only PDF, so both are needed.)

Python Docstrings
-----------------

For Sphinx to properly load and process the documentation strings from the 
Python files themselves, they need to be marked up in a specific way. Natively
it would be in reStructuredText, but it looks ugly. Instead, we use the 
Napoleon extension for Sphinx to allow for the usage of 
`NumPy docstring formatting <https://numpydoc.readthedocs.io/>`_.
`An example of Numpy formatting is also provided by Sphinx <https://www.sphinx-doc.org/en/master/usage/extensions/example_numpy.html>`_.


.. _technical-conventions-filter-names:

Filter Names
============

Although the filter wheel has its own description of the filter names, for 
ease of programming, we define the following filter names to use throughout 
the software. They are typically single characters indicative of the actual 
filter name.

+--------------------------+--------------------+
| OpihiExarata Filter Name | Normal Filter Name |
+==========================+====================+
| c                        | clear              |
+--------------------------+--------------------+
| g                        | g'                 |
+--------------------------+--------------------+
| r                        | r'                 |
+--------------------------+--------------------+
| i                        | i'                 |
+--------------------------+--------------------+
| z                        | z'                 |
+--------------------------+--------------------+
| 1                        | (A filler value.)  |
+--------------------------+--------------------+
| 2                        | (A filler value.)  |
+--------------------------+--------------------+
| b                        | blank              |
+--------------------------+--------------------+