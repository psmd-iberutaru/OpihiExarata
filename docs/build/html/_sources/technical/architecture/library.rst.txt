.. _technical-architecture-library:

=======
Library
=======

Here we provide a brief summary of the available functionality provided by the 
software library of OpihiExarata. The whole point of the library is to store 
functions and subroutines which are useful across the entire software 
package.

When developing and maintaining OpihiExarata itself, please utilize the library
before implementing something custom. If the library is incomplete, and the 
missing functionality would likely be used again at least once, please add it 
to the library and call it from there. The library does not typically 
reimplement functionality already implemented by third-party package 
dependencies; however, there may be some wrapper functions to streamline 
the capabilities thereof to better fit the use cases for OpihiExarata.

The summaries provided here do not substitute a search through the 
:ref:`home-code-manual`, but hopefully they help in searching for library
functionality.


Configuration
=============

See :py:mod:`opihiexarata.library.config`.

The implementation of configuration parameters is done via this module. 

When a user specifies a configuration file to be applied to this software, the 
file is loaded and its parameters and values are loaded into the the 
namespace of this module. Therefore, the software internally can call these 
configurations as variables in this module; an example, 
:code:`opihiexarata.library.config.LYCANROC` would correspond to the 
``LYCANROC`` configuration parameter in the configuration YAML file.

Both normal configuration parameters and secret parameters (detailed in 
:ref:`user-configuration`) are taken from their respective files and placed 
into this same namespace. Therefore, all of the configuration parameters must 
be uniquely named.

The loading and applying of a configuration file (either secret or not), 
provided by the user via regular methods, is done via 
:py:func:`opihiexarata.library.config.load_then_apply_configuration`. Note that 
this will only apply the configuration to the current Python session.


.. _technical-architecture-library-conversion:

Conversion
==========

See :py:mod:`opihiexarata.library.conversion`.

All types of required conversions are implemented here. The OpihiExarata 
software has specific conventions (see :ref:`technical-conventions`) for units
so that data may be better easily exchanged. However, some of these values 
needs to be converted for various reasons and so the conversions are 
implemented here.

Functions for converting between Julian day (convention) to other various 
formats are implemented.

Functions for formatting RA and DEC from degrees (convention) to sexagesimal 
string formatting are implemented. Specifically formatted sexagesimal can also 
be converted back to degrees.

Functions related to the conversion of different (but equivalent) names for 
things like filter or engine names are also provided.


Engines
=======

See :py:mod:`opihiexarata.library.engine`.

Base classes for different engines and solution implementations exist here. 
They are typically subclassed for the actual implementation of the engines 
(:ref:`technical-architecture-services-engines`) and solutions 
(:ref:`technical-architecture-vehicles-solutions`). These are also useful for 
type checking.


Error
=====

See :py:mod:`opihiexarata.library.error`.

Error exceptions specific to OpihiExarata are created here. All errors that 
come from OpihiExarata (either directly or indirectly) should be defined here. 
Using built-in Python errors is not suggested as using an error here helps 
specify that the issue comes from OpihiExarata.


FITS File Handing
=================

See :py:mod:`opihiexarata.library.fits`.

This implements functions which assist in the reading and writing of image and 
table FITS files. Astropy has a lot of functionality for this, and these 
functions wrap around their implementation so that it is more specialized for 
OpihiExarata and so that the reading and writing of FITS files are uniformly 
applied across the software.


.. _technical-architecture-library-hint:

Type Hinting
============

See :py:mod:`opihiexarata.library.hint`.

Python is a dynamically typed language. However it implements type hints 
(see :pep:`483` and :pep:`484`) so that text editors and other development 
tools and features can be more accurate and detailed. OpihiExarata uses type 
hints throughout and highly recommends their usage. However, to avoid 
extremely long object calls and unnecessary importing, object types that 
would otherwise need to be imported to be used are instead all imported into 
this one namespace to be used across the codebase.


HTTP Calls
==========

See :py:mod:`opihiexarata.library.http`.

Some of the functionality of OpihiExarata requires the use of HTTP APIs. 
Although a lot of the HTTP web functionality is implemented outside of this 
library where specifically needed (because of the unique nature of each 
process), there are some functions common among them which are implemented 
here.


Image Array Processing
======================

See :py:mod:`opihiexarata.library.image`.

Opihi is an imaging telescope and images are often represented as arrays. 
However, there are some functionality that make sense in terms of images but 
have more involved implementations when using arrays as images. Functions 
here implement common manipulations of images represented as arrays.


JSON Parsing
============

See :py:mod:`opihiexarata.library.json`.

Although OpihiExarata prefers YAML formatting for configuration files and 
other data serializations, JSON is another popular format which is used by 
some of the services OpihiExarata relies on. Thus some JSON functionality
is implemented here as wrapper functions.


Minor Planet Center Records
===========================

See :py:mod:`opihiexarata.library.mpcrecord`.

One of the most ubiquitous ways of representing an observation of an asteroid 
is using the 
`MPC 80-column foarmat record <https://www.minorplanetcenter.net/iau/info/OpticalObs.html>`_.
However, it is not a very connivent format for Python to use and so 
functions which convert between the 80-column format and an Astropy table 
(see :py:mod:`astropy.table`, or more specifically, 
:py:class:`astropy.table.Table`). In general, the table format is better for 
internal manipulation while the 80-column format is used primarily to record 
and send asteroid observations to other services (including, obviously, the 
Minor Planet Center).


File and Directory Path Manipulations
=====================================

See :py:mod:`opihiexarata.library.path`.

Path and filename manipulations are common across all aspects of OpihiExarata.
For uniform application and convenience, common path manipulations are 
implemented here. This only has implementations for where the filepaths are 
strings and not objects. 


Photometric and Astrometric Data Handing Table
==============================================

See :py:mod:`opihiexarata.library.phototable`.

The astrometric solution and the photometric solution 
(see :ref:`technical-architecture-vehicles-solutions`) both have a lot of 
similar information in tables. Older versions of this software had two 
different tables which were very unwieldy as progress continued. As such, 
this class implements a photometry table which is more coherent and 
comprehensive to better harmonize the interplay between the astrometric and 
photometric solutions. Feature expansion in this region is unlikely.

Telescope Control Software
==========================

See :py:mod:`opihiexarata.library.tcs`.

It is important for the OpihiExarata software to talk to the telescope 
control software to give it the needed information to correct the pointing. It
is unnecessary to always bother the telescope controller and so functions 
which call and execute the telescope control software are written here. Only 
those functions which are needed for OpihiExarata are implemented. The 
implementation is specific for the IRTF TCS and it requires the installation 
of the t3io software.


Temporary Directory
===================

See :py:mod:`opihiexarata.library.temporary`.

Sometimes the OpihiExarata software needs to save temporary files when 
processing data and reading the results. In order for these files not to 
mess up anything on the system this software is installed on, a temporary 
directory is created where the files can be created and utilized. The exact 
place where this directory is created is given by the configuration parameter 
``TEMPORARY_DIRECTORY`` (see :ref:`user-configuration`) Functions implemented 
here help with the management of this temporary directory.