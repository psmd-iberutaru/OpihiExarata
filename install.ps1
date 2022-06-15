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

##########################################
Write-Output "=========================================="
Write-Output "===== Python Part ========================"
Write-Output "=========================================="
# This executes the installation instructions for the Python segment of the 
# code. We do the following:
#   - Install packages required for building and installing the software.
#   - Build the OpihiExarata package, clearing out previously built packages.
#   - Install the package.

# Installing required packages which are needed for the installation of the 
# Python segment. These parts is OS dependent as this is for Qt.
if ($isCentOS) {
    sudo yum groupinstall "C Development Tools and Libraries"
    sudo yum install mesa-libGL-devel
}
elseif ($isUbuntu) {
    sudo apt install build-essential libgl1-mesa-dev
}

# Python packages required.
pyox -m pip install build setuptools wheel

# The default directory where we will build OpihiExarata. Note that the actual 
# process is being run a in the root directory so we do not need to go a 
# directory up.
$build_dir = "./dist/"

# Removing previously build distributions, they are not needed.
Remove-Item $build_dir -Recurse -Force

# Build the package.
pyox -m build

# Install the newly built package and wheel.
$build_file = Get-ChildItem $build_dir -Recurse -Name -Filter "OpihiExarata-*.whl"

# We also uninstall any previous versions.
pyox -m pip uninstall -y OpihiExarata

# We assume the only wheel file that was built is the same one to be installed.
$build_path = $build_dir + $build_file
Write-Output "Installing OpihiExarata package:   $build_path"
# The optimized mode is in the event it is being build on a network drive or 
# something.
pyox -O -m pip install $build_path