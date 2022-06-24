.. _technical-installation-orbfit:

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

Directory
---------

Enter into a directory which is accessible and usable by programs. In this 
documentation, we will call this directory :file:`Orbfit/`. You should do the 
commands of this section of the installation documentation within this 
directory.

Dependencies
------------

The following dependencies should be installed. The installation of these are 
dependent on the package manager and operating system used.

For APT-based systems::

    sudo apt install gcc make curl time

For YUM, DNF, or Zypper based systems::

    sudo yum install gcc make curl time

Fortran Compiler
----------------

A Fortran compiler is needed to compile the software. Although there are many 
different compilers available, we document here how to use the Intel Fortran 
compiler. The method of install is OS dependent, or more specifically, package 
manager dependent. Other installation method exist, see 
`Intel Fortran compiler install`_ for more information (these instructions were 
derived from it).

Install
~~~~~~~

Using package managers to install is the most convenient.

APT Package Managers
++++++++++++++++++++
Download the Intel repository to the system keyring::

    # Downloading key...
    wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \
    | gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
    # Adding signed entry...
    echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list
    # Update the repository list...
    sudo apt update

Install the Intel Fortran compiler, the base toolkit is also needed as a 
requirement::

    sudo apt install intel-basekit
    sudo apt install intel-hpckit

It is highly suggested to update or install the following toolchains::

    sudo apt update
    sudo apt install cmake pkg-config build-essential

YUM, DNF, Zypper Package Managers
+++++++++++++++++++++++++++++++++
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

Install the Intel Fortran compiler, the base toolkit is also needed as a 
requirement::

    sudo yum install intel-basekit
    sudo yum install intel-hpckit

It is highly suggested to update or install the following toolchains::

    sudo yum update
    sudo yum install cmake pkgconfig
    sudo yum groupinstall "Development Tools"

For Zypper, both is done via::

    sudo zypper install intel-basekit
    sudo zypper install intel-hpckit
    sudo zypper update
    sudo zypper install cmake pkg-config
    sudo zypper install pattern devel_C_C++


Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Set the environment variables for command-line development. This command sets 
the variables for the current session only. (For persistent environment 
variable set up,consider adding it to your startup script.)::

    . /opt/intel/oneapi/setvars.sh

.. _Intel Fortran compiler install: https://www.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-linux/top/installation.html


Download OrbFit
===============

The software needs to be downloaded. 

You can likely find the software package on the `OrbFit website`_. Otherwise, 
a download command may work::

    curl -O http://adams.dm.unipi.it/orbfit/OrbFit5.0.7.tar.gz

And it can thus be extracted::

    tar -xvzf OrbFit5.0.7.tar.gz

.. _OrbFit website: http://adams.dm.unipi.it/orbfit/


Compile
=======

To configure the compilation flags, OrbFit comes with a set of files which 
describe the flags. Initialize the proper compilation flags via the 
:command:`config` command, (flags for an optimized build using the Intel 
compiler)::

    ./config -O intel

The generated compilation flags, however, needs to be changed. The generated 
compilation flags can be found in the file :file:`Orbfit/src/make.flags`, as 
generated by the :command:`config` script. The options should be 
(see `Intel Fortran compiler options`_ for more information)::

    FFLAGS= -warn nousage -O -mp1 -static-intel -save -assume byterecl -I../include

.. note::
    You make use the default compilation flags as well; the change to the 
    flags just allows the program to run with the Intel Fortran libraries 
    statically compiled with the program rather than linked in. This alleviates 
    the need for always needing to set up the environment variables whenever 
    OrbFit is run. The changing memory model does not seem to affect the orbit 
    determination part of the program.

.. _Intel Fortran compiler options: https://www.intel.com/content/www/us/en/develop/documentation/fortran-compiler-oneapi-dev-guide-and-reference/top/compiler-reference/compiler-options/alphabetical-list-of-compiler-options.html 

Finally the program can be compiled using the makefile::

    make

The compiled programs should exist in :file:`Orbfit/bin/`.


Download JPL Ephemerides File
=============================

The OrbFit package uses the JPL ephemerides file for its calculations, it 
requires the binary ephemerides files. Current documentation suggests using 
the 405 ephemerides set, but more updated sets (DE 407) also exist. For Linux, 
precomputed binaries can be found at `JPL Ephemerides binary files for Linux`_ 
and the `JPL Ephemerides descriptions`_.

For DE405::

    curl -O https://ssd.jpl.nasa.gov/ftp/eph/planets/Linux/de405/lnxp1600p2200.405

For DE440 (used in this documentation)::

    curl -O https://ssd.jpl.nasa.gov/ftp/eph/planets/Linux/de440/linux_p1550p2650.440

The downloaded binary ephemerides file must be linked so that the OrbFit 
program can properly utilize it; using a symbolic link in the 
:file:`Orbfit/lib/` directory, and assuming the DE440 file was downloaded (the 
command below should be changed to fit your file)::

    cd ./lib/
    ln -s ./../linux_p1550p2650.440 jpleph
    # Back to Orbfit/.
    cd ..

.. _JPL Ephemerides binary files for Linux: https://ssd.jpl.nasa.gov/ftp/eph/planets/Linux/

.. _JPL Ephemerides descriptions: https://ssd.jpl.nasa.gov/planets/eph_export.html


Testing Suite
=============

The software's test suit can be executed from :file:`Orbfit/` via::

    make tests

This ensures that the program has been installed correctly.


Executable Path for Configuration File
======================================

For this program's executables to be used, the path that they exist in must 
be known to OpihiExarata. Copy the output of the working directory command 
and add it to the configuration file's entries as noted. The path should be 
an absolute path; these commands should be run in the :file:`Orbfit/` directory::

    cd .; echo "ORBFIT_DIRECTORY =="; pwd
    cd ./bin; echo "ORBFIT_BINARY_EXECUTABLE_DIRECTORY =="; pwd; cd ..

If your main operating system is Windows and you are installing this via WSL 
Ubuntu, use the following instead::

    cd .; echo "ORBFIT_DIRECTORY =="; echo "\\\\wsl$/Ubuntu"$(pwd)
    cd ./bin; echo "ORBFIT_BINARY_EXECUTABLE_DIRECTORY =="; pwd; cd ..

OpihiExarata Template Files
===========================

In order for OpihiExarata to properly use the OrbFit program, files which are 
used by OrbFit must be collected for OpihiExarata to leverage.

Create and enter the directory (starting from :file:`Orbfit/`)::

    mkdir exarata; cd exarata

Within the :file:`Orbfit/exarata/` directory, copy over the asteroid propagation 
files. This contains ephemerides data for asteroids to better propagations. 
Generally, these files can be found in :file:`Orbfit/tests/bineph/testout`. For 
some reason, the file extensions on these files are not in a form which is 
liked by Orbfit, so they are also changed. Namely, the commands below should 
work::

    # Copying the files...
    cp ./../tests/bineph/testout/AST17.* .
    cp ./../tests/bineph/testout/CPV.* .
    # Extension changes...
    mv AST17.bai_431_fcct AST17.bai
    mv AST17.bep_431_fcct AST17.bep
    mv CPV.bai_431_fcct CPV.bai
    mv CPV.bep_431_fcct CPV.bep
    mv CPV_iter.bop CPV.bop

Also, create the files which are to be used to input data into Orbfit from 
OpihiExarata. The main file that needs to be created is :file:`exarata.oop`. 
Create it with your favorite text editor and fill the file and save it with 
the following:

::

    ! First object
    object1.
        .name = exarata        ! Object name
        .obs_dir = '.'         ! Observations directory

    ! Elements output
    output.
        .epoch = CAL 2022/01/01  00:00:00 UTC  ! The epoch time of the orbit
        .elements = 'KEP'                      ! Kepler output elements

    ! Operations: preliminary orbits, differential corrections, identification
    operations.
        .init_orbdet = 1    ! Initial orbit determination
                            ! (0 = no, 1 = yes)
        .diffcor = 1        ! Differential correction 
                            ! (0 = no, 1 = yes)
        .ident = 0          ! Orbit identification
                            ! (0 = no, 1 = yes)
        .ephem = 0          ! Ephemerides
                            ! (0 = no, 1 = yes)

    ! Error model
    error_model.
        .name='fcct14'      ! Error model

    ! Propagation
    propag.

        .iast=17         ! 0=no asteroids with mass, n=no. of massive asteroids (def=0)
        .filbe='AST17'   ! name of the asteroid ephemerides file (def='CPV')
        .npoint=600      ! minimum number of data points for a deep close appr (def=100)
        .dmea=0.2d0      ! min. distance for ctrl. of close-app. to Earth only (def=0.1)
            .dter=0.05d0    ! min. distance for control of close-app.
                            ! to terrestrial planets (MVM)(def=0.1)

    ! Additional options
    IERS.
        .extrapolation=.T.  ! extrapolation of Earth rotation

    reject.
        .rejopp=.FALSE.	    ! reject entire opposition


The other two files you can create with the following commands::

    echo "exarata" > exarata.inp
    touch exarata.obs

.. note::
    OpihiExarata will check that these three files exist as a check to see 
    that these steps have been followed correctly. It is also a way to ensure 
    that the configuration paths provided in the configuration are valid and 
    point to the right location.
