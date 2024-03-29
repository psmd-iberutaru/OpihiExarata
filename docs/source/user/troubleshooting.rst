.. _user-troubleshooting:

===============
Troubleshooting
===============

For all of your troubleshooting needs. Here we detail some of the common 
problems encountered and the solutions for these problems.


.. _user-troubleshooting-automatic-mode-stop-button-not-working:

Automatic Mode Stop Button Not Working
======================================

If the :guilabel:`Stop` button in the automatic mode GUI is not working and 
fails to stop the loop as designed, then this is likely because of an oversight 
when the code was changed. The loop will run forever until stopped as per the 
design of the automatic mode.

You can force the loop to stop gracefully by creating a file named 
:file:`opihiexarata.stop` in the same data directory that the 
automatic loop is fetching the most recent images from. The loop checks for the 
existence of this file and it will stop in a similar way to if the stop button 
was pressed. The loop will be considered :guilabel:`Halted` as it stopped via 
a method other than the :guilabel:`Stop` button.

If this fails, then the suggested remedy is to ungracefully stop or crash the 
process that OpihiExarata is running in. 

In either case, this is an error with the code of OpihiExarata and the 
maintainers of the software should be contacted.

.. _user-troubleshooting_oserror_too_many_open_files

OSError Too Many Open Files
===========================

Sometimes there is an issue where there are too many open files. This happens 
due to Astropy using memory mapping for reading FITS files. The references 
are not actually terminated and because of this it reaches the Linux file limit.
See the `Astropy FAQ`_. 

OpihiExarata should already have a memory mapping disabled and some mitigation 
to avoid this issue. However, the effectiveness and pitfalls of the mitigation 
is not fully understood. Hence this troubleshooting entry.

A temporary fix if this issue ever occurs is to close the OpihiExarata window
and optionally restart the terminal session/window it is in.

.. _Astropy FAQ: https://docs.astropy.org/en/stable/io/fits/appendix/faq.html#i-am-opening-many-fits-files-in-a-loop-and-getting-oserror-too-many-open-files

.. _user-troubleshooting-pyside-gui-does-not-match-documentation-or-ui-files:

PySide GUI Does Not Match Documentation or UI Files
===================================================

This problem can be caused by one of two things. 

If the documentation and the GUI differs, then the documentation may be out of 
date. Otherwise, the Python GUI files built by PySide6 are out of date and 
need to be built again.

If the documentation is out of date, see 
:ref:`technical-installation-documentation` for rebuilding up to date 
documentation. If information is missing, please contact the maintainers to 
update the documentation.

If the GUI differs from the Qt Designer UI files, then the Python UI needs to 
be built from these files. See 
:ref:`technical-architecture-graphical-user-interface-building-ui-files` for 
more information.