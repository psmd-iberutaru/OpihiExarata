.. _technical-architecture-vehicles-solutions:

======================
Vehicles and Solutions
======================



.. _technical-architecture-vehicles-solutions-preprocesssolution:

PreprocessSolution
==================

The data that comes from the Opihi camera is considered raw data, it has many
systematic artifacts like hot pixels, dark current, and bias to name a few.
We reduce this data using standard array processing procedures.

We can remove these using preprocessing calibration images. These images 
are taken before hand. For the use case for Opihi, using archive calibration
files are more than satisfactory and avoiding the need for the user to 
take calibration images on their own reduces the overhead.

An explanation on the procedure and methedology of data preprocessing is 
assumed by this manual, but a breif summary may be 
`obtained from here <https://wiki.digiultsparrow.space/en/academic/notes/astronomical-ccd-image-preprocessing>`_.
