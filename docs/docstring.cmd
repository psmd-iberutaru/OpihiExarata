:;# This is a special script which intermixes both sh and cmd code. It is 
:;# written this way because it is used in system() shell-outs directly in 
:;# otherwise portable code. See https://stackoverflow.com/questions/17510688
:;# for details.


:;# Execute the building of the Python document strings, toggling based on how
:;# different shells handle different comment strings.

:; sphinx-apidoc -f -e -o ./source/code/ ./../src/opihiexarata/ ; exit
@ECHO OFF
sphinx-apidoc -f -e -o ./source/code/ ./../src/opihiexarata/