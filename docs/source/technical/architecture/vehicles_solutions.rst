.. _technical-architecture-vehicles-solutions:

======================
Vehicles and Solutions
======================

Vehicles
========


Solution
========

OpihiSolution
-------------

The OpihiSolution is a class which is built to conveniently store and interface
with all of the of the other solution classes provided by OpihiExarata. This 
grouping is beneficial because a single image and its associated solutions 
can remain together and saving the newly solved data is a lot easier. 

The OpihiSolution class, which contains all of the functionality which 
OpihiExarata has to offer for a single image from Opihi, also is helpful for 
interfacing with the GUI.


AstrometrySolution
~~~~~~~~~~~~~~~~~~

Implementation: :py:class:`opihiexarata.astrometry.solution.AstrometricSolution`

The AstrometrySolution contains the results and other related functions 
which are derived from the astrometry engines and converted to a standard 
form from their appropriate vehicle functions.

Primarily, it contains a table listing the stars which were observed to be 
in the field and their pixel location. It also contains a way to convert 
between pixel and on-sky coordinates or vice-verse.


PhotometrySolution
~~~~~~~~~~~~~~~~~~

Implementation: :py:class:`opihiexarata.photometry.solution.PhotometricSolution`

The PhotometrySolution contains the results and other related functions 
which are derived from the photometry engines and converted to a standard 
form from their appropriate vehicle functions.

Primarily, it contains a table listing the stars which are detected within the 
astrometric solution and also have filter magnitudes provided by the 
photometric database; aperture DN counts are also given. An average sky value 
is calculated by excluding these sources and is used to correct the aperture 
DN counts. From this table and the corrected DN counts, the filter zero point 
and its error are also calculated.


OrbitalSolution
~~~~~~~~~~~~~~~

Implementation: :py:class:`opihiexarata.orbit.solution.OrbitalSolution`

The OrbitalSolution contains the results and other related functions 
which are derived from the orbit engines and converted to a standard 
form from their appropriate vehicle functions.

Primarily, it contains the siz primary Keplerian orbital elements along with 
the epoch that these orbital elements. The mean anomaly is the primary anomaly 
used. However, the eccentric anomaly is also calculated using Newton's method 
to solve Kepler's equation: :math:`M = E - e \sin E`. The true anomaly is 
then calculated from the eccentric anomaly and the eccentricity using 
geometry.


EphemeriticSolution
~~~~~~~~~~~~~~~~~~~

Implementation: :py:class:`opihiexarata.ephemeris.solution.EphemeriticSolution`

The EphemeriticSolution contains the results and other related functions 
which are derived from the ephemeris engines and converted to a standard 
form from their appropriate vehicle functions.

Primarily, it contains the ephemeris function. This function provides for the 
on-sky coordinates of an asteroid at a (provided) future time based on the 
ephemeris. The ephemeris itself is derived from the orbital elements as 
provided by the OrbitalSolution.


PropagativeSolution
~~~~~~~~~~~~~~~~~~~

Implementation: :py:class:`opihiexarata.propagate.solution.PropagativeSolution`

The PropagativeSolution contains the results and other related functions 
which are derived from the propagation engines and converted to a standard 
form from their appropriate vehicle functions.

Primarily, it contains the propagation function. This function provides for 
the on-sky coordinates of an asteroid at a (provided) future time based on 
the propagation of the asteroid's path on the sky. The propagation of the 
path is determined by extrapolating the motion of the asteroid on the 
sky based on a sequence of recent images.


.. _technical-architecture-vehicles-solutions-preprocesssolution:

PreprocessSolution
------------------

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

The implementation of image preprocessing is done by the PreprocessSolution
(see :py:class:`opihiexarata.opihi.preprocess.OpihiPreprocessSolution`). 
However, because the preprocessing of CCD images is pretty standard and simple
and involves only one method, this solution does not require an engine and 
instead implements it itself.

Moreover, because many of the image calibration files used are generally the 
same from image to image, this solution is also not image specific. Instead, 
it contains a function which will take an image (either an array or a fits 
file) and pre-process it. It is built like this so that the large preprocessing 
calibration images (which are cached within the class to avoid disk utilization)
does not take up a too much memory as opposed if the class was duplicated per 
image.