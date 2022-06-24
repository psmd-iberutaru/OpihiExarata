.. _user-configuration:

=============
Configuration
=============

There are many different configuration options available to the user to 
modify the OpihiExarata software. The configuration options are split into 
two different configuration files, detailed here.

If these configuration files to not exist on the system, you can generate a 
new configuration file, which contains the defaults, using the 
:option:`generate` action from the command-line interface, see :ref:`user-command-line-available-actions-generate`.


.. _user-configuration-standard-configuration-file:

Standard Configuration File
===========================

A standard configuration file (simplified to configuration file), typically 
called something like :file:`configuration.yaml`, is where most of the 
configuration parameters for all aspects of the OpihiExarata software package 
exists.

The configuration file is a YAML formatted file with relatively verbose names.
A newly generated configuration file is a copy of the default file being used.

To detail all of the configuration parameters here is not particularly 
efficient. The parameters are documented in the configuration file itself. 
It can be found at :file:`OpihiExarata/src/opihiexarata/configuration.yaml` in 
the directory tree. Alternatively, it can also be found 
`here on the OpihiExarata Github, configuration.yaml <https://github.com/psmd-iberutaru/OpihiExarata/blob/master/src/opihiexarata/configuration.yaml>`_.



.. _user-configuration-secrets-configuration-file:

Secrets Configuration File
==========================

A secrets configuration file (simplified to secrets file), typically 
called something like :file:`secrets.yaml`, is where configuration parameters 
which should not be released to the public (via open source) are kept, hence a 
secrets file. These are often software and API keys.

The secrets file is a YAML formatted file with relatively verbose names.
A newly generated secrets file is a copy of the default file being used. But, 
there are no defaults and the secrets are blank as that is the whole point of 
a secrets file. They need to be filled in with a user provided secrets file.

To detail all of the secrets parameters here is not particularly efficient. 
The secrets themselves are documented in the secrets file itself. It can be 
found at :file:`OpihiExarata/src/opihiexarata/secrets.yaml` in the directory tree. 
Alternatively, it can also be found `here on the OpihiExarata Github, secrets.yaml <https://github.com/psmd-iberutaru/OpihiExarata/blob/master/src/opihiexarata/secrets.yaml>`_. 