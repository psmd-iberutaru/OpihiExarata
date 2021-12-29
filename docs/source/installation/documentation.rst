=======================
Optional: Documentation
=======================

Building the documentation is relatively simple as we leverage Sphinx to build it.

Prerequisites
=============

Sphinx
------

To build the Sphinx documentation, Python needs to be installed (the Python version 
installed in this installation procedure can be used). 

The following packages must be installed::

    pip install sphinx sphinx-rtd-theme

LaTeX
-----

If a PDF version of the documentation is desired, Sphinx can build it via LaTeX. LaTeX 
must be installed. We suggest installing the `TeX Live distribution`_ and installing the 
full install. Instructions on how to install TeX Live is beyond the scope of this 
documentation.

_TeX Live distribution: https://tug.org/texlive/

Directory
---------

Change your directory to the ``OpihiExarata/docs`` directory, run all of the commands 
while within this directory.

Build
=====

First, the Python docstrings need to be processed into documentation. This can be done 
via running the script file: ``./docstring.cmd``

Second, the documentation can be built using the batch/makefile using the command: ``make <type>``. The ``<type>`` should be replaced with the type of output desired, suggestions below:

* ``html`` A collection of webpages ordered and structured. This is the suggested method.
* ``singlehtml`` A single HTML page; useful when sending the documentation between devices.
* ``latexpdf`` A PDF compiled by built LaTeX files. Using this option invokes the entire toolchain for you.

The documentation can be built to other different forms, see the 
`sphinx-build documentation`_.

_`sphinx-build documentation`: https://www.sphinx-doc.org/en/master/man/sphinx-build.html
