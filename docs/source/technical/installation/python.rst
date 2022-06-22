.. _technical-installation-python-part:

====================
Install: Python Part
====================

The Python part of OpihiExarata is the primary part of OpihiExarata. Luckily,
it is likely also the simplest.

You will build the Python wheel from the source and install it.

Download
========

Download and install a current release of Python if you have not already. You 
can find the latest releases at: `Python Releases`_.

Please note you must install/have Python 3.9+.

.. _Python Releases: https://www.python.org/downloads/

Build
=====

You should have have the repository code in ``OpihiExarata/``. You can 
run the build command (while in the directory) based on the operation system 
you are using:

Windows: ``python -m build``

Linux: ``python39 -m build``

The package will build into a distributable wheel, note in the output the 
version that you installed. The version is likely to be the day you built it, 
it affects the name of the wheel file for the next step.

Install
=======

Install the wheel package. 

You will need to modify this command to the proper wheel that you generated 
from before. Because this project using date-based versioning, your package 
will likely be that of the date that you build the wheel. 

(The ``--upgrade`` option is to ensure that you have the most up to date version.)

You can install the wheel using while in ``OpihiExarata/``::

    pip install ./dist/OpihiExarata-YYYY.MM.DD-py3-none-any.whl --upgrade