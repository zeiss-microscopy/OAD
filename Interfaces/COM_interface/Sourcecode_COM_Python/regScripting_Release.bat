:: regScripting_zen311.bat --> works with ZEN 3.11 or newer !!!
:: This needs to be run with administrator privileges !!!

echo off

SET DLL1="c:\Program Files\Carl Zeiss\ZEN 2\ZEN 2 (blue edition)\Zeiss.Micro.Scripting.comhost.dll"
SET DLL2="c:\Program Files\Carl Zeiss\ZEN 2\ZEN 2 (blue edition)\Zeiss.Micro.LM.Scripting.comhost.dll"
SET DLL3="c:\Program Files\Carl Zeiss\ZEN 2\ZEN 2 (blue edition)\Zeiss.Micro.Scripting.Research.comhost.dll"

regsvr32.exe /u %DLL1%
regsvr32.exe /u %DLL2%
regsvr32.exe /u %DLL3%

regsvr32.exe %DLL1%
regsvr32.exe %DLL2%
regsvr32.exe %DLL3%

popd
pause