.. _user-index:

===========
User Manual
===========

This is the user manual portion of the OpihiExarata software package for 
reducing and analyzing Opihi data.

The Opihi telescope is a smaller telescope mounted on the side of the IRTF. It 
primarily provides asteroid view-finding and photometric calibration services. 

It was conceived to assist the IRTF telescope and its instruments in finding 
asteroids and other near Earth objects on the sky. This is needed when the 
positional uncertainty in the ephemeris of these objects are greater than the 
field of view of the IRTF's current acquisition and tracking instruments 
(about 1 arcminuite). This can often be the case for newly discovered objects 
with a small number of observations. With Opihi's 32 arcminuite field of view, 
these objects can be spotted and the telescope pointing can be corrected, thus 
greatly reducing the overhead time of finding the target.

However, a minority of time allocated by the IRTF are for these types of 
targets. Having Opihi only operate a few times a semester when it is needed 
for acquisition is inefficient. In addition to the asteroid view-finding 
capabilities, the Opihi telescope also serves as a source for photometric
monitoring and calibration. By continuously taking pictures and determining the
photometric solution for each, the photometric conditions (as measured by 
the zero point magnitude) can be monitored over time. Moreover, this 
photometric data can also be used to assist with photometrically calibrating 
science targets observed by other IRTF facility instruments (e.g. SpeX, MORIS, 
SPECTRE, etc).

A more detailed description of the physical and optical specifications of the 
Opihi telescope can be found in :ref:`user-opihi-telescope`.

It is typical for the asteroid view-finding to be done manually by either a 
telescope operator or an observing astronomer; for this reason, we may refer 
to this view-finding mode as the :ref:`user-manual-mode` of operation for 
Opihi and OpihiExarata. 

The photometric monitoring mode does not require the constant 
input from a user, it only requires instructing the Opihi camera to 
continuously take images and for the software (OpihiExarata) to continuously 
solve for their respective photometric solutions; for this reason, we may 
refer to this photometric monitoring mode as the :ref:`user-automatic-mode` 
of operation for Opihi and OpihiExarata.

Photometric monitoring may be done manually if the user desires more control 
over the process. However, asteroid view-finding cannot be done automatically. 
It is currently beyond the scope of this software to implement automatic 
asteroid/transient finding.

An astronomer or other user interacts with the Opihi telescope and the 
OpihiExarata software by connecting to a VNC session; `this is common to all 
IRTF instruments <http://irtfweb.ifa.hawaii.edu/observing/computer/vnc.php>`_. 
The Opihi camera controller has an interface and data viewer independent of 
the interfaces of OpihiExarata.

For the general user, the OpihiExarata presents itself with helpful graphical
user interfaces (GUIs). However, a command-line interface is provided to 
open these GUIs. It is likely that most users do not need to worry about this
interface as the GUI may already be open for them in the VNC session, however,
the command-line interface and its usage is documented in 
:ref:`user-command-line`. 

See :ref:`user-manual-mode` or :ref:`user-automatic-mode` for usage instructions
depending on the desired mode of operation. Both of these have some technical 
jargon better described in :ref:`user-system-framework`. See 
:ref:`user-configuration` for the available configuration options of both 
modes. If you are having trouble, see :ref:`user-troubleshooting` for more
information and possible solutions. If you believe you found an issue or bug 
with the software, please report it to the appropriate IRTF staff member(s). 

If you used the Opihi telescope or the OpihiExarata software, please 
acknowledge your usage in any projects or publications; see 
:ref:`user-citations` for assistance and for our own references.


.. toctree::
    :maxdepth: 3
    :hidden:
    :caption: User Manual

    opihi_telescope
    system_framework
    command_line
    manual_mode
    automatic_mode
    configuration
    recording_fits_file
    troubleshooting
    citations
    trivia