.. _technical-architecture-monitor-database:

================
Monitor Database
================

One of the functionalities of the Opihi telescope is to record and monitor 
the atmospheric conditions over time. This functionality is similar to the 
`CFHT SkyProbe <https://www.cfht.hawaii.edu/Instruments/Elixir/skyprobe/home.html>`_.

In both :ref:`user-manual-mode` or :ref:`user-automatic-mode`, OpihiExarata can 
save zero point data obtained from solving the photometric solution of an 
image. (See :ref:`user-manual-mode-procedure-find-asteroid-location-compute-photometric-solution` 
for computing the photometric solution in manual mode, and :ref:`user-automatic-mode` 
generally for computing the photometric solution in automatic mode.) We save 
the zero point information in a database.


Database Schema
===============

The layout of a database is typically described by the database schema. For 
our purposes, we find that a flat file database is the simplest to understand 
for those unfamiliar with OpihiExarata itself. Although typically a general 
user will interact with this database through the output of the monitoring 
webpage (see :ref:`user-zero-point-monitoring`), there may be the case where 
the full data is needed.

The database is a flat text file database following the following hierarchy:

1.  All database files are stored in a single directory. To mark that it is an OpihiExarata database directory, a blank file `exarata_zero_point_database.check` exists. This file is made upon a new database directory and is required.
2.  Each file of the database represents a single day of data. The filenames are given as `YYYY-MM-DD.txt` where the date is the UTC date of a given zero point observations.
3.  Each line within a given file of the database is a single zero point observation. The UTC time and date (in ISO 8601 format) is provided along with the zero point value, error, and name of the filter per :ref:`technical-conventions-filter-names`.

Managing the Database
=====================

The database is custom to this software and so the API which manages it is 
also native to OpihiExarata. The database is managed with an instance of the 
database solution class found. (For more information, see 
:ref:`technical-architecture-vehicles-solutions-opihizeropointdatabasesolution`.)

As records are appended to the files of the database, some records may get out 
of order. The API interface provides methods to clean up the database. 

The location and other interactions between the database and the other parts of 
the OpihiExarata software is configurable via the configuration file, see 
:ref:`user-configuration-standard-configuration-file`.