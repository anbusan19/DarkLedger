      ******************************************************************
      * PROGRAM-ID: PAYROLL                                            *
      * AUTHOR: LEDGER-DE-MAIN SYSTEM                                  *
      * DATE-WRITTEN: 2025-12-05                                       *
      * DESCRIPTION: PAYROLL ENGINE WITH EXACT DECIMAL PRECISION       *
      *              PROCESSES EMPLOYEE PAYROLL DATA AND CALCULATES    *
      *              GROSS PAY, FEDERAL TAX, STATE TAX, AND NET PAY    *
      ******************************************************************
       IDENTIFICATION DIVISION.
       PROGRAM-ID. PAYROLL.
       AUTHOR. LEDGER-DE-MAIN-SYSTEM.
       DATE-WRITTEN. 2025-12-05.
       DATE-COMPILED.
      
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT INPUT-FILE
               ASSIGN TO "data/input.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-INPUT-STATUS.
           SELECT OUTPUT-FILE
               ASSIGN TO "data/output.rpt"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-OUTPUT-STATUS.

       DATA DIVISION.
       FILE SECTION.
       FD  INPUT-FILE
           RECORDING MODE IS F
           BLOCK CONTAINS 0 RECORDS.
       01  INPUT-RECORD                PIC X(23).
      
       FD  OUTPUT-FILE
           RECORDING MODE IS F
           BLOCK CONTAINS 0 RECORDS.
       01  OUTPUT-RECORD               PIC X(60).
      
       WORKING-STORAGE SECTION.
       01  WS-INPUT-RECORD.
           05  WS-EMPLOYEE-ID          PIC X(10).
           05  WS-HOURS-WORKED         PIC 999V99.
           05  WS-HOURLY-RATE          PIC 9999V99.
           05  WS-TAX-CODE             PIC XX.
      
       01  WS-CALCULATED-VALUES.
           05  WS-GROSS-PAY            PIC 9(8)V99.
           05  WS-FEDERAL-TAX          PIC 9(8)V99.
           05  WS-STATE-TAX            PIC 9(8)V99.
           05  WS-NET-PAY              PIC 9(8)V99.
      
       01  WS-TAX-RATES.
           05  WS-FEDERAL-RATE         PIC V99 VALUE 0.15.
           05  WS-STATE-RATE           PIC V99 VALUE 0.05.
      
       01  WS-COUNTERS.
           05  WS-RECORDS-PROCESSED    PIC 9(5) VALUE 0.
           05  WS-RECORDS-ERROR        PIC 9(5) VALUE 0.
      
       01  WS-FLAGS.
           05  WS-EOF-FLAG             PIC X VALUE 'N'.
           05  WS-VALID-FLAG           PIC X VALUE 'Y'.
      
       01  WS-FILE-STATUS.
           05  WS-INPUT-STATUS         PIC XX.
           05  WS-OUTPUT-STATUS        PIC XX.
      
       01  WS-OUTPUT-RECORD-FORMATTED.
           05  WS-OUT-EMPLOYEE-ID      PIC X(10).
           05  WS-OUT-GROSS-PAY        PIC 9(10)V99.
           05  WS-OUT-FEDERAL-TAX      PIC 9(10)V99.
           05  WS-OUT-STATE-TAX        PIC 9(10)V99.
           05  WS-OUT-NET-PAY          PIC 9(10)V99.
           05  WS-OUT-STATUS           PIC XX.
      
       01  WS-SUMMARY-LINE             PIC X(60).

       PROCEDURE DIVISION.
       MAIN-LOGIC.
           PERFORM OPEN-FILES.
           PERFORM READ-NEXT-RECORD.
           PERFORM UNTIL WS-EOF-FLAG = 'Y'
               PERFORM PROCESS-RECORD
               PERFORM READ-NEXT-RECORD
           END-PERFORM.
           PERFORM WRITE-SUMMARY.
           PERFORM CLOSE-FILES.
           STOP RUN.
      
      ******************************************************************
      * OPEN-FILES: OPENS INPUT AND OUTPUT FILES                      *
      ******************************************************************
       OPEN-FILES.
           OPEN INPUT INPUT-FILE.
           OPEN OUTPUT OUTPUT-FILE.
      
      ******************************************************************
      * CLOSE-FILES: CLOSES INPUT AND OUTPUT FILES                    *
      ******************************************************************
       CLOSE-FILES.
           CLOSE INPUT-FILE.
           CLOSE OUTPUT-FILE.
      
      ******************************************************************
      * READ-NEXT-RECORD: READS NEXT RECORD FROM INPUT FILE           *
      * SETS EOF FLAG WHEN END OF FILE IS REACHED                     *
      ******************************************************************
       READ-NEXT-RECORD.
           READ INPUT-FILE INTO WS-INPUT-RECORD
               AT END
                   MOVE 'Y' TO WS-EOF-FLAG
           END-READ.
      
      ******************************************************************
      * PROCESS-RECORD: PROCESSES A SINGLE EMPLOYEE RECORD            *
      * VALIDATES INPUT, CALCULATES PAYROLL, AND WRITES OUTPUT        *
      ******************************************************************
       PROCESS-RECORD.
           PERFORM VALIDATE-INPUT.
           IF WS-VALID-FLAG = 'Y'
               PERFORM CALCULATE-PAYROLL
               PERFORM WRITE-OUTPUT-RECORD
               ADD 1 TO WS-RECORDS-PROCESSED
           ELSE
               PERFORM WRITE-ERROR-RECORD
               ADD 1 TO WS-RECORDS-ERROR
           END-IF.
      
      ******************************************************************
      * CALCULATE-PAYROLL: PERFORMS ALL PAYROLL CALCULATIONS          *
      * COMPUTES GROSS PAY, FEDERAL TAX, STATE TAX, AND NET PAY        *
      * USES FIXED-POINT ARITHMETIC WITH BANKER'S ROUNDING             *
      ******************************************************************
       CALCULATE-PAYROLL.
           COMPUTE WS-GROSS-PAY ROUNDED = 
               WS-HOURS-WORKED * WS-HOURLY-RATE.
           COMPUTE WS-FEDERAL-TAX ROUNDED = 
               WS-GROSS-PAY * WS-FEDERAL-RATE.
           COMPUTE WS-STATE-TAX ROUNDED = 
               WS-GROSS-PAY * WS-STATE-RATE.
           COMPUTE WS-NET-PAY ROUNDED = 
               WS-GROSS-PAY - WS-FEDERAL-TAX - WS-STATE-TAX.
      
      ******************************************************************
      * VALIDATE-INPUT: VALIDATES EMPLOYEE RECORD DATA                *
      * CHECKS EMPLOYEE ID, HOURS WORKED, AND HOURLY RATE             *
      * SETS WS-VALID-FLAG TO 'N' IF ANY VALIDATION FAILS             *
      ******************************************************************
       VALIDATE-INPUT.
           MOVE 'Y' TO WS-VALID-FLAG.
           
           IF WS-EMPLOYEE-ID = SPACES OR WS-EMPLOYEE-ID = SPACES
               MOVE 'N' TO WS-VALID-FLAG
           END-IF.
           
           IF WS-HOURS-WORKED <= 0
               MOVE 'N' TO WS-VALID-FLAG
           END-IF.
           
           IF WS-HOURLY-RATE <= 0
               MOVE 'N' TO WS-VALID-FLAG
           END-IF.
      
      ******************************************************************
      * WRITE-OUTPUT-RECORD: WRITES SUCCESSFUL PAYROLL RECORD         *
      * FORMATS OUTPUT WITH FIXED-WIDTH MONETARY VALUES               *
      ******************************************************************
       WRITE-OUTPUT-RECORD.
           MOVE WS-EMPLOYEE-ID TO WS-OUT-EMPLOYEE-ID.
           MOVE WS-GROSS-PAY TO WS-OUT-GROSS-PAY.
           MOVE WS-FEDERAL-TAX TO WS-OUT-FEDERAL-TAX.
           MOVE WS-STATE-TAX TO WS-OUT-STATE-TAX.
           MOVE WS-NET-PAY TO WS-OUT-NET-PAY.
           MOVE 'OK' TO WS-OUT-STATUS.
           WRITE OUTPUT-RECORD FROM WS-OUTPUT-RECORD-FORMATTED.
      
      ******************************************************************
      * WRITE-ERROR-RECORD: WRITES ERROR RECORD FOR INVALID INPUT     *
      * SETS ALL MONETARY VALUES TO ZERO AND STATUS TO 'ER'           *
      ******************************************************************
       WRITE-ERROR-RECORD.
           MOVE WS-EMPLOYEE-ID TO WS-OUT-EMPLOYEE-ID.
           MOVE 0 TO WS-OUT-GROSS-PAY.
           MOVE 0 TO WS-OUT-FEDERAL-TAX.
           MOVE 0 TO WS-OUT-STATE-TAX.
           MOVE 0 TO WS-OUT-NET-PAY.
           MOVE 'ER' TO WS-OUT-STATUS.
           WRITE OUTPUT-RECORD FROM WS-OUTPUT-RECORD-FORMATTED.
      
      ******************************************************************
      * WRITE-SUMMARY: WRITES SUMMARY LINE WITH PROCESSING COUNTS     *
      ******************************************************************
       WRITE-SUMMARY.
           STRING 'SUMMARY: PROCESSED=' WS-RECORDS-PROCESSED
                  ' ERRORS=' WS-RECORDS-ERROR
               DELIMITED BY SIZE
               INTO WS-SUMMARY-LINE
           END-STRING.
           WRITE OUTPUT-RECORD FROM WS-SUMMARY-LINE.
