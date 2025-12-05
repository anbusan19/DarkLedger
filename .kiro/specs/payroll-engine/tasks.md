# Implementation Plan: Payroll Engine

- [x] 1. Set up COBOL project structure and file definitions





  - Create `cobol/` directory for COBOL source files
  - Create `cobol/bin/` directory for compiled binaries (add to .gitignore)
  - Create `data/` directory for input/output files
  - Add `.gitignore` entries for `cobol/bin/` and `data/*.dat`, `data/*.rpt`
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 2. Implement COBOL program structure and data definitions





  - [x] 2.1 Write IDENTIFICATION and ENVIRONMENT divisions

    - Define program metadata with proper fixed-format structure (columns 1-6 for sequence, column 7 for indicators, columns 8-72 for code)
    - Declare INPUT-FILE and OUTPUT-FILE with file paths `data/input.dat` and `data/output.rpt`
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  - [x] 2.2 Write DATA DIVISION with file and working storage definitions


    - Define FD entries for INPUT-FILE (23-byte record) and OUTPUT-FILE (60-byte record)
    - Define WS-INPUT-RECORD with Employee ID (X(10)), Hours Worked (999V99), Hourly Rate (9999V99), Tax Code (XX)
    - Define WS-CALCULATED-VALUES with Gross Pay, Federal Tax, State Tax, Net Pay (all 9(8)V99)
    - Define WS-TAX-RATES with Federal Rate (V99 VALUE 0.15) and State Rate (V99 VALUE 0.05)
    - Define WS-COUNTERS for records processed and errors
    - Define WS-FLAGS for EOF and validation status
    - _Requirements: 1.2, 1.3, 1.4, 1.5, 2.1_

- [x] 3. Implement core payroll calculation logic




  - [x] 3.1 Write CALCULATE-PAYROLL paragraph


    - Implement Gross Pay calculation: COMPUTE WS-GROSS-PAY ROUNDED = WS-HOURS-WORKED * WS-HOURLY-RATE
    - Implement Federal Tax calculation: COMPUTE WS-FEDERAL-TAX ROUNDED = WS-GROSS-PAY * WS-FEDERAL-RATE
    - Implement State Tax calculation: COMPUTE WS-STATE-TAX ROUNDED = WS-GROSS-PAY * WS-STATE-RATE
    - Implement Net Pay calculation: COMPUTE WS-NET-PAY ROUNDED = WS-GROSS-PAY - WS-FEDERAL-TAX - WS-STATE-TAX
    - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4_

- [x] 4. Implement input validation logic






  - [x] 4.1 Write VALIDATE-INPUT paragraph

    - Check Employee ID is not spaces or empty (set WS-VALID-FLAG to 'N' if invalid)
    - Check Hours Worked is greater than zero (set WS-VALID-FLAG to 'N' if invalid)
    - Check Hourly Rate is greater than zero (set WS-VALID-FLAG to 'N' if invalid)
    - Initialize WS-VALID-FLAG to 'Y' at start of validation
    - _Requirements: 5.1, 5.2, 5.3_

- [x] 5. Implement file I/O and record processing






  - [x] 5.1 Write main PROCEDURE DIVISION control flow

    - Implement OPEN-FILES paragraph to open INPUT-FILE and OUTPUT-FILE
    - Implement CLOSE-FILES paragraph to close both files
    - Implement main processing loop with READ-NEXT-RECORD paragraph
    - Handle AT END condition by setting WS-EOF-FLAG to 'Y'
    - _Requirements: 1.1, 4.1_

  - [x] 5.2 Write PROCESS-RECORD paragraph

    - Call VALIDATE-INPUT
    - If WS-VALID-FLAG = 'Y', call CALCULATE-PAYROLL and WRITE-OUTPUT-RECORD
    - If WS-VALID-FLAG = 'N', call WRITE-ERROR-RECORD and increment WS-RECORDS-ERROR
    - Increment WS-RECORDS-PROCESSED for valid records
    - _Requirements: 4.5, 5.4_
  - [x] 5.3 Write WRITE-OUTPUT-RECORD paragraph


    - Format output record with Employee ID, Gross Pay, Federal Tax, State Tax, Net Pay
    - Use fixed-width format with leading zeros for monetary values (12 characters each, format 99999999V99)
    - Set status field to 'OK'
    - Write to OUTPUT-FILE
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_
  - [x] 5.4 Write WRITE-ERROR-RECORD paragraph


    - Format error record with Employee ID and all monetary fields set to zero
    - Set status field to 'ER'
    - Write to OUTPUT-FILE
    - _Requirements: 5.4_

  - [x] 5.5 Write WRITE-SUMMARY paragraph

    - Format summary line: "SUMMARY: PROCESSED=nnnnn ERRORS=nnnnn"
    - Write as final line to OUTPUT-FILE
    - _Requirements: 5.5_


- [x] 6. Create test data files and compilation script




  - [x] 6.1 Create sample input.dat file

    - Include 3 valid test records with varying hours and rates
    - Include 2 invalid test records (zero hours, zero rate)
    - Use proper fixed-width format (23 bytes per record)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  - [x] 6.2 Create compilation script


    - Write `cobol/compile.sh` (or `compile.bat` for Windows) with GnuCOBOL compilation command
    - Use command: `cobc -x -o cobol/bin/payroll cobol/payroll.cbl`
    - Make script executable
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  - [x] 6.3 Create test execution script






    - Write script to compile, run COBOL program, and display output.rpt contents
    - Verify output format matches specification
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 7. Verify COBOL program compilation and execution






  - [x] 7.1 Compile the COBOL program


    - Run compilation script and verify no errors
    - Confirm binary is created in `cobol/bin/payroll`
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [ ] 7.2 Execute program with test data
    - Run the compiled binary
    - Verify output.rpt is created with correct format
    - Verify calculations match expected values for test cases
    - Verify summary line shows correct counts
    - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 4.5, 5.5_
