.. _technical-installation-download:

=================
Install: Download
=================

The OpihiExarata software is stored its 
`Github software repository <https://github.com/psmd-iberutaru/OpihiExarata>`_. 
It needs to be downloaded from there, there are two main methods of doing that.
Both are detailed here.

Throughout the installation tutorial we refer to the internal OpihiExarata 
directory as :file:`OpihiExarata/`. This allows for the instructions to be 
general. Please adapt any absolute paths as needed.

Via git (Recommended)
=====================

The best way to download OpihiExarata is to clone the repository::

    git clone https://github.com/psmd-iberutaru/OpihiExarata.git

The location where you download the OpihiExarata repository is relatively 
irrelevant. 


Via .zip Archive
================

There are alternative ways to download the software. Although, the only other 
method that is worthwhile to document is downloading the software as an 
archive and extracting it to the desired location.

A zip archive of the git repository can be downloaded via::

    curl -O -L https://github.com/psmd-iberutaru/OpihiExarata/archive/refs/heads/master.zip
    unzip master.zip
    # Optional; to follow the documentation naming conventions.
    mv OpihiExarata-master OpihiExarata
    # The zip is no longer needed.
    rm master.zip