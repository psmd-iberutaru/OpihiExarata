.. _technical-installation:

============
Installation
============

The installation instructions are detailed here. For convenience, installation 
scripts have been written to install the software for choice operating systems. 
Currently, the supported operating systems are, in order, Rocky Linux, Windows, 
and Ubuntu. Future compatibility with other operating systems is unlikely to 
be supported in the future as this software package is purpose built. In order 
to get the scripts, and the software in general, you still need to download the 
software, see :ref:`technical-installation-download`.


.. _technical-installation-automated-scripts:

Automated Scripts
=================

As there are many parts to the OpihiExarata software, for convenience, an 
installation script has been written for convenience and to help facilitate 
installation. Please note that the automated script installs everything, if 
you want to customize your install, please see 
:ref:`technical-installation-manual-installation`.

The installation script is written in Powershell Core and thus require the 
installation of Powershell Core. Instructions for the installation and usage 
of `Powershell Core <https://docs.microsoft.com/en-us/powershell/>`_ can be 
found on Microsoft's website. The installation of the OpihiExarata software 
does not depend on Powershell Core after installation, but the convenience 
scripts would be unavailable. If this is the case, please follow the other 
installation instructions as usual.

In addition to the installation script, an auxillary script has been written in 
Powershell Core. The purpose of the auxillary script is to do tasks not 
strictly related to installation. These tasks include code formatting, 
testing, and documentation building. You may use this as well but it is not 
necessary for installation.

Script Usage
------------

A few elements of the scripts must be tuned to your current operating system. 
Editing a few lines in the beginning of each script file before running them 
is all that is needed.

For the installation script ``install.ps1``:

- You need to specify the version-specific Python command that Powershell Core uses to enter the correct Python interpreter. It is typically something like ``python3.9`` for Python 3.9, or something similar for other versions. (Windows operating systems, for example, is often just ``python``.) For example, the line in ``install.ps1`` should be something like::

    Set-Alias -Name pyox -Value python3.9

- If you are using a Linux system, you need to specify the primary flavor as different systems have different ways of installing packages. Set either ``$isCentOS`` or ``$isUbuntu`` to True based on what system you have. If the system detects that you have a Linux system and neither is specified, an error will be raised.

For the auxillary script ``auxillary.ps1``:

- Like the install script, you need to specify the version-specific Python command that Powershell Core uses. Typically it is typically something like ``python3.9`` for Python 3.9. It is advised that you use the same entry as in the installation script::

    Set-Alias -Name pyox -Value python3.9


.. _technical-installation-manual-installation:

Manual Installation
===================

Instructions are present for those who prefer a manual install, either because 
the installation script does not work or they want to customize their 
installation. 

The installation instructions must be followed in order. There are optional 
parts to the installation instructions, typically they are not needed for a 
feature complete install of OpihiExarata, but they are highly suggested. The 
installation order is as follows, we note what is optional and why:

1.  :ref:`technical-installation-download`: You will download the OpihiExarata package from its Github repository in this step.
2.  :ref:`technical-installation-python-part`: You will download a supported Python version and build then install the Python part of OpihiExarata and its dependencies. This part is the main part of installation.
3.  :ref:`technical-installation-documentation`: (Optional) You will build and process the documentation files to build the documentation for OpihiExarata. This is helpful if this set of documentation that you are reading is outdated or if you just want the documentation on your machine to be up to date.
4.  :ref:`technical-installation-windows-compatibility`: (Situational) Some of the services that OpihiExarata depends on only works for Linux. In order to have supported functionality on Windows, the OpihiExarata software leverages the Windows Subsystem for Linux. It is required that Windows users download and install this feature. The instructions are detailed here.
5.  :ref:`technical-installation-orbfit`: This installs the Orbfit preliminary orbit determiner program which OpihiExarata uses for orbit determination.


.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: Installation

   download
   python
   documentation
   windows
   orbfit