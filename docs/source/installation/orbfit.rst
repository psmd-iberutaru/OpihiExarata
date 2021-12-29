===============
Install: Orbfit
===============

Orbfit is one of the available asteroid orbit determiners. 

The instructions of installing Orbfit is derived from the 
`Orbfit installation documentation`_.

.. _Orbfit installation documentation: http://adams.dm.unipi.it/~orbmaint/orbfit/OrbFit/doc/help.html#install


Prerequisites
=============

There are a few prerequisites before the software can be installed.

Fortran Compiler
----------------

A Fortran compiler is needed to compile the software. Although there are many different 
compilers available, we document here how to use the Intel Fortran compiler. The method 
of install is OS dependent, or more specifically, package manager dependent. Other 
installation method exist, see `Intel Fortran compiler install`_ for more information 
(these instructions were derived from it).

Install
+++++++

Using package managers to install is the most convenient.

APT Package Managers
````````````````````
Download the Intel repository to the system keyring::

    # Downloading key...
    wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \
    | gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
    # Adding signed entry...
    echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list
    # Update the repository list...
    sudo apt update

Install the Intel Fortran compiler, the base toolkit is also needed as a requirement::

    sudo apt install intel-basekit
    sudo apt install intel-hpckit

It is highly suggested to update or install the following toolchains::

    sudo apt update
    sudo apt install cmake pkg-config build-essential

YUM, DNF, Zypper Package Managers
`````````````````````````````````
Download the Intel repository file and add it to the configuration directory::

    # Creating repository file...
    tee > /tmp/oneAPI.repo << EOF
    [oneAPI]
    name=Intel® oneAPI repository
    baseurl=https://yum.repos.intel.com/oneapi
    enabled=1
    gpgcheck=1
    repo_gpgcheck=1
    gpgkey=https://yum.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
    EOF
    # Moving the file to the directory...
    sudo mv /tmp/oneAPI.repo /etc/yum.repos.d
    # Update the repository list...
    sudo yum update

If you are using Zypper::

    # Creating repository file...
    sudo zypper addrepo https://yum.repos.intel.com/oneapi oneAPI
    rpm --import https://yum.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
    # Update the repository list...
    sudo zypper update

Install the Intel Fortran compiler, the base toolkit is also needed as a requirement::

    sudo yum install intel-basekit
    sudo yum install intel-hpckit

It is highly suggested to update or install the following toolchains::

    sudo yum update
    sudo yum -y install cmake pkgconfig
    sudo yum groupinstall "Development Tools"

For Zypper, both is done via::

    sudo zypper install intel-basekit
    sudo zypper install intel-hpckit
    sudo zypper update
    sudo zypper --non-interactive install cmake pkg-config
    sudo zypper --non-interactive install pattern devel_C_C++


Environment Variables
+++++++++++++++++++++

Set the environment variables for command-line development. This command sets the variables for the current session only. (For persistent environment variable set up, consider adding it to your startup script.)::

    . /opt/intel/oneapi/setvars.sh


.. _Intel Fortran compiler install: https://www.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-linux/top/installation.html