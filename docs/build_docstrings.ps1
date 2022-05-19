#requires -PSEdition Core

# This script builds the documentation files documenting the source code 
# itself using Sphinx and the written docstrings.

# Removing old cached files. This is done to ensure that it does not mess
# with the current build.
Remove-Item ./source/code/ -Recurse -Force

# Build the documentation files from the docstrings within the functions
# and classes.
sphinx-apidoc -f -e -o ./source/code/ ./../src/opihiexarata/