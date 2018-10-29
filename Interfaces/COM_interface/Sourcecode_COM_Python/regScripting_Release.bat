:: regScripting_Release.bat

echo off

pushd "C:\Windows\Microsoft.NET\Framework64\v4.0.30319"

SET dll-1="C:\Program Files\Carl Zeiss\ZEN 2\ZEN 2 (blue edition)\Zeiss.Micro.Scripting.dll"
regasm /u /codebase /tlb %dll-1%
regasm /codebase /tlb %dll-1%

SET dll-2="C:\Program Files\Carl Zeiss\ZEN 2\ZEN 2 (blue edition)\Zeiss.Micro.LM.Scripting.dll"
regasm /u /codebase /tlb %dll-2%
regasm /codebase /tlb %dll-2%
popd
pause