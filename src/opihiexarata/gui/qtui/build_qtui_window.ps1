#requires -PSEdition Core

# Powershell script to build the Python GUI files from the Qt Designer UI 
# files.

# If there are permission issues because of Powershell execution policy, then
# you can change it using:
# Set-ExecutionPolicy -Scope Process RemoteSigned

# Creating the GUI files.

pyside6-uic .\primary.ui | Out-File .\qtui_primary.py -Encoding "utf8"
pyside6-uic .\selector.ui | Out-File .\qtui_selector.py -Encoding "utf8"