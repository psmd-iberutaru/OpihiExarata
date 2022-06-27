.. _technical-architecture-services-engines:

====================
Services and Engines
====================

The OpihiExarata software primarily outsources solving the main five problems 
for solving an image to other internal or external modules, those being:

- The image astrometric solution, the pointing of the image and its WCS solution;
- The photometric solution, determined from a photometric star catalog;
- The preliminary orbit determination, calculated from a record of observations;
- The ephemeris, calculated from a set of provided orbital elements;
- The asteroid propagation, calculated from a set of asteroid observations.

There are many different types of services and programs which are available 
that are able to solve the above problems. We decided that it is good to 
allow the user (or the program in general) to be able to customize/swap which 
service they use to process their data. This interchangeability also allows 
for OpihiExarata to be more stable as if a given service fails, a different 
one can be selected to continue instead of said inability breaking the 
software and workflow.

Each service has different interfaces and protocols for communication between 
it and external problems like OpihiExarata; some have nice APIs while others 
are more complicated. 

To deal with the fact that each service has unique interfaces, we implemented 
a wrapper/abstraction layer for each and every supported service. This 
abstraction layer allows for easier implementation of these services.
These abstraction layers are called Engines and are implemented in as 
subclasses from :py:mod:`opihiexarata.library.engine`. These engines are 
classified under 
:ref:`technical-architecture-services-engines-astrometryengines`, 
:ref:`technical-architecture-services-engines-photometryengines`, 
:ref:`technical-architecture-services-engines-orbitengines`, 
:ref:`technical-architecture-services-engines-ephemerisengines`, 
:ref:`technical-architecture-services-engines-propagateengines`
depending on the problem it solves.

We detail all of the available engines (which solve the five problems) here. 
Note that the names of the engines themselves (when in the code or otherwise) 
are case insensitive.

A lot of these engines use other external services, see :ref:`user-citations` 
for our references.

.. _technical-architecture-services-engines-astrometryengines:

AstrometryEngines
=================

These engines solve for the astrometric plate solution of an image.


Astrometry.net Nova
-------------------

Implementation: :py:class:`opihiexarata.astrometry.webclient.AstrometryNetWebAPIEngine`

This allows for the leveraging of the 
`Astrometry.net Nova online service <https://nova.astrometry.net/>`_ for 
astrometric plate solving. It is a stable system able to solve most images. 
However, as it is a public system, there is a queue so solving a particular 
image may take longer from your perspective because of the added wait time.
This implementation is based off of the 
`official version <https://github.com/dstndstn/astrometry.net/blob/main/net/client/client.py>`_.

The images taken are uploaded to the service to be solved, OpihiExarata 
periodically requests the solution, parsing it when the image is astrometrically 
solved successfully.




.. _technical-architecture-services-engines-photometryengines:

PhotometryEngines
=================

These engines solve for the photometric calibration solution of an image.


Pan-STARRS 3pi DR2 MAST
-----------------------

Implementation: :py:class:`opihiexarata.photometry.panstarrs.PanstarrsMastWebAPIEngine`

This specifies that the photometric database to be used for photometric 
calibration should be Pan-STARRS 3pi Data Release 2. We access it via a web 
interface using the 
`Pan-STARRS MAST API <https://catalogs.mast.stsci.edu/docs/panstarrs.html>`_.

The Pan-STARRS 3pi Data Release 2 survey covers areas north of -30 
degrees declination in only the g', r', i', and z' filters. OpihiExarata
queries the database around the field of view for photometric stars to use in 
calculating relevant the photometric quantities of the image.



.. _technical-architecture-services-engines-orbitengines:

OrbitEngines
============

These engines solve for preliminary orbital elements from a list of 
observations.


OrbFit
------

Implementation: :py:class:`opihiexarata.orbit.orbfit.OrbfitOrbitDeterminerEngine`

This utilizes the `OrbFit software system <http://adams.dm.unipi.it/orbfit/>`_ 
in determining the preliminary orbital elements of a sun-orbiting object 
(typically an asteroid) provided a list of on-sky coordinate observations 
through time. This particular software system uses least-squares as its method 
of orbit determination.


Custom Orbit
------------

Implementation: :py:class:`opihiexarata.orbit.custom.CustomOrbitEngine`

This does not utilize any actual service for orbital determination. The user 
provides the orbital elements to use along with their respective epoch period.
No asteroid observational information is used. Typically orbital elements a 
user provides through an interface (GUI) should be passed through the 
vehicle arguments (see :ref:`technical-architecture-services-engines`).



.. _technical-architecture-services-engines-ephemerisengines:

EphemerisEngines
================

These engines solve for an asteroid's on-sky track from a set of 
Keplerian orbital elements.


.. _technical-architecture-services-engines-ephemerisengines-jpl-horizons:

JPL Horizons
------------

Implementation: :py:class:`opihiexarata.ephemeris.jplhorizons.JPLHorizonsWebAPIEngine`

This utilizes the `JPL Horizons System <https://ssd.jpl.nasa.gov/horizons/>`_
from the `JPL Solar Systems Dynamics <https://ssd.jpl.nasa.gov/>`_ group for 
the determination of an ephemeris from a set of Keplerian orbital elements.
This software sends the orbital elements (and other observatory parameters) 
via the `Horizons API <https://ssd-api.jpl.nasa.gov/doc/horizons.html>`_ 
service and parses the returned ephemeris.



.. _technical-architecture-services-engines-propagateengines:

PropagateEngines
================

These engines solve for an asteroid's (or other target's) on-sky track from a 
set of recent observations.

Linear
------

Implementation: :py:class:`opihiexarata.propagate.polynomial.LinearPropagationEngine`

This takes the most recent (within a few hours) observations and fits a 
first order (linear) polynomial function to both the RA and DEC as a function 
of time. This method assumes a tangent plane projection and so is not suited 
for propagations on long timescales. See 
:ref:`technical-algorithms-polynomial-propagation` for more information on the 
algorithm used.


Quadratic
---------

Implementation: :py:class:`opihiexarata.propagate.polynomial.QuadraticPropagationEngine`

This takes the most recent (within a few hours) observations and fits a 
second order (quadratic) polynomial function to both the RA and DEC as a 
function of time. This method assumes a tangent plane projection and so is not 
suited for propagations on long timescales. See 
:ref:`technical-algorithms-polynomial-propagation` for more information on the 
algorithm used.


