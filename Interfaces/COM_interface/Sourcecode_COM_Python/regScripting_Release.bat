:: This needs to be run with administrator privileges !!!

echo off

SET DLL1="c:\Program Files\Carl Zeiss\ZEN 2\ZEN 2 (blue edition)\Zeiss.Micro.Scripting.comhost.dll"
SET DLL2="c:\Program Files\Carl Zeiss\ZEN 2\ZEN 2 (blue edition)\Zeiss.Micro.LM.Scripting.comhost.dll"
SET DLL3="c:\Program Files\Carl Zeiss\ZEN 2\ZEN 2 (blue edition)\Zeiss.Micro.Scripting.Research.comhost.dll"
:: only needed for ZEN >= 3.13
SET DLL4="c:\Program Files\Carl Zeiss\ZEN 2\ZEN 2 (blue edition)\Zeiss.Micro.LM.Scripting.Research.comhost.dll

regsvr32.exe /u %DLL1%
regsvr32.exe /u %DLL2%
regsvr32.exe /u %DLL3%
:: only needed for ZEN >= 3.13
regsvr32.exe /u %DLL4%

regsvr32.exe %DLL1%
regsvr32.exe %DLL2%
regsvr32.exe %DLL3%
:: only needed for ZEN >= 3.13
regsvr32.exe %DLL4%

popd
pause