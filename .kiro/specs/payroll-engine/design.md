# Design Document: Payroll Engine

## Overview

The Payroll Engine is a COBOL program that processes employee payroll data with exact decimal precision. It reads fixed-width input records, performs tax calculations using fixed-point arithmetic, and writes structured output for downstream processing by the Python Bridge and Base L2 settlement layer.

The design follows classic mainframe batch processing patterns: sequential file I/O, record-by-record processing, and comprehensive error handling. This approach ensures predictable behavior, auditability, and compatibility with the "Frankenstein" architecture.

## Architecture

### Program Structure

The COBOL program follows the standard four-division structure:

1. **IDENTIFICATION DIVISION**: Program metadata and documentation
2. **ENVIRONMENT DIVISION**: File declarations and I/O configuration
3. **DATA DIVISION**: Data structures for input, output, and working storage
4. **PROCEDURE DIVISION**: Processing logic and control flow

### Processing Flow

```
START
  ↓
OPEN FILES (input.dat, output.rpt)
  ↓
READ FIRST RECORD
  ↓
┌─────────────────────┐
│ PROCESS LOOP        │
│  ↓                  │
│ VALIDATE INPUT      │
│  ↓                  │
│ IF VALID:           │
│   - CALC GROSS PAY  │
│   - CALC FED TAX    │
│   - CALC STATE TAX  │
│   - CALC NET PAY    │
│   - WRITE OUTPUT    │
│ ELSE:               │
│   - WRITE ERROR     │
│  ↓                  │
│ READ NEXT RECORD    │
│  ↓                  │
│ IF NOT EOF: LOOP    │
└─────────────────────┘
  ↓
WRITE SUMMARY
  ↓
CLOSE FILES
  ↓
END
```

## Components and Interfaces

### Input File Structure (input.dat)

Fixed-width format, one record per employee:

| Field         | Position | Length | Type        | Format      |
|---------------|----------|--------|-------------|-------------|
| Employee ID   | 1-10     | 10     | Alphanumeric| Left-aligned|
| Hours Worked  | 11-15    | 5      | Numeric     | 999V99      |
| Hourly Rate   | 16-21    | 6      | Numeric     | 9999V99     |
| Tax Code      | 22-23    | 2      | Alphanumeric| Left-aligned|

**Example Input Record:**
```
EMP0001234012345006750US
```
Parsed as:
- Employee ID: `EMP0001234`
- Hours Worked: `123.45`
- Hourly Rate: `67.50`
- Tax Code: `US`

### Output File Structure (output.rpt)

Fixed-width format, one record per processed employee:

| Field         | Position | Length | Type        | Format      |
|---------------|----------|--------|-------------|-------------|
| Employee ID   | 1-10     | 10     | Alphanumeric| Left-aligned|
| Gross Pay     | 11-22    | 12     | Numeric     | 99999999V99 |
| Federal Tax   | 23-34    | 12     | Numeric     | 99999999V99 |
| State Tax     | 35-46    | 12     | Numeric     | 99999999V99 |
| Net Pay       | 47-58    | 12     | Numeric     | 99999999V99 |
| Status        | 59-60    | 2      | Alphanumeric| OK/ER       |

**Example Output Record (Success):**
```
EMP0001234000008333.25000001249.99000000416.66000006666.60OK
```

**Example Output Record (Error):**
```
EMP0001234000000000.00000000000.00000000000.00000000000.00ER
```

### Summary Line

Written as the final line of output.rpt:

```
SUMMARY: PROCESSED=nnnnn ERRORS=nnnnn
```

## Data Models

### Working Storage Variables

```cobol
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
```

### File Definitions

```cobol
FD  INPUT-FILE
    RECORDING MODE IS F
    BLOCK CONTAINS 0 RECORDS.
01  INPUT-RECORD                PIC X(23).

FD  OUTPUT-FILE
    RECORDING MODE IS F
    BLOCK CONTAINS 0 RECORDS.
01  OUTPUT-RECORD               PIC X(60).
```

## Calculation Logic

### Gross Pay Calculation

```
GROSS-PAY = HOURS-WORKED × HOURLY-RATE
```

COBOL implementation uses `COMPUTE` with `ROUNDED` clause:
```cobol
COMPUTE WS-GROSS-PAY ROUNDED = 
    WS-HOURS-WORKED * WS-HOURLY-RATE
```

### Tax Calculations

```
FEDERAL-TAX = GROSS-PAY × 0.15
STATE-TAX = GROSS-PAY × 0.05
```

COBOL implementation:
```cobol
COMPUTE WS-FEDERAL-TAX ROUNDED = 
    WS-GROSS-PAY * WS-FEDERAL-RATE

COMPUTE WS-STATE-TAX ROUNDED = 
    WS-GROSS-PAY * WS-STATE-RATE
```

### Net Pay Calculation

```
NET-PAY = GROSS-PAY - FEDERAL-TAX - STATE-TAX
```

COBOL implementation:
```cobol
COMPUTE WS-NET-PAY ROUNDED = 
    WS-GROSS-PAY - WS-FEDERAL-TAX - WS-STATE-TAX
```

## Error Handling

### Validation Rules

The program validates each input record before processing:

1. **Employee ID Validation**
   - Must not be spaces
   - Must not be empty
   - Error code: `ER01`

2. **Hours Worked Validation**
   - Must be greater than zero
   - Must be numeric
   - Error code: `ER02`

3. **Hourly Rate Validation**
   - Must be greater than zero
   - Must be numeric
   - Error code: `ER03`

### Error Processing Flow

```cobol
PERFORM VALIDATE-INPUT
IF WS-VALID-FLAG = 'N'
    ADD 1 TO WS-RECORDS-ERROR
    PERFORM WRITE-ERROR-RECORD
ELSE
    PERFORM CALCULATE-PAYROLL
    PERFORM WRITE-OUTPUT-RECORD
    ADD 1 TO WS-RECORDS-PROCESSED
END-IF
```

### Error Output

When validation fails, the program writes an error record with:
- Original Employee ID
- All monetary fields set to zero
- Status field set to `ER`

The program continues processing subsequent records (fail-safe behavior).

## Testing Strategy

### Unit Test Cases

1. **Basic Calculation Test**
   - Input: EMP001, 40.00 hours, $25.00/hour
   - Expected: Gross=$1000.00, Fed=$150.00, State=$50.00, Net=$800.00

2. **Decimal Precision Test**
   - Input: EMP002, 37.50 hours, $22.75/hour
   - Expected: Gross=$853.13, Fed=$127.97, State=$42.66, Net=$682.50

3. **Rounding Test**
   - Input: EMP003, 33.33 hours, $15.15/hour
   - Expected: Verify proper banker's rounding at each step

4. **High Value Test**
   - Input: EMP004, 160.00 hours, $500.00/hour
   - Expected: Gross=$80000.00, Fed=$12000.00, State=$4000.00, Net=$64000.00

### Validation Test Cases

5. **Invalid Hours (Zero)**
   - Input: EMP005, 0.00 hours, $25.00/hour
   - Expected: Error record, status=ER

6. **Invalid Hours (Negative)**
   - Input: EMP006, -10.00 hours, $25.00/hour
   - Expected: Error record, status=ER

7. **Invalid Rate (Zero)**
   - Input: EMP007, 40.00 hours, $0.00/hour
   - Expected: Error record, status=ER

8. **Invalid Employee ID (Blank)**
   - Input: (spaces), 40.00 hours, $25.00/hour
   - Expected: Error record, status=ER

### Integration Test Cases

9. **Batch Processing Test**
   - Input: 10 valid records
   - Expected: 10 output records, summary shows PROCESSED=10 ERRORS=0

10. **Mixed Batch Test**
    - Input: 5 valid, 3 invalid records
    - Expected: 8 output records, summary shows PROCESSED=5 ERRORS=3

### Compilation Test

11. **GnuCOBOL Compilation**
    - Verify program compiles without errors using: `cobc -x -free payroll.cbl`
    - Verify executable runs and produces output

## File I/O Specifications

### File Locations

- Input: `data/input.dat`
- Output: `data/output.rpt`

### File Access Mode

- Sequential read for input
- Sequential write for output
- No random access required

### End-of-File Handling

```cobol
READ INPUT-FILE
    AT END
        MOVE 'Y' TO WS-EOF-FLAG
    NOT AT END
        PERFORM PROCESS-RECORD
END-READ
```

## Performance Considerations

### Expected Throughput

- Target: Process 1000 records per second on modern hardware
- Batch size: Up to 100,000 records per run
- Memory footprint: Minimal (< 1MB working storage)

### Optimization Notes

- Use `BLOCK CONTAINS 0` for optimal OS-level buffering
- Minimize I/O operations by batching writes
- Use `ROUNDED` clause for efficient rounding
- Avoid unnecessary data movement with `MOVE CORRESPONDING`

## Compilation and Deployment

### Compiler

GnuCOBOL (formerly OpenCOBOL) version 3.0 or higher

### Compilation Command

```bash
cobc -x -o cobol/bin/payroll cobol/payroll.cbl
```

Flags:
- `-x`: Generate executable
- `-o`: Specify output file
- Fixed format (default for .cbl extension)

### Runtime Environment

- OS: Linux, macOS, or Windows with GnuCOBOL runtime
- No external dependencies beyond GnuCOBOL runtime libraries
- File system access to `data/` directory

## Integration Points

### Python Bridge Interface

The Python Bridge (`backend/bridge.py`) will:

1. Write JSON input to `data/input.dat` in fixed-width format
2. Execute the COBOL binary via subprocess
3. Read `data/output.rpt` and parse fixed-width output
4. Convert results back to JSON for API responses

### Data Flow

```
Frontend (JSON)
    ↓
Python Bridge (JSON → Fixed-Width)
    ↓
COBOL Engine (Fixed-Width → Fixed-Width)
    ↓
Python Bridge (Fixed-Width → JSON)
    ↓
Coinbase SDK (USDC Transfer)
```

## Security Considerations

### Input Sanitization

- COBOL program assumes input is pre-validated by Python Bridge
- No SQL injection risk (no database access)
- No buffer overflow risk (fixed-width fields with strict PIC clauses)

### Data Privacy

- No logging of sensitive data within COBOL program
- Input/output files should be secured at OS level
- Consider encryption for data at rest (handled by deployment environment)

## Maintenance and Extensibility

### Adding New Tax Types

To add additional tax deductions:

1. Add new rate constant to `WS-TAX-RATES`
2. Add new calculated field to `WS-CALCULATED-VALUES`
3. Add computation in `CALCULATE-PAYROLL` paragraph
4. Update output record structure
5. Update Python Bridge parser

### Modifying Tax Rates

Tax rates are defined as constants in `WS-TAX-RATES`. To change:

1. Update `VALUE` clause in data definition
2. Recompile program
3. No code logic changes required

### Supporting Multiple Tax Codes

Future enhancement: Use `TAX-CODE` field to apply different rates:

```cobol
EVALUATE WS-TAX-CODE
    WHEN 'US'
        MOVE 0.15 TO WS-FEDERAL-RATE
        MOVE 0.05 TO WS-STATE-RATE
    WHEN 'CA'
        MOVE 0.20 TO WS-FEDERAL-RATE
        MOVE 0.10 TO WS-STATE-RATE
END-EVALUATE
```
