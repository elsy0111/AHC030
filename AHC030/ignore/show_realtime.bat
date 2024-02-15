@echo off
set /p filePath="Enter the file path: "
pwsh.exe -Command "Get-Content -Path '%filePath%' -Wait"
