.. _technical-architecture-vehicles-solutions:

======================
Vehicles and Solutions
======================

Vehicles
========

The input and output of each of the engines are curtailed to each service. 
(See :ref:`technical-architecture-services-engines` for the engines.) 
However, the solution classes all expect exactly the same input regardless 
of which engine/service is used. To extract the needed information from an 
engine for the instantiation of the solution class, we mimic the usage of an 
engine (by a user) via what we call a vehicle function. 

A vehicle function is just a section of code which mimics the usage of the 
engines that access the service, using it to determine the required results 
for the solutions. All vehicle functions have the same input (additional 
arguments may be provided in rare cases for special engines, details are 
engine specific and may be found in 
:ref:`technical-architecture-services-engines`) and the exact same output 
depending on the solution class it services. We detail the inputs 
and outputs here for vehicle functions corresponding to the solutions, 
exceptions (like additional arguments).


Astrometry Vehicle Functions
----------------------------

.. _figure-vehicle-function-astrometry:

.. figure:: /assets/images/vehicle-function-astrometry.*

    A somewhat visual description of the input arguments used by 
    astrometric vehicle functions and their respective engines to 
    provide the information for astrometric solutions.
    
As shown in :numref:`figure-vehicle-function-astrometry`, the astrometric 
vehicle functions and engines generally require the input of the image data. 
They are required to return the on-sky position of the image, its orientation, 
and pixel scale. They also must provide a table of all of the stars which are 
within the field along with a 
`FITS world coordinate system (WCS) <https://fits.gsfc.nasa.gov/fits_wcs.html>`_ 
solution as implemented via Astropy.


Photometry Vehicle Functions
----------------------------

.. _figure-vehicle-function-photometry:

.. figure:: /assets/images/vehicle-function-photometry.*

    A somewhat visual description of the input arguments used by 
    photometric vehicle functions and their respective engines to 
    provide the information for photometric solutions.

As shown in :numref:`figure-vehicle-function-photometry`, the photometric 
vehicle functions and engines generally require the input of parameters (RA, 
DEC, and search radius) to do a cone search of a photometric catalog. They are 
required to return a table detailing the location and filter magnitudes of all 
found stars within the search radius along with a list of filters which the 
table contains data for.


Orbit Vehicle Functions
-----------------------

.. _figure-vehicle-function-orbit:

.. figure:: /assets/images/vehicle-function-orbit.*

    A somewhat visual description of the input arguments used by 
    orbital vehicle functions and their respective engines to 
    provide the information for orbital solutions.

As shown in :numref:`figure-vehicle-function-orbit`, the orbital vehicle 
functions and engines generally require the input of asteroid observations 
in the 80-column Minor Planet Center format. They are required to output 
(from their calculations) the six Keplerian orbital elements are calculated 
(along with their errors) as outputs; the epoch of these orbital elements 
must also be returned. 


Ephemeris Vehicle Functions
---------------------------

.. _figure-vehicle-function-ephemeris:

.. figure:: /assets/images/vehicle-function-ephemeris.*

    A somewhat visual description of the input arguments used by 
    ephemeris vehicle functions and their respective engines to 
    provide the information for ephemeris solutions.

As shown in :numref:`figure-vehicle-function-ephemeris`, the ephemeris 
vehicle functions and engines generally require the input of the six 
Keplerian orbital elements and the epoch that they were determined for. 
They are required to output the on-sky rates (both first order, "velocity", 
and second order, "acceleration") of an asteroid (or other target) and a 
function which, when specified a time of observation, gives the predicted 
on-sky position from the ephemeris.



Propagation Vehicle Functions
-----------------------------

.. _figure-vehicle-function-propagate:

.. figure:: /assets/images/vehicle-function-propagate.*

    A somewhat visual description of the input arguments used by 
    propagation vehicle functions and their respective engines to 
    provide the information for propagation solutions.

As shown in :numref:`figure-vehicle-function-propagate`, the propagation 
vehicle functions and engines generally require the input of on-sky 
observations (RA, DEC, and observational time) of an asteroid. They are 
required to output the on-sky rates (both first order, "velocity", and 
second order, "acceleration") of an asteroid (or other target) and a function 
which, when specified a time of observation, gives the predicted on-sky 
position from propagating the on-sky motion. 


Solution
========

Solutions classes incorporate information extracted from the engines and 
vehicles. These classes also calculates other values which are derived from 
the results of the engine and vehicle functions.

OpihiSolution
-------------

The OpihiSolution is a class which is built to conveniently store and interface
with all of the of the other solution classes provided by OpihiExarata for a 
single image. This grouping is beneficial because a single image and its 
associated solutions can remain together and saving the newly solved data is 
a lot easier. 

The OpihiSolution class, which contains all of the functionality which 
OpihiExarata has to offer for a single image from Opihi, is also a helpful 
abstraction for developing the interactions between the GUI and an image and 
its data.


AstrometrySolution
~~~~~~~~~~~~~~~~~~

Implementation: :py:class:`opihiexarata.astrometry.solution.AstrometricSolution`

The AstrometrySolution contains the results and other related functions 
which are derived from the astrometry engines and converted to a standard 
form from their appropriate vehicle functions.

Primarily, it contains the on-sky location of an image along with its pixel 
scale. It also contains a table listing the stars which were observed to be 
in the field and their pixel location. A way to convert between pixel and 
on-sky coordinates or vice-verse is implemented utilizing the WCS solution.


PhotometrySolution
~~~~~~~~~~~~~~~~~~

Implementation: :py:class:`opihiexarata.photometry.solution.PhotometricSolution`

The PhotometrySolution contains the results and other related functions 
which are derived from the photometry engines and converted to a standard 
form from their appropriate vehicle functions.

Primarily, it contains a table listing the stars which are detected within the 
astrometric solution and it also has their filter magnitudes as provided by the 
photometric database; aperture DN counts are also given. An average sky value 
is calculated from sky regions, i.e. not including the stellar regions and 
other regions on the detector. This average sky value is used to correct the 
aperture DN counts. From this table and the corrected DN counts, the filter 
zero point and its error are also calculated.


OrbitalSolution
~~~~~~~~~~~~~~~

Implementation: :py:class:`opihiexarata.orbit.solution.OrbitalSolution`

The OrbitalSolution contains the results and other related functions 
which are derived from the orbit engines and converted to a standard 
form from their appropriate vehicle functions.

Primarily, it contains the siz primary Keplerian orbital elements along with 
the epoch that these orbital elements. The mean anomaly :math:`M` is the 
primary anomaly used. However, the eccentric anomaly :math:`E` is also 
calculated using Newton's method to solve Kepler's equation: 
:math:`M = E - e \sin E`. The true anomaly :math:`\nu` is then calculated 
from the eccentric anomaly and the eccentricity using the geometrically 
derived formula: (See 
`Broucke, R. Celestial Mechanics p. 388 <https://ui.adsabs.harvard.edu/abs/1973CeMec...7..388B>`_.)

.. math::

    \tan\left( \frac{\nu - E}{2} \right) = \frac{\beta \sin E}{1 - \beta \cos E}

Where :math:`\beta` is:

.. math::
    
    \beta \triangleq \frac{e}{1 + \sqrt{1 - e^2}}


EphemeriticSolution
~~~~~~~~~~~~~~~~~~~

Implementation: :py:class:`opihiexarata.ephemeris.solution.EphemeriticSolution`

The EphemeriticSolution contains the results and other related functions 
which are derived from the ephemeris engines and converted to a standard 
form from their appropriate vehicle functions.

Primarily, it contains the ephemeris function. This function provides for the 
on-sky coordinates of an asteroid at a (provided) future time based on the 
ephemeris. It also contains the on-sky first-order and second-order rates of 
an asteroid. The ephemeris itself is derived from the orbital elements as 
provided by the OrbitalSolution.


PropagativeSolution
~~~~~~~~~~~~~~~~~~~

Implementation: :py:class:`opihiexarata.propagate.solution.PropagativeSolution`

The PropagativeSolution contains the results and other related functions 
which are derived from the propagation engines and converted to a standard 
form from their appropriate vehicle functions.

Primarily, it contains the propagation function. This function provides for 
the on-sky coordinates of an asteroid at a (provided) future time based on 
the propagation of the asteroid's path on the sky.  It also contains the 
on-sky first-order and second-order rates of an asteroid. The propagation of 
the path is determined by extrapolating the motion of the asteroid on the 
sky based on a sequence of recent images.


.. _technical-architecture-vehicles-solutions-opihipreprocesssolution:

OpihiPreprocessSolution
-----------------------

The data that comes from the Opihi camera is considered raw data, it has many
systematic artifacts like hot pixels, dark current, and bias to name a few.
We reduce this data using standard array processing procedures.

We can remove these using preprocessing calibration images. These images 
are taken before hand. For the use case for Opihi, using archive calibration
files are more than satisfactory and avoiding the need for the user to 
take calibration images on their own reduces the overhead.

An explanation on the procedure and methodology of data preprocessing is 
assumed by this manual, but a brief summary may be 
`obtained from here <https://wiki.digiultsparrow.space/en/academic/notes/astronomical-ccd-image-preprocessing>`_.

The implementation of image preprocessing is done by the OpihiPreprocessSolution 
class (see :py:class:`opihiexarata.opihi.preprocess.OpihiPreprocessSolution`). 
However, because the preprocessing of CCD images is pretty standard and simple
and involves only one method, this solution does not require an engine and 
instead implements it itself.

Moreover, because many of the image calibration files used are generally the 
same from image to image, this solution is also not image specific unlike the 
other solution classes. Instead, it contains a function which will take an 
image (either an array or a fits file) and pre-process it. It is built like 
this so that the large preprocessing calibration images (which are cached 
within the class to avoid disk utilization) does not take up a too much 
memory as opposed if the class was duplicated per image.


.. _technical-architecture-vehicles-solutions-opihizeropointdatabasesolution:

OpihiZeroPointDatabaseSolution
------------------------------

In order to properly manage and store zero point observations, we utilize a 
solution which provides us an API-like interface to the zero point database.
The implementation of this interface is done by the 
OpihiZeroPointDatabaseSolution 
(see :py:class:`opihiexarata.opihi.database.OpihiZeroPointDatabaseSolution`).

The specifics of the database are explained in 
:ref:`technical-architecture-monitor-database`. The monitoring webpage which 
shows recent information added to the database to a user is described in 
:ref:`user-zero-point-monitoring`.