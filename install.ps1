#requires -PSEdition Core

# This is the master script for installing the entire OpihiExarata suite.

# Optionally, the auxiliary files and other development processes can be built 
# along with the installation.


################################################################################
# Parameter handling for this script.
Param (
    [switch]$Auxiliary=$False
)

# If the user wanted auxiliary processes to compute.
if ($Auxiliary) {
    pwsh -File "./auxiliary.ps1"
}


# All of the Powershell scripts for installation resides in the installation
# directory.
$install_script_dir = "./install/"

# Installing the Python part of the program.
Write-Output "=========================================="
Write-Output "===== Python Part ========================"
Write-Output "=========================================="
pwsh -File ($install_script_dir + "install_python.ps1")