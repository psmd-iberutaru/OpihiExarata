:;# This is a special script which intermixes both sh and cmd code. It is 
:;# written this way because it is used in system() shell-outs directly in 
:;# otherwise portable code. See https://stackoverflow.com/questions/17510688
:;# for details. (Must use LF for line endings for Linux compatability.)


:;# Execute the building of the Python document strings, toggling based on how
:;# different shells handle different comment strings. Removing the previous
:;# docstring files is also useful.

:;# Bash-like shell
:; rm -r ./source/code/*
:; sphinx-apidoc -f -e -o ./source/code/ ./../src/opihiexarata/ 
:; exit

:;# DOS-like shell
@ECHO OFF
del /S /Q .\source\code\*
sphinx-apidoc -f -e -o ./source/code/ ./../src/opihiexarata/