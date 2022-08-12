.. _user-recording-fits-file:

===================
Recording FITS File
===================

The results from the procedures and calculations performed by the engines and 
corresponding solution classes (via the processes of :ref:`user-manual-mode` 
or :ref:`user-automatic-mode`) are primarily stored in the header of a FITS 
file. We copy the original to preserve it and save it with all of the 
information from OpihiExarata.

Although all of the possible headers are added, only information that 
can be added will be added. Otherwise, for entries which does not have any 
information to be saved, they are left blank and added only as a filler 
entry. (We do this to preserve the order of the header cards in the event 
additional information is added or overwritten to the header.)

Header Naming Convention
========================

In order to prevent name conflicts, and to have some resemblance of order, 
header keywords have a specific naming convention. As FITS header keywords 
are typically limited to 8 characters, we have the convention as follows.

- All keywords follow the following convention: ``OX@+++++``.
- To prevent collisions, we use the ``OX`` as a prefix to identify the keyword namespace which OpihiExarata will use.
- We group similar results together using a single letter character at ``@``. They are:
    - ``_``: Reserved for the beginning and ending cards.
    - ``T``: Specific information about the asteroid/target itself. 
    - ``M``: Specific metadata information.
    - ``A``: Results related to astrometry.
    - ``P``: Results related to photometry.
    - ``O``: Results related to orbital solutions.
    - ``E``: Results related to ephemerides.
    - ``R``: Results related to propagation calculations.
- The rest of the five characters ``+++++`` delimitate what the entry is about. As it is only five characters, the descriptions are very abbreviated. 
    - FITS header comments supplement. They are also a little brief to prevent their truncation because of the total character limit of FITS headers.
    - There are a few additional conventions in this region. A non-exhaustive list of common ones are:
        - Where possible, the keyword is kept to be 8 characters long, underscores fill what would otherwise be spaces.
        - For values with errors, typically if the value was solved via an engine, it is marked as ``++++S``. If it was derived from other solved values it is marked as ``++++D``. The errors are typically given with ``++++E``.
        - For non-sidereal rates, the first order rates in RA and DEC are called "velocity" and are marked as ``++++V``. Second order rates, "acceleration", are marked as ``++++A``.