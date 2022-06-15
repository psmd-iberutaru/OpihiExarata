#requires -PSEdition Core

# Powershell script to build the Python GUI files from the Qt Designer UI 
# files.

# If there are permission issues because of Powershell execution policy, then
# you can change it using:
# Set-ExecutionPolicy -Scope Process RemoteSigned

# Creating the GUI files.
pyside6-uic .\manual.ui | Out-File .\qtui_manual.py -Encoding "utf8"
pyside6-uic .\selector.ui | Out-File .\qtui_selector.py -Encoding "utf8"

pyside6-uic .\automatic.ui | Out-File .\qtui_automatic.py -Encoding "utf8"