# Requirements Document

## Introduction

The Payroll Engine is the core calculation component of Ledger-De-Main, responsible for computing employee compensation with exact decimal precision. This component must process employee payroll data, apply tax calculations, and produce verified output suitable for blockchain settlement. The engine leverages COBOL's fixed-point arithmetic to eliminate floating-point errors that plague modern languages, ensuring audit-proof calculations for financial compliance.

## Glossary

- **Payroll Engine**: The COBOL program that performs all payroll calculations
- **Employee Record**: A data structure containing employee identification and compensation parameters
- **Gross Pay**: Total compensation before any deductions (Hours Worked × Hourly Rate)
- **Federal Tax**: Tax deduction calculated at 15% of Gross Pay
- **State Tax**: Tax deduction calculated at 5% of Gross Pay
- **Net Pay**: Final compensation after all deductions (Gross Pay - Federal Tax - State Tax)
- **Input File**: Fixed-width text file (input.dat) containing employee data for processing
- **Output File**: Fixed-width text file (output.rpt) containing calculation results
- **Fixed-Point Arithmetic**: Decimal calculation method that maintains exact precision to 2 decimal places

## Requirements

### Requirement 1

**User Story:** As an Operator, I want to submit employee payroll data through a standardized input format, so that the Payroll Engine can process calculations consistently.

#### Acceptance Criteria

1. WHEN the Payroll Engine starts execution, THE Payroll Engine SHALL read employee data from the Input File
2. THE Payroll Engine SHALL accept Employee ID as a 10-character alphanumeric field
3. THE Payroll Engine SHALL accept Hours Worked as a numeric field with up to 3 digits and 2 decimal places
4. THE Payroll Engine SHALL accept Hourly Rate as a numeric field with up to 4 digits and 2 decimal places
5. THE Payroll Engine SHALL accept Tax Code as a 2-character alphanumeric field

### Requirement 2

**User Story:** As an Auditor, I want all monetary calculations performed using fixed-point arithmetic, so that results are exact and auditable without floating-point errors.

#### Acceptance Criteria

1. THE Payroll Engine SHALL perform all calculations using COBOL DECIMAL data types with exactly 2 decimal places
2. THE Payroll Engine SHALL calculate Gross Pay by multiplying Hours Worked by Hourly Rate
3. THE Payroll Engine SHALL round all intermediate calculations to 2 decimal places using banker's rounding
4. THE Payroll Engine SHALL maintain precision throughout the calculation chain without accumulating errors

### Requirement 3

**User Story:** As an Operator, I want federal and state taxes automatically calculated and deducted, so that net pay reflects all required withholdings.

#### Acceptance Criteria

1. THE Payroll Engine SHALL calculate Federal Tax as exactly 15% of Gross Pay
2. THE Payroll Engine SHALL calculate State Tax as exactly 5% of Gross Pay
3. THE Payroll Engine SHALL calculate Net Pay by subtracting Federal Tax and State Tax from Gross Pay
4. THE Payroll Engine SHALL ensure that Net Pay is never negative

### Requirement 4

**User Story:** As an Operator, I want calculation results written to a structured output file, so that the Python Bridge can parse and process the data for settlement.

#### Acceptance Criteria

1. WHEN calculations complete successfully, THE Payroll Engine SHALL write results to the Output File
2. THE Payroll Engine SHALL output Employee ID in a 10-character field
3. THE Payroll Engine SHALL output Gross Pay, Federal Tax, State Tax, and Net Pay as fixed-width numeric fields with 2 decimal places
4. THE Payroll Engine SHALL format all monetary values with leading zeros and fixed decimal positions
5. THE Payroll Engine SHALL write exactly one output record per input record processed

### Requirement 5

**User Story:** As an Operator, I want clear error handling for invalid input data, so that I can identify and correct data issues before settlement.

#### Acceptance Criteria

1. IF Hours Worked is negative or zero, THEN THE Payroll Engine SHALL reject the record and write an error message
2. IF Hourly Rate is negative or zero, THEN THE Payroll Engine SHALL reject the record and write an error message
3. IF Employee ID is blank or contains only spaces, THEN THE Payroll Engine SHALL reject the record and write an error message
4. WHEN an error occurs, THE Payroll Engine SHALL continue processing remaining records
5. THE Payroll Engine SHALL write a summary line indicating total records processed and total records with errors

### Requirement 6

**User Story:** As a Developer, I want the COBOL program to follow fixed-format conventions, so that it remains maintainable and compatible with standard COBOL compilers.

#### Acceptance Criteria

1. THE Payroll Engine SHALL use fixed-format COBOL with 80-column line width
2. THE Payroll Engine SHALL place sequence numbers in columns 1-6
3. THE Payroll Engine SHALL place indicators in column 7
4. THE Payroll Engine SHALL place code in columns 8-72
5. THE Payroll Engine SHALL use descriptive variable names following COBOL naming conventions
