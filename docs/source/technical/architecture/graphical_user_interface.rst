.. _technical-architecture-graphical-user-interface:

========================
Graphical User Interface
========================

The graphical user interface (GUI) makes use of PySide6 which itself is a
Python implementation of the Qt 6 GUI framework.

We use PySide6 as opposed to PyQt 6 because of licensing preferences and 
because PySide is developed by the Qt Company (the first party) and so it is 
likely to be supported for longer.

(The PySide6 is LGPL licensed. Qt Designer is GPL licensed but we only use it 
as a connivent tool and do not bundle or have our program require it. As far 
at PySide6 is concerned, we are dynamically linking it and are bound only by 
LGPL.)

The exact shape and form of the GUIs are a byproduct of the feature sets in 
:ref:`user-manual-mode` and :ref:`user-automatic-mode`. The interface is 
optimized to those use cases and does not otherwise follow a rigid theme. 


Qt Designer
===========

To design the GUIs, we use 
`Qt Designer <https://doc.qt.io/qt-6/qtdesigner-manual.html>`_ as it is an 
easy interface. This program can be downloaded via the 
`Qt installer <https://doc.qt.io/qtdesignstudio/studio-installation.html>`_. 
Qt Designer does not need to be installed on the same machine as it just 
generates the GUI design files.

When installing Pyside6, Qt Designer often is included and can be invoked by::

    pyside6-designer

The GUI design files are saved in the 
:file:`/OpihiExarata/src/opihiexarata/gui/qtui/` directory typically as 
something akin to :file:`manual.ui`. These files may be opened by Qt Designer 
and modified as needed.


.. _technical-architecture-graphical-user-interface-building-ui-files:

Building UI Files
=================

It is part of development (not installation) to develop the Python versions of
the GUI files. The UI files created via Qt Designer can be converted to their 
Python versions using :command:`pyside6-uic`. (See 
`Qt's documentation <https://doc.qt.io/qtforpython/tutorials/basictutorial/uifiles.html#using-ui-files-from-designer-or-qtcreator-with-quiloader-and-pyside6-uic>`_ 
for more information.)

The UI files are stored in :file:`/OpihiExarata/src/opihiexarata/gui/qtui/`
and it is expected that the generated Python equivalent files will also be 
written there as :file:`qtui_*.py`, where the original UI filename fills the 
wildcard.

For example, for a file :file:`manual.ui`, it can be converted to the proper 
Python version using the command::

    pyside6-uic manual.ui > qtui_manual.py

Every UI file should be turned into their respective Python version. A 
Powershell Core script has been written to automate this process. It can be 
found in the same directory and is executed by::

    pwsh build_qtui_window.ps1