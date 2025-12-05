@echo off
REM Test execution script for Payroll Engine (Windows)
REM Compiles, runs COBOL program, and displays output

echo ========================================
echo PAYROLL ENGINE TEST EXECUTION
echo ========================================
echo.

REM Step 1: Compile the COBOL program
echo [1/3] Compiling COBOL program...
call cobol\compile.bat
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Compilation failed. Aborting test.
    exit /b 1
)
echo.

REM Step 2: Run the compiled program
echo [2/3] Executing payroll engine...
cobol\bin\payroll.exe
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Program execution failed with error code %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)
echo Program execution completed successfully.
echo.

REM Step 3: Display output report
echo [3/3] Displaying output report (data/output.rpt):
echo ========================================
if exist data\output.rpt (
    type data\output.rpt
    echo.
    echo ========================================
    echo.
    echo [SUCCESS] Test execution complete!
    echo.
    echo Output Format Verification:
    echo - Each record should be 60 characters wide
    echo - Employee ID: positions 1-10
    echo - Gross Pay: positions 11-22 (format: 9999999999V99)
    echo - Federal Tax: positions 23-34 (format: 9999999999V99)
    echo - State Tax: positions 35-46 (format: 9999999999V99)
    echo - Net Pay: positions 47-58 (format: 9999999999V99)
    echo - Status: positions 59-60 (OK or ER)
    echo - Summary line: "SUMMARY: PROCESSED=nnnnn ERRORS=nnnnn"
) else (
    echo [ERROR] Output file not found at data\output.rpt
    exit /b 1
)
