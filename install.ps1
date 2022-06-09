#requires -PSEdition Core

# Parameter handling for this script.
Param (
    [switch]$Auxiliary=$False
)

###############################################################################

# This is the master script for installing the entire OpihiExarata suite.
# The avaliable configurations are listed here.

# Each operating systems has their own unique way to determining how to
# enter the Python shell. For ease, please set it here so that the alias
# can be applied uniformly.
Set-Alias -Name pyox -Value python

# For Linux installations different flavors have different package managers.
# as such, the package manager installation command is different and is alised 
# here. We only support a few flavors. Fill in the prefix per your operating
# system if you use Linux. CentOS and RockyLinux are considered equivilant here.

$isCentOS = $False
$isUbuntu = $False

# Optionally, the auxiliary files and other development processes can be built 
# along with the installation. You may do so by invoking the -Auxiliary option
# or uncommenting below.
#$Auxiliary=$True


###############################################################################
# We begin the scriping here, please do not change any of the scripts below.

# If the user is on a Linux machine but did not specify exactly which one, then 
# stop as they need to specify.
if ($isLinux) {
    if (-not ($isUbuntu -or $isCentOS)) {
        # The user did not specify their Linux flavor.
        throw "You are running a Linux machine but did not specify the Linux flavor."
    }
}

# If the user wanted auxiliary processes to compute.
if ($Auxiliary) {
    pwsh -File "./auxiliary.ps1"
}


# All of the Powershell scripts for installation resides in the installation
# directory.
$install_script_dir = "./install/"

# Installing the Python part of the program.
pwsh -File ($install_script_dir + "install_python.ps1")