@REM Author: Sebastian Rhode
@REM Date: 2017_04_02
@REM Version 1.1
@REM File: czi2ometiff_xml_split.bat
@REM
@REM Must be used from command line:
@REM C:\mydir>czi2ometiff_xml2.bat dir2process option2 option3 option4 bftoolsdir splioption
@REM
@REM Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
@REM #######################################################################################

@echo off

@REM Get the direcotry and options to be processed from the command line arguments
set DIR2PROCESS=%1
@REM @ECHO %DIR2PROCESS%
set EXPORTOMETIFF=%2
set CREATEOMEXML=%3
set WAITFORKEY=%4
set BFTOOLSPATH=%5
set SPLITDIM=%6
@REM @ECHO %BFTOOLSPATH%
set VERSION=1.1
set BFCONVERT=bfconvert.bat
set SHOWINF=showinf.bat

@REM Define the bfconvert tool to be used
set BFCONVERT_PATH=%BFTOOLSPATH%\%BFCONVERT%
set SHOWINF_PATH=%BFTOOLSPATH%\%SHOWINF%

@REM Store the original working directory
set ORIGINAL_DIR=%CD%

@REM Show the bfconvert tool location and the directories
@ECHO Running czi2ometiff_xml_split.bat - Version %VERSION% by SRh
@ECHO Location of bfconvert: %BFCONVERT_PATH%
@ECHO Original Directory: %ORIGINAL_DIR%
@ECHO Working Directory: %DIR2PROCESS%
@ECHO Export as OME-TIFF: %EXPORTOMETIFF%
@ECHO Split-Option: %SPLITDIM%
@ECHO Create OME-XML: %CREATEOMEXML%
@ECHO Wait for User at the end: %WAITFORKEY%

@REM Set working directory
pushd %DIR2PROCESS%

@REM Run the bfconvert.bat for all CZI files inside the direcory
@REM for /r %%f in (*.czi) do call bfconvert.bat -no-upgrade %%f %%~nf.ome.tiff
if "%EXPORTOMETIFF%" == "-export" (

	for /r %%f in (*.czi) do (
		
		@ECHO File2Convert: "%%f"

		@REM No splitting of any dimension
		if "%SPLITDIM%" == "-NOSPLIT" (
			call %BFCONVERT_PATH% -no-upgrade -option zeissczi.attachments false "%%f" "%%~nf.ome.tiff"
		)
		
		@REM split every timepoint
		if "%SPLITDIM%" == "-T" (
			set arg1=%%~nf_T%%%t.ome.tiff
			@REM %BFCONVERT_PATH% -no-upgrade -option zeissczi.attachments false "%%f" "%%~nf_T%%%%t.ome.tiff"
			call %BFCONVERT_PATH% -no-upgrade -option zeissczi.attachments false "%%f" "!arg1!"
		)
	)
)


@REM Create an OME-XML from the CZI when option was set to TRUE
if "%CREATEOMEXML%" == "-xml" (
 	for /r %%f in (*.czi) do (
		call %SHOWINF_PATH% -no-upgrade -nometa -nopix -omexml-only -novalid -nocore "%%f" > "%%~nf.xml"
		@REM call %SHOWINF_PATH% -no-upgrade -nopix -omexml-only -novalid -nocore "%%f" > "%%~nf.xml"
		@ECHO Created:  %%~nf.xml
	)
)

@ECHO Change back directory to original: %ORIGINAL_DIR%
pushd %ORIGINAL_DIR%


if "%WAITFORKEY%" == "-wait" (
	pause
)

@ECHO Done and Exit.
exit /B 0
