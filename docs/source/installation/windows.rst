===============================
Optional: Windows Compatibility
===============================

Many of the parts of OpihiExarata are built for Linux-only operating systems. 
However, Windows can use a Linux subsystem to call the compiled Linux parts, allowing
OpihiExarata to run on Windows, with a set of assumptions.

When a Linux call is needed, the software calls it via the Windows Subsystem for Linux 
(WSL) using Powershell. Thus WSL must be installed and Powershell must have script mode 
enabled.


Powershell Execution Policy
===========================

Powershell scripts are seen as the most reliable way to call WSL on Windows. But,
the default execution policy of most Windows machines disable scripts. To enable 
scripts, do the following command in an administrator Powershell shell::

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned

See Microsoft's documentation for more information on 
`setting Powershell execution policies`_ and `what policies are available`_.

.. _setting Powershell execution policies: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy
.. _what policies are available: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies


Windows Subsystem for Linux
===========================

As the WSL system is slightly new, the steps to install it differ based on what version 
of Windows is installed.

For Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11 and higher, 
see `Modern Install`_.

For older versions of Windows 10 (version 1903 or higher, with build 18362 or higher), see `Manual Install`_.

OpihiExarata does not support or is designed to run on older versions of Windows.

Modern Install
--------------

In newer Windows versions (Windows 10 version 2004 and higher (Build 19041 and higher) or 
Windows 11), the installation of WSL is relatively simple. 

In an administrator Powershell, run the following::

    wsl --install

This installs Ubuntu as the WSL distribution by default. See the 
`WSL install documentation`_ for more information.

.. _WSL install documentation: https://docs.microsoft.com/en-us/windows/wsl/install


Manual Install
--------------

These installation instructions was taken from the `manual installation documentation`_ 
from Microsoft.

**Enable WSL**

In an administrator Powershell, enable the WSL system via::

    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

**Enable Virtual Machine Feature**

In an administrator Powershell, enable the virtual machine platform::

    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

**Download Linux Kernel Update Package**

You can download the latest kernel package from: 
`WSL2 Linux kernel update package for x64 machines`_.

Run the downloaded package; you will likely be prompted for administrative permissions.

**Set WSL 2 as Default**

In an administrator Powershell, use the following command to set WSL 2 as the default version::

    wsl --set-default-version 2

This the more typical WSL installation, rather than WSL 1 which is a compatibility layer.

**Download Linux Distribution**

Download your desired Linux distribution from the Windows store, we suggest `WSL Ubuntu`_:


.. _manual installation documentation: https://docs.microsoft.com/en-us/windows/wsl/install-manual

.. _WSL2 Linux kernel update package for x64 machines: https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi

.. _WSL Ubuntu: https://www.microsoft.com/store/apps/9n6svws3rx71


Verify
======

To verify that that the Powershell execution policy is correct, check that the Local 
Machine policy is at least RemoteSigned. You can check this by using an administrative 
Powershell command::

    Get-ExecutionPolicy -List

To verify that you have installed and set up WSL properly, in an administrative Powershell run::

    wsl

If this is the first time you have installed the WSL system onto your computer, you will 
have to setup a user account similar to a fresh install. Follow and complete the prompt, 
and then check ``wsl`` again to ensure that it enters a standard Linux shell without any 
interruptions.

Final
=====

When installing other parts of the OpihiExarata software, follow the instructions using 
the WSL OS installed where needed. The commands should be run in your usual WSL shell in 
the proper relevant directory.