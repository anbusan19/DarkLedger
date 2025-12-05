# Requirements Document

## Introduction

The Python Bridge is the integration layer that connects the modern web frontend with the legacy COBOL Payroll Engine. It provides a RESTful API for payroll processing, handles data format conversion between JSON and fixed-width text, manages subprocess execution of COBOL binaries, and ensures secure handling of API credentials for blockchain settlement. This component abstracts the complexity of COBOL integration while maintaining the precision and auditability of the legacy calculation engine.

## Glossary

- **Python Bridge**: The FastAPI application that mediates between the frontend and COBOL engine
- **API Endpoint**: HTTP endpoint that accepts JSON payroll requests and returns JSON responses
- **Format Converter**: Component that transforms JSON data to fixed-width text and vice versa
- **COBOL Executor**: Component that invokes the COBOL binary via subprocess
- **Pydantic Model**: Python data validation class that defines request/response schemas
- **Fixed-Width Format**: Text format where each field occupies a specific character position
- **Input File**: The `data/input.dat` file written by Python for COBOL consumption
- **Output File**: The `data/output.rpt` file written by COBOL for Python parsing
- **Key Manager**: Component that securely loads Coinbase API credentials from environment variables
- **Validation Error**: Error returned when input data fails Pydantic validation

## Requirements

### Requirement 1

**User Story:** As a Frontend Developer, I want to submit payroll data via a REST API endpoint, so that I can integrate payroll processing into the web application.

#### Acceptance Criteria

1. THE Python Bridge SHALL expose a POST endpoint at `/api/payroll/process`
2. THE Python Bridge SHALL accept JSON request bodies containing employee payroll data
3. THE Python Bridge SHALL return JSON responses with HTTP status codes indicating success or failure
4. THE Python Bridge SHALL use FastAPI framework for API implementation
5. THE Python Bridge SHALL enable CORS for frontend integration

### Requirement 2

**User Story:** As a Developer, I want input data validated before processing, so that invalid data is rejected before reaching the COBOL engine.

#### Acceptance Criteria

1. THE Python Bridge SHALL define Pydantic models for request validation
2. THE Python Bridge SHALL validate that Employee ID is a non-empty string with maximum 10 characters
3. THE Python Bridge SHALL validate that Hours Worked is a positive decimal number with maximum 2 decimal places
4. THE Python Bridge SHALL validate that Hourly Rate is a positive decimal number with maximum 2 decimal places
5. WHEN validation fails, THE Python Bridge SHALL return HTTP 422 status with detailed error messages

### Requirement 3

**User Story:** As a System Integrator, I want JSON data converted to fixed-width format, so that the COBOL program can read the input correctly.

#### Acceptance Criteria

1. THE Python Bridge SHALL convert Employee ID to a 10-character left-aligned field with space padding
2. THE Python Bridge SHALL convert Hours Worked to a 5-character numeric field in format 99999 (implied 2 decimals)
3. THE Python Bridge SHALL convert Hourly Rate to a 6-character numeric field in format 999999 (implied 2 decimals)
4. THE Python Bridge SHALL convert Tax Code to a 2-character left-aligned field with space padding
5. THE Python Bridge SHALL write formatted records to `data/input.dat` with exactly 23 bytes per record

### Requirement 4

**User Story:** As a System Administrator, I want the COBOL binary executed safely via subprocess, so that the system remains secure and errors are handled gracefully.

#### Acceptance Criteria

1. THE Python Bridge SHALL execute the COBOL binary at `cobol/bin/payroll` using subprocess
2. THE Python Bridge SHALL capture stdout and stderr from the COBOL process
3. WHEN the COBOL process exits with non-zero status, THE Python Bridge SHALL return HTTP 500 with error details
4. THE Python Bridge SHALL set a timeout of 30 seconds for COBOL execution
5. THE Python Bridge SHALL log subprocess execution details for debugging

### Requirement 5

**User Story:** As a Developer, I want fixed-width output parsed back to JSON, so that the frontend can display results in a structured format.

#### Acceptance Criteria

1. THE Python Bridge SHALL read the `data/output.rpt` file after COBOL execution
2. THE Python Bridge SHALL parse Employee ID from positions 1-10
3. THE Python Bridge SHALL parse Gross Pay, Federal Tax, State Tax, and Net Pay from their respective 12-character fields
4. THE Python Bridge SHALL parse the status field from positions 59-60
5. THE Python Bridge SHALL convert parsed monetary values to decimal numbers with 2 decimal places

### Requirement 6

**User Story:** As a Security Engineer, I want API credentials loaded from environment variables, so that sensitive keys are never hardcoded in source code.

#### Acceptance Criteria

1. THE Python Bridge SHALL load `COINBASE_API_KEY_NAME` from environment variables
2. THE Python Bridge SHALL load `COINBASE_PRIVATE_KEY` from environment variables
3. WHEN required environment variables are missing, THE Python Bridge SHALL raise a configuration error on startup
4. THE Python Bridge SHALL never log or expose API credentials in responses
5. THE Python Bridge SHALL provide a key manager module that encapsulates credential loading

### Requirement 7

**User Story:** As a Developer, I want comprehensive error handling, so that failures are reported clearly and the system remains stable.

#### Acceptance Criteria

1. WHEN the input file cannot be written, THE Python Bridge SHALL return HTTP 500 with a descriptive error message
2. WHEN the COBOL binary is not found, THE Python Bridge SHALL return HTTP 500 indicating missing executable
3. WHEN the output file cannot be read, THE Python Bridge SHALL return HTTP 500 with a descriptive error message
4. WHEN output parsing fails, THE Python Bridge SHALL return HTTP 500 with parsing error details
5. THE Python Bridge SHALL use try-except blocks to catch and handle all exceptions gracefully

### Requirement 8

**User Story:** As a Frontend Developer, I want clear API documentation, so that I can understand request/response formats without reading source code.

#### Acceptance Criteria

1. THE Python Bridge SHALL generate OpenAPI documentation automatically via FastAPI
2. THE Python Bridge SHALL serve interactive API docs at `/docs` endpoint
3. THE Python Bridge SHALL include example request and response bodies in the documentation
4. THE Python Bridge SHALL document all possible HTTP status codes and their meanings
5. THE Python Bridge SHALL include descriptions for all request and response fields
