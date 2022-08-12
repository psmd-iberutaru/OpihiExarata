.. _user-manual-mode:

===========
Manual Mode
===========

The manual mode of OpihiExarata is its asteroid view-finding mode. Although,
photometric monitoring can be done manually, and the manual mode is well 
equipped for said use case, it is not the primary use case for the manual mode.

The user uses the Opihi instrument to take images of an asteroid. Then they 
specify the location of the asteroid using a GUI (usually with help from 
comparing their image to a reference image). An astrometric solution can 
convert the asteroid's pixel location to an on-sky location. Then by 
utilizing previous observations, its path across the sky can be determined. 
This information is used to properly point the IRTF telescope to the desired 
asteroid target.

We present the procedure for operating OpihiExarata in its manual mode, 
please also reference the GUI figure provided for reference. We also summarize 
the procedure and process of the manual mode via a flowchart.

.. _user-manual-mode-graphical-user-interface:

Graphical User Interface
========================

.. _figure-manual-mode-gui-all:

.. figure:: /assets/images/manual-mode-gui-all.*

    The GUI of the manual mode of OpihiExarata. This is what you see when 
    the interface is freshly loaded. Most of the text is filler text, they will
    change as the program is executed. Note that there are different tabs for 
    the summary, astrometry, photometry, orbit, ephemeris, and propagation. 
    Each of the sections covers their GUIs, this is just the general GUI.

The manual mode GUI contains a main data window and a few tabs 
compartmentalizing a lot of the functionality of OpihiExarata, see 
:numref:`figure-manual-mode-gui-all`.

In the manual mode general GUI, you have three buttons which control file 
and target acquisition. The :guilabel:`New Target` button specifies that you 
desire to work on a new target (typically a new asteroid). The 
:guilabel:`Manual New Image` button opens a file dialog so that you can 
select a new Opihi image FITS file to load into OpihiExarata. The 
:guilabel:`Automatic New Image` button pulls the most recent FITS image from 
the same directory as the last image specified manually.

There is also a data viewer. Relevant information from the solutions will be 
plotted here along with the image data. There is a navigation bar for 
manipulating the image, including zooming, panning, saving, and configuring 
other options. This functionality makes use of matplotlib, see 
`Interactive navigation (outdated) <https://matplotlib.org/3.2.2/users/navigation_toolbar.html>`_ 
or `Interactive figures <https://matplotlib.org/stable/users/explain/interactive.html>`_
for more information.

There is also a :guilabel:`Refresh Window` button to redraw the image in the 
viewer and to also refresh the information in the tabs. This should not be 
needed too much as the program should automatically refresh itself if there 
is new information.

Supplementary information is provided in the summary tab. This includes 
information about the path of the file, the filename, and methods to save the 
file. 

A :guilabel:`Send Target to TCS` button allows for the user to send the target 
location (after astrometry has been executed) to the telescope operator and 
the telescope control software. Non-sidereal rates are sent as well if they 
were calculated via 

Procedure
=========

.. _figure-manual-mode-flowchart:

.. figure:: /assets/images/manual-mode-flowchart.*

    A flowchart summary of the procedure of the manual mode. It includes 
    the actions of the user along with the program's flow afterwards.

We describe the procedure for utilizing the asteroid view-finding (manual) 
mode of OpihiExarata. See :numref:`figure-automatic-mode-flowchart` for a 
flowchart summary of this procedure.


Start and Open GUI
------------------
You will want to open the OpihiExarata manual mode GUI, typically via the 
command-line interface with::

    opihiexarata manual --config=config.yaml --secret=secrets.yaml

Please replace the configuration file names with the correct path to your 
configuration and secrets file; see :ref:`user-configuration` for more 
information.


.. _user-manual-mode-procedure-specify-new-target-name:

Specify New Target Name
-----------------------

The OpihiExarata manual mode software groups sequential images as belonging to 
a set of observations of a single target. In order to tell the software what 
target/asteroid you are observing you need to provide its name.

Use the :guilabel:`New Target` button, it will open a small prompt for you to 
enter the name of the asteroid/target you are observing. From this point on, 
all images loaded (either manually or automatically fetched) will be assumed 
to be of the target you provided (until you change it by clicking the button 
again).

.. note::
    If you are observing an asteroid, this target name should also be the name 
    of the asteroid. The software will attempt to use this name to obtain 
    historical observations from the Minor Planet Center.


Take and Image
--------------

The first step in processing data is to take an image using the camera 
controller. 

.. note::
    It is highly suggested that you take two images if this is the first image 
    you are taking of a given specified asteroid. This allows you to have a 
    reference image which makes asteroid finding much easier. You process the 
    first image normally (using the second image as the reference image) then 
    process the second image (using the first image as the reference image). 
    It does not matter which is the reference image for more images taken. (See 
    :ref:`user-manual-mode-procedure-find-asteroid-location`.)


.. _user-manual-mode-procedure-find-asteroid-location:

Find Asteroid Location
----------------------

You will need to find and specify the location of the asteroid in the image. 
It is beyond the scope of this software and procedure to implement this 
automatically. (If you are not observing asteroids, you may skip this step 
and just click :guilabel:`Submit` in the 
:ref:`user-manual-mode-procedure-find-asteroid-location-target-selector-gui`.)

Use the :ref:`user-manual-mode-procedure-find-asteroid-location-target-selector-gui`
to find the asteroid pixel location.


.. _user-manual-mode-procedure-find-asteroid-location-target-selector-gui:

Target Selector GUI
~~~~~~~~~~~~~~~~~~~

.. _figure-target-selector-gui:

.. figure:: /assets/images/target-selector-gui.*

    The GUI for finding the pixel location of a target in the image. The 
    targets are typically asteroids.

The target selector GUI allows you to select a specific target (generally an 
asteroid) location in an image, see :numref:`figure-target-selector-gui`.

The current file which you are determining the location of a target in is 
given by :guilabel:`Current:`. The reference image (if provided) used to 
compare against is given by :guilabel:`Reference:`. Both of these files can 
be changed using their respective :guilabel:`Change` buttons; a file dialog 
will be opened so you can specify the new FITS files.

There is a data viewer similar to the one specified in 
:ref:`user-manual-mode-graphical-user-interface`. However, in addition, if you 
drag a box (left click and hold, drag, then release) without any tool selected 
in toolbar, the software will search within the drawn (blue) box and 
extract the brightest object within the box. It will mark this target with a 
red triangle. It will assume that this is the desired target and update the 
:guilabel:`Target X` and :guilabel:`Target Y` fields with its pixel coordinates. 

.. note::
    This box drawing method finds the brightest object in the current image. 
    It ignores the subtractive comparison method and its result as such 
    comparisons do not affect the actual current image.

You can compare your current image file :math:`C` with your reference image 
:math:`R` file in two subtractive ways using the two labeled buttons under 
:guilabel:`Subtraction Method`. (There are also buttons for simply viewing 
the images.) Therefore, the two (plus two) ways of viewing the data are:

- :guilabel:`None`, :math:`C-0``: The current image is not compared with the reference image.
- :guilabel:`Reference`, :math:`R-0`: The reference image is shown rather than the current image. 
- :guilabel:`Sidereal`, :math:`C-R`: The two images are subtracted assuming the IRTF is doing sidereal tracking. Because of this assumption, no shifting is done.
- :guilabel:`Non-sidereal`, :math:`C-T_v(R)`: The two images are subtracted assuming the IRTF is doing non-sidereal tracking. Because of this assumption, the images are shifted based on the non-sidereal rates of the current image and the time between the two images. 

The displayed image's color bar scale can be modified manually by entering 
values into the boxes accompanying :guilabel:`Scale [Low High]`, the left and 
right being the lower and higher bounds of the color bar respectively as 
indicated. The scale can also be automatically set so that the lower bound is 
the 1 percentile and the higher bound is the 99 percentile by clicking the 
:guilabel:`1 - 99 %` button. If the :guilabel:`Auto` checkbox is enabled, 
this autoscaling is done whenever a new operation is done the image (i.e. 
using the tools in the toolbar, changing the comparison method, among others).

Select your target, either from the box method or by manually entering the 
coordinates in the :guilabel:`Target X` and :guilabel:`Target Y` boxes, and 
click :guilabel:`Submit`. The location of your target will be recorded.


.. _user-manual-mode-procedure-find-asteroid-location-compute-astrometric-solution:

Compute Astrometric Solution
----------------------------

.. _figure-manual-mode-gui-astrometry:

.. figure:: /assets/images/manual-mode-gui-astrometry.*

    The astrometry GUI tab for customizing and executing astrometric solutions.
    This is the default view before any values have been calculated.

The astrometric solution of the image is next to be solved. The pattern of 
stars within the image is compared with known patterns in astrometric star 
databases to derive the `WCS <https://fits.gsfc.nasa.gov/fits_wcs.html>`_ 
astrometric solution of the image. See :numref:`figure-manual-mode-gui-astrometry`
for the interface for astrometric solutions.

To solve for the astrometric solution of the image, you will need to select 
the desired astrometric engine from the drop down menu then click on the 
:guilabel:`Solve Astrometry` button to solve. 
(See :ref:`technical-architecture-services-engines` for more information on 
the available engines.)

The pixel location (X,Y) of the center of the image, given by 
:guilabel:`Opihi Center`, and the specified target, given by 
:guilabel:`Target/Asteroid`, is provided with or without an astrometric 
solution. When the astrometric solution is provided, the right ascension and 
declination of these will also be provided.

Custom pixel coordinate (X,Y) can be provided in the boxes to be translated to 
the sky coordinates that they correspond to. Alternatively, if sky coordinates 
are provided (in sexagesimal form, RA hours and DEC degrees, delimitated by 
colons), the pixel coordinates of the sky coordinates can also be determined; 
the pixel coordinate boxes must be empty as the solving gives preference to 
pixel to on-sky solving. Enter in either pixel or sky coordinates as described 
and click the :guilabel:`Custom Solve` button to convert it to the other. The 
button does nothing without a valid astrometric solution.


.. _user-manual-mode-procedure-find-asteroid-location-compute-photometric-solution:

Compute Photometric Solution
-----------------------------

.. _figure-manual-mode-gui-photometry:

.. figure:: /assets/images/manual-mode-gui-photometry.*

    The photometry GUI tab for customizing and executing photometric solutions.
    This is the default view before any values have been calculated.

The photometric solution of the image is next to be solved. The brightness of 
the stars in the image is compared to known filter magnitudes from a 
photometric database to derive a photometric calibration solution. 
See :numref:`figure-manual-mode-gui-photometry` for the interface for 
photometric solutions.

This is an optional step and is not related to asteroid finding in of itself. 
This operation can be skipped entirely if a photometric solution is not 
necessary.

To solve for the photometric solution of the image, you will need to select 
the desired photometric engine from the drop down menu then click on the 
:guilabel:`Solve Photometry` button to solve. 
(See :ref:`technical-architecture-services-engines` for more information on 
the available engines.)

The filter that the image was taken in is noted by :guilabel:`Filter`, this is 
determined by the FITS file header.

Once a photometric solution has been solved, the corresponding filter zero 
point magnitude (and its error) of the image is provided by 
:guilabel:`Zero Point`.

.. note::
    Execution of the photometric solution requires a completed astrometric 
    solution from 
    :ref:`user-manual-mode-procedure-find-asteroid-location-compute-astrometric-solution`.


.. _user-manual-mode-procedure-asteroid-on-sky-position:

Asteroid On-Sky Position
------------------------

The asteroid pixel location is derived from the procedure in 
:ref:`user-manual-mode-procedure-find-asteroid-location-target-selector-gui`
and the corresponding on-sky location is derived from the procedure in 
:ref:`user-manual-mode-procedure-find-asteroid-location-compute-astrometric-solution`.


.. _user-manual-mode-procedure-historical-observations:

Historical Observations
-----------------------

The software will attempt to use the target/asteroid name provided in 
:ref:`user-manual-mode-procedure-specify-new-target-name`
to obtain the set of historical observations from the Minor Planet Center.

Recently taken images will also be considered part of the set of historical 
observations.


.. _user-manual-mode-procedure-asteroid-observation-record:

Asteroid Observation Record
---------------------------

The combination of both :ref:`user-manual-mode-procedure-historical-observations`
and :ref:`user-manual-mode-procedure-asteroid-on-sky-position` makes up the 
sum total of the asteroid observation record. Using this asteroid observation 
record, the future path of the asteroid on the sky can be determined to 
eventually allow for the proper acquisition. 

There are two different procedures for determining the future track of the 
asteroid:

- Propagating the on-sky motion of the asteroid into the future.
- Solving for the orbital elements and deriving an ephemeris.

Both options are sufficient but we recommend 
:ref:`user-manual-mode-procedure-asteroid-position-propagation`. 


.. _user-manual-mode-procedure-asteroid-position-propagation:

Asteroid Position Propagation
-----------------------------

.. _figure-manual-mode-gui-propagate:

.. figure:: /assets/images/manual-mode-gui-propagate.*

    The propagation GUI tab for customizing and executing propagation solutions.
    This is the default view before any values have been calculated.

Propagating the on-sky motion of the asteroid is done by taking the 
observational record from 
:ref:`user-manual-mode-procedure-asteroid-observation-record` and propagating 
only the most recent observations forward in time. See 
:numref:`figure-manual-mode-gui-propagate` for the interface for propagation 
solutions.

To solve for the propagation solution from the observations, you will need to 
select the desired propagation engine from the drop down menu then click on the 
:guilabel:`Solve Propagation` button to solve. 
(See :ref:`technical-architecture-services-engines` for more information on 
the available engines.)

If a propagation solution is done, the on-sky rates will be provided under 
:guilabel:`Propagate Rate [ "/s | "/s²]`. Both the first order (velocity) and 
second order (acceleration) on-sky rates in RA and DEC are given in arcseconds 
per second or arcseconds per second squared. The RA is given on the right and 
DEC on the left within the first or second order pairs. These rates may be 
sent to the TCS to update its non-sidereal rates vai the 
:guilabel:`Update TCS Rate` button after they are derived.

You may also provide a custom date and time, in the provided dialog box (using 
(`ISO-8601 like formatting <https://www.iso.org/standard/70907.html>`_). You 
can specify the timezone that the provided date and time corresponds to using 
the dropdown menu. When you click :guilabel:`Custom Solve`, the displayed RA 
and DEC coordinates are the estimated sky coordinates for the asteroid at the 
provided input time.

.. note::
    Execution of the propagation solution requires a completed astrometric 
    solution from 
    :ref:`user-manual-mode-procedure-find-asteroid-location-compute-astrometric-solution`.


.. _user-manual-mode-procedure-orbital-elements:

Orbital Elements
----------------

.. _figure-manual-mode-gui-orbit:

.. figure:: /assets/images/manual-mode-gui-orbit.*

    The orbit GUI tab for customizing and executing orbital solutions.
    This is the default view before any values have been calculated.

Provided a list of historical observations, we can solve for the Keplerian 
orbital elements using preliminary orbit determination for osculating elements.
See :numref:`figure-manual-mode-gui-orbit` for the interface for orbital 
solutions.

To solve for the orbital solution from the observations, you will need to 
select the desired orbit engine from the drop down menu then click on the 
:guilabel:`Solve Orbit` button to solve. 
(See :ref:`technical-architecture-services-engines` for more information on 
the available engines.)

The six Keplerian orbital elements (plus the epoch) are provided after the 
orbital solution is solved. They are:

- :guilabel:`SM-Axis`: The semi-major axis of the orbit, this is in AU.
- :guilabel:`Ecc.`: The eccentricity of the orbit, this is unit-less.
- :guilabel:`Incli.`: The inclination of the orbit, in degrees.
- :guilabel:`As-Node`: The longitude of the ascending node, in degrees.
- :guilabel:`Peri.`: The argument of perihelion, in degrees.
- :guilabel:`M-Anom.`: The mean anomaly, in degrees.
- :guilabel:`Epoch`: The epoch of these of these osculating orbital elements, in Julian days.

If the Engine provided is :guilabel:`Custom`, then you are trying to provide a 
custom orbit. You provide your Keplerian orbital parameters in the boxes. You 
may also specify the error in these elements by providing another number 
delimitated from the first by a letter. (Note, scientific notation is not 
supported, especially E-notation based entries.) After you provide your 
orbital parameters, you can click :guilabel:`Solve Orbit` to *solve* for your 
orbital solution.

.. note::
    Execution of the orbital solution requires a completed astrometric 
    solution from 
    :ref:`user-manual-mode-procedure-find-asteroid-location-compute-astrometric-solution`.


.. _user-manual-mode-procedure-ephemeris:

Ephemeris
---------

.. _figure-manual-mode-gui-ephemeris:

.. figure:: /assets/images/manual-mode-gui-ephemeris.*

    The ephemeris GUI tab for customizing and executing ephemeris solutions.
    This is the default view before any values have been calculated.

The orbital elements derived in :ref:`user-manual-mode-procedure-orbital-elements`
can then be used to derive an ephemeris of an asteroid. See 
:numref:`figure-manual-mode-gui-ephemeris` for the interface for ephemeris 
solutions.

To solve for the ephemeris solution from the orbital elements, you will need to 
select the desired ephemeris engine from the drop down menu then click on the 
:guilabel:`Solve Ephemeris` button to solve. 
(See :ref:`technical-architecture-services-engines` for more information on 
the available engines.)

If an ephemeris solution is done, the on-sky rates will be provided under 
:guilabel:`Ephemeris Rate [ "/s | "/s²]`. Both the first order (velocity) and 
second order (acceleration) on-sky rates in RA and DEC are given in arcseconds 
per second, or arcseconds per second squared. The RA is given on the right and 
DEC on the left within the first or second order pairs. These rates may be 
sent to the TCS to update its non-sidereal rates vai the 
:guilabel:`Update TCS Rate` button after they are derived.

You may also provide a custom date and time, in the provided dialog box (using 
`ISO-8601 like formatting <https://www.iso.org/standard/70907.html>`_). You 
can specify the timezone that the provided date and time corresponds to using 
the dropdown menu. When you click :guilabel:`Custom Solve`, the displayed RA 
and DEC coordinates are the estimated sky coordinates for the asteroid at the 
provided input time.

.. note::
    Execution of the ephemeris solution requires a completed orbital 
    solution from :ref:`user-manual-mode-procedure-orbital-elements` which 
    itself depends on a completed astrometric solution from 
    :ref:`user-manual-mode-procedure-find-asteroid-location-compute-astrometric-solution`.


.. _user-manual-procedure-asteroid-on-sky-future-track:

Asteroid On-Sky Future Track
----------------------------

Regardless of which method you use to derive the future track of the asteroid 
(either from :ref:`user-manual-mode-procedure-asteroid-position-propagation` or 
from :ref:`user-manual-mode-procedure-orbital-elements` and 
:ref:`user-manual-mode-procedure-ephemeris`), the future position of the 
asteroid and the on-sky rates are determined (see the respective sections 
for details). 


Telescope Control Software: Update
----------------------------------

The new asteroid on-sky future track (position and on-sky rates) derived from 
:ref:`user-manual-procedure-asteroid-on-sky-future-track` can be sent to the 
telescope control software to slew the telescope to the correct location of 
the asteroid.
