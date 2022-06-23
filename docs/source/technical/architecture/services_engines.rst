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
subclasses from :mod:`opihiexarata.library.engine`. These engines are 
classified under 
:ref:`technical-architecture-services-engines-astrometryengines`, 
:ref:`technical-architecture-services-engines-photometryengines`, 
:ref:`technical-architecture-services-engines-orbitengines`, 
:ref:`technical-architecture-services-engines-ephemerisengines`, 
:ref:`technical-architecture-services-engines-propagateengines`
depending on the problem it solves.

We detail all of the available engines (which solve the five problems) here. 


.. _technical-architecture-services-engines-astrometryengines:

AstrometryEngines
=================

These engines solve for the astrometric plate solution of an image.



.. _technical-architecture-services-engines-photometryengines:

PhotometryEngines
=================

These engines solve for the photometric calibration solution of an image.



.. _technical-architecture-services-engines-orbitengines:

OrbitEngines
============

These engines solve for preliminary orbital elements from a list of 
observations.



.. _technical-architecture-services-engines-ephemerisengines:

EphemerisEngines
================

These engines solve for an asteroid's on-sky track from a set of 
Keplerian orbital elements.



.. _technical-architecture-services-engines-propagateengines:

PropagateEngines
================

These engines solve for an asteroid's (or other target's) on-sky track from a 
set of recent observations.

