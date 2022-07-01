.. _user-command-line:

============
Command Line
============

The OpihiExarata software system should already be installed on the computer 
Opihi operates off of. (If that is not the case, consult 
:ref:`technical-installation` for more information or contact a staff member.) 
To test that OpihiExarata is installed on the system, you can run the 
following in a terminal::

    opihiexarata

This should print a help menu of sorts. 

The general overview of the command-line syntax of this command is::
    
    opihiexarata [action] [options]

Where :option:`[action]` is the specified actions to take. There are many 
actions which the command-line interface may execute. The currently available 
actions are detailed in :ref:`user-command-line-available-actions`. 

Different command-line options, :option:`[options]`, are detailed in :ref:`user-command-line-available-options`. The options detailed are all 
optional. The only mandatory input is the required action to take.


.. _user-command-line-available-actions:


Available Actions
=================

.. option:: [action]

Here we list the available actions for the command-line interface, ordered by 
(approximately) the order of importance each command is to the average user.

Note that there are aliases for different actions for ease of use, they
are all listed here.

.. _user-command-line-available-actions-manual:


Manual
------

.. option:: manual, m

This opens up the manual mode GUI. This is used when the user wants to 
utilize the manual (asteroid view-finding) of Opihi and OpihiExarata. Or, 
alternatively, the user wants to manually operate the photometric monitoring 
mode.

.. _user-command-line-available-actions-automatic:


Automatic
---------

.. option:: automatic, auto, a

This opens up the automatic mode GUI. This is used when the user wants to 
utilize the automatic (photometric monitoring) mode of Opihi and OpihiExarata.
Typically, this user would be a telescope operator.

.. _user-command-line-available-actions-generate:


Generate
--------

.. option:: generate, g

This generates configuration files to allow a user to edit and customize the 
functionality of OpihiExarata. There are two different configuration files.
Which type of configuration file, and where it is saved are determined by the 
specification of the optional parameters 
For more information about configuration and configuration files, see 
:ref:`user-configuration`. 


.. _user-command-line-available-actions-help:

Help
----

.. option:: help, h

This displays the help dialog in the terminal. It is identical to the 
:option:`--help` option or invoking :command:`opihiexarata` without any 
specified action.


.. warning::
    If any action is specified that does not match any of the expected actions, 
    the program will raise a Python exception as opposed to ignoring it or 
    raising a shell error.


.. _user-command-line-available-options:


Available Options
=================

.. option:: [options]

Here we list the available actions for the command-line interface, ordered by 
(approximately) the order of importance each command is to the average user.

Note that there are aliases for different actions for ease of use, they
are not listed here. Instead, the overall preferred syntax and formatting 
is provided. To see the aliases, see the help screen for more information:
:ref:`user-command-line-available-actions-help`.


Help
----

.. option:: --help

This overrides any specified actions and executes the help dialog. See 
:ref:`user-command-line-available-actions-help`.


Manual
------

.. option:: --manual

This opens up the manual mode GUI regardless of the action specified. See :ref:`user-command-line-available-actions-manual`.


Automatic
---------

.. option:: --automatic

This opens up the automatic mode GUI regardless of the action specified. See :ref:`user-command-line-available-actions-automatic`.


.. _user-command-line-available-options-configuration:

Configuration
-------------

.. option:: --config=<path/to/config.yaml>

This specifies the path of the configuration file. The configuration file is 
in a YAML format. If the action specified is :option:`generate`, then this is 
the path where the generated configuration fill will be saved. Otherwise, the 
program will read the configuration file at this path and use its values 
instead of the program's defaults, where they differ. 

See :ref:`user-configuration-standard-configuration-file` for the 
specifications of the configuration file.


.. _user-command-line-available-options-secrets:

Secrets
-------

.. option:: --secret=<path/to/secret.yaml>

This specifies the path of the secrets file. The secrets file is 
in a YAML format. If the action specified is :option:`generate`, then this is 
the path where the generated secrets fill will be saved. Otherwise, the 
program will read the secrets file at this path and use its values 
instead of the program's defaults, where they differ. 

See :ref:`user-configuration-secrets-configuration-file` for the 
specifications of the secrets file.


Overwrite
---------

.. option:: --overwrite

This option allows for the specification of what to do when a provided 
file at a path already exists. This is typically used when generating new 
configuration files. When provided, any pre-existing files are overwritten.
The default, when this option is not provided, is to raise an error because a 
file already exists at a given path.


Keep Temporary
--------------

.. option:: --keep-temporary

The normal operation of OpihiExarata requires the writing of temporary files.
A temporary directory is created (as specified by the configuration file) and 
is then purged and deleted. Using this flag prevents the cleanup of the 
temporary directory on the program's exit. However, as the software itself 
often cleans up after itself periodically during usage, this option is not 
very useful for the end user. It is more for debugging purposes.



.. warning::
    If any option is specified that does not match any of the expected option, 
    the program will raise a shell error.