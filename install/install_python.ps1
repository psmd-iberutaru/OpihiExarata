#requires -PSEdition Core

# This executes the installation instructions for the Python segment of the 
# code. We do the following:
#   - Install packages required for building and installing the software.
#   - Build the OpihiExarata package, clearing out previously built packages.
#   - Install the package.

Write-Output "=========================================="
Write-Output "===== Python Part ========================"
Write-Output "=========================================="

# Installing required packages which are needed for the installation of the 
# Python segment.
# These parts is OS dependent.

if ($isCentOS) {
    sudo yum install libgl1-mesa-dev
}
elseif ($isUbuntu) {
    sudo apt install libgl1-mesa-dev
}


# Python packages required.
pip install build setuptools wheel


# The default directory where we will build OpihiExarata. Note that the actual 
# process is being run a in the root directory so we do not need to go a 
# directory up.
$build_dir = "./dist/"

# Removing previously build distributions, they are not needed.
Remove-Item $build_dir -Recurse -Force

# Build the package.
python -m build

# Install the newly built package and wheel.
$build_file = Get-ChildItem $build_dir -Recurse -Name -Filter "OpihiExarata-*.whl"

# We also uninstall any previous versions.
python -m pip uninstall -y OpihiExarata

# We assume the only wheel file that was built is the same one to be installed.
$build_path = $build_dir + $build_file
Write-Output "Installing OpihiExarata package:   $build_path"
# The optimized mode is in the event it is being build on a network drive or 
# something.
python -O -m pip install $build_path