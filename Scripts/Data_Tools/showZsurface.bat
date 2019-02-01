@REM Author: czsrh
@REM Date: 30.05.2017
@REM Version 1.0
@REM File: showZsurface.bat
@REM
@REM Must be used from command line:
@REM C:\mydir>showZsurface.bat czifile True tab True png True
@REM
@REM Arguments:
@REM %1 = Filename of CZI !!! No spaces inside filename are allowed !!!
@REM %2 = Write plantable to CSV file
@REM %3 = Define the used separator for the CSV file
@REM %4 = Option to save the plot
@REM %5 = Specify image save format
@REM %6 = Option to display an additional surface plot
@REM
@REM Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved. 
@REM #################################################################################

@echo off
set DEFAULT_SCRIPT_DIR=c:\Users\m1srh\Documents\GitHub\open_application_development\Scripts\Data_Tools\
set DEFAULT_SCRIPT=showZsurface.py

@REM Get the direcotry and options to be processed from the command line arguments
set CZIFILE=%1
set WRITECSV=%2
set SEPARATOR=%3
set SAVEOPT=%4
set FORMAT=%5
set SHOWOPT=%6
set VERSION=1.0

@ECHO Running showZsurface.bat - Version %VERSION% by czsrh

@REM Store the original working directory
set ORIGINAL_DIR=%CD%

@ECHO Change to script directory: %DEFAULT_SCRIPT_DIR%
pushd %DEFAULT_SCRIPT_DIR%

@REM define commad line parameters for the python script
@ECHO Start python script: %DEFAULT_SCRIPT%
python %DEFAULT_SCRIPT% -file "%CZIFILE%" -csv %WRITECSV% -sep %SEPARATOR% -save %SAVEOPT% -format %FORMAT% -show %SHOWOPT%
@REM @ECHO Errorlevel: %ERRORLEVEL%

@ECHO Change back directory to original: %ORIGINAL_DIR%
pushd %ORIGINAL_DIR%

@ECHO Done and Exit.
exit /B 0