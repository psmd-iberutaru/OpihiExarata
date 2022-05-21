#requires -PSEdition Core

# Parameter handling for this script.
Param (
    [switch]$Auxiliary=$False
)

###############################################################################

# This is the master script for installing the entire OpihiExarata suite.
# The avaliable configurations are listed here.

# For Linux installations different flavors have different package managers.
# as such, the package manager installation command is different and is alised 
# here. We only support a few flavors. Fill in the prefix per your operating
# system if you use Linux.
function LinuxPackagePrefix {
    sudo apt $args
}

# Optionally, the auxiliary files and other development processes can be built 
# along with the installation. You may do so by invoking the -Auxiliary option
# or uncommenting below.
#$Auxiliary=$True


###############################################################################
# We begin the scriping here, please do not change any of the scripts below.

# The alias for Linux installation. This is needed in the event that 
# sudo is needed as aliases only work for single commands. Powershell already
# uses package, and a good space-themed name like this is unlikely to conflict
# with other defined aliases.
New-Alias -Name constellation -Value LinuxPackagePrefix

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