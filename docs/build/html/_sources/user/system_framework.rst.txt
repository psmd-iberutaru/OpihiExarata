
.. _user-system-framework:

================
System Framework
================

We briefly cover a few terms and processes necessary for usage of this 
software. This does not go into more detail than is needed by a standard user; 
for more information, see the :ref:`technical-index`.

Engines
=======

For processing of Opihi data, there are four problems which the OpihiExarata 
does not solve on its own (or does not have the data to do so). They are:

- Astrometric plate solving of an image.
- Photometeric calibration.
- Preliminary orbit determination.
- Ephemeris computations.

Additionally, there is another problem which is implemented similarly as if 
OpihiExarata could not solve it on its own:

- On-sky target propagation.

These five problems are solved by sending relevant data to other services, 
utilizing their APIs to compute a solution. (See our :ref:`user-citations` for 
more references.)

Each of these services are made by different organizations. We access the 
capabilities of theses service by what we call an "engine". Each service has 
their own custom implemented engine. Selecting a given engine (as you use this 
program) means that your data will be processed by the service the engine 
corresponds to.

You can find out about the different available services (and thus engines) in 
:ref:`technical-architecture-services-engines`.

Vehicles and Solutions
----------------------

There may be multiple engines for solving one of the five problems. Different 
datasets may be predisposed to work better with one engine over another. As an 
implementation detail, we also built wrappers around the engines called 
vehicle functions and solution classes for ease of use. More detail about these 
wrappers can be found in :ref:`technical-architecture-vehicles-solutions`, but 
it likely is of little concern to the average user. 

Conceptually, you may think of the engine as synonymous with the service; the 
rest are just unnecessary details.