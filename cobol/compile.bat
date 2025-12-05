@echo off
REM Compilation script for Payroll Engine (Windows)
REM Compiles COBOL source to executable binary

echo Compiling payroll.cbl...
cobc -x -o cobol/bin/payroll cobol/payroll.cbl

if %ERRORLEVEL% EQU 0 (
    echo Compilation successful! Binary created at cobol/bin/payroll.exe
) else (
    echo Compilation failed with error code %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)
