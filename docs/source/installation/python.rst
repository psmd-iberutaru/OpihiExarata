=========================
Installation: Python Part
=========================

The Python part of OpihiExarata is the primary part of OpihiExarata. Luckily,
it is likely also the simplest.

You will build the Python wheel from the source and install it.

.. warning::
    This should be the last part of OpihiExarata that should be installed. All
    parts of OpihiExarata *must* be installed in order for it to work properly.
    Return to this part only after completing all other parts of the installation.

Build
=====

You should have already have the repository code in ``OpihiExarata/``. You can 
run the build command based on the operation system you are using:

Windows: ``py -m build``

Linux: ``python3 -m build``

The package will build into a distributable wheel, note in the output the version
that you installed. The version is likely to be the day you built it, it affects
the name of the wheel file for the next step.


Install
=======

Install the wheel package. You will need to modify this command to the proper 
wheel that you generated from before. Because this project using date-based 
versioning, your package will likely be that of the date that you build the 
wheel. (Force reinstall is optional but suggested to ensure you have the most 
up-to-date version.)

You can install the wheel using::

    pip install ./dist/OpihiExarata-YYYY.MM.DD-py3-none-any.whl --force-reinstall