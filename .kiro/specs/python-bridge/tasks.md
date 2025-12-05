# Implementation Plan: Python Bridge

- [x] 1. Set up Python project structure and dependencies





  - Create `backend/` directory for Python source files
  - Create `requirements.txt` with FastAPI, Uvicorn, Pydantic dependencies
  - Create `backend/__init__.py` to make it a package
  - Add Python virtual environment to `.gitignore`
  - _Requirements: 1.4_

- [x] 2. Implement Pydantic data models






  - [x] 2.1 Create models.py with request models

    - Define `EmployeePayrollInput` model with employee_id (str, max 10 chars), hours_worked (Decimal, gt 0), hourly_rate (Decimal, gt 0), tax_code (str, 2 chars)
    - Define `PayrollRequest` model with employees list (min 1 item)
    - Add Field validators and example schemas for OpenAPI documentation
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 8.3_

  - [x] 2.2 Create models.py with response models





    - Define `EmployeePayrollOutput` model with employee_id, gross_pay, federal_tax, state_tax, net_pay, status fields
    - Define `PayrollResponse` model with results list and summary dict
    - Configure Decimal serialization for JSON responses
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 8.5_
-

- [x] 3. Implement format conversion functions





  - [x] 3.1 Create bridge.py with JSON to fixed-width converter

    - Implement `json_to_fixed_width()` function that converts EmployeePayrollInput to 23-byte string
    - Format Employee ID as 10-char left-aligned with space padding
    - Format Hours Worked as 5-char numeric (multiply by 100, zero-pad)
    - Format Hourly Rate as 6-char numeric (multiply by 100, zero-pad)
    - Format Tax Code as 2-char left-aligned
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [x] 3.2 Create bridge.py with fixed-width to JSON parser

    - Implement `parse_output_line()` function that parses 60-byte output record
    - Extract Employee ID from positions 1-10 (strip whitespace)
    - Extract and convert monetary values from positions 11-22, 23-34, 35-46, 47-58 (divide by 100, convert to Decimal)
    - Extract status from positions 59-60
    - Return dict with parsed values

    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [x] 3.3 Implement summary line parser





    - Implement `parse_summary_line()` function that extracts processed and error counts
    - Use regex or string parsing to extract numeric values from "SUMMARY: PROCESSED=nnnnn ERRORS=nnnnn"
    - Return dict with {"processed": int, "errors": int}
    - _Requirements: 5.1_








- [x] 4. Implement file I/O operations


  - [x] 4.1 Create write_input_file function





    - Implement `write_input_file()` that accepts list of EmployeePayrollInput
    - Convert each employee to fixed-width format using `json_to_fixed_width()`
    - Write all records to `data/input.dat` with newlines
    - Handle file write errors with try-except and raise descriptive exceptions
    - _Requirements: 3.5, 7.1_
  - [x] 4.2 Create read_output_file function





    - Implement `read_output_file()` that reads all lines from `data/output.rpt`
    - Return list of lines (excluding empty lines)
    - Handle file read errors with try-except and raise descriptive exceptions
    - _Requirements: 5.1, 7.3_


- [x] 5. Implement COBOL subprocess execution


  - [x] 5.1 Create execute_cobol function


    - Implement `execute_cobol()` using subprocess.run() with list args (not shell=True)
    - Set executable path to `cobol/bin/payroll` (or `cobol/bin/payroll.exe` on Windows)
    - Capture stdout and stderr with capture_output=True
    - Set timeout to 30 seconds
    - Check returncode and raise exception if non-zero
    - Log subprocess execution details (command, returncode, execution time)
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 7.2_

- [x] 6. Implement main orchestration function




  - [x] 6.1 Create process_payroll function in bridge.py


    - Implement `process_payroll()` that accepts PayrollRequest and returns PayrollResponse
    - Call `write_input_file()` with request.employees
    - Call `execute_cobol()` and handle subprocess errors
    - Call `read_output_file()` to get output lines
    - Parse each output line (except summary) using `parse_output_line()`
    - Parse summary line using `parse_summary_line()`
    - Build and return PayrollResponse with results and summary
    - Wrap all operations in try-except blocks with specific error handling
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 7. Implement key manager for credential loading




  - [x] 7.1 Create key_manager.py module


    - Define `KeyManager` class with __init__ that loads COINBASE_API_KEY_NAME and COINBASE_PRIVATE_KEY from os.getenv()
    - Raise ValueError if either environment variable is missing
    - Implement `get_credentials()` method that returns tuple of (api_key_name, private_key)
    - Implement __repr__ that masks credentials in logs
    - Create singleton instance `key_manager` at module level
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 8. Implement FastAPI application and routes






  - [x] 8.1 Create main.py with FastAPI app initialization

    - Initialize FastAPI app with title="Ledger-De-Main API" and version="1.0.0"
    - Configure CORS middleware with allowed origins ["http://localhost:3000", "http://localhost:5173"]
    - Set allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
    - _Requirements: 1.1, 1.4, 1.5_

  - [x] 8.2 Implement POST /api/payroll/process endpoint

    - Define route handler that accepts PayrollRequest body
    - Call `process_payroll()` from bridge.py
    - Return PayrollResponse with HTTP 200 on success
    - Handle validation errors (automatic via Pydantic, returns 422)
    - Handle processing errors with try-except, return HTTP 500 with error details
    - Add OpenAPI documentation with descriptions and examples
    - _Requirements: 1.1, 1.2, 1.3, 2.5, 7.1, 7.2, 7.3, 7.4, 7.5, 8.1, 8.2, 8.3, 8.4, 8.5_

  - [x] 8.3 Implement GET /health endpoint

    - Define simple health check route that returns {"status": "healthy"}
    - Return HTTP 200
    - _Requirements: 1.1_
  - [x] 8.4 Configure logging


    - Set up Python logging with INFO level
    - Configure log format with timestamp, logger name, level, and message
    - Create logger instance for the bridge module
    - _Requirements: 4.5_

- [x] 9. Create test data and manual testing script






  - [x] 9.1 Create sample JSON request file

    - Create `backend/test_request.json` with 3 valid employees and 1 invalid (for testing validation)
    - Include varied hours and rates to test calculations
    - _Requirements: 1.2, 2.1, 2.2, 2.3, 2.4_

  - [x] 9.2 Create manual test script

    - Create `backend/test_api.py` or shell script that uses curl/httpx to call the API
    - Send POST request to /api/payroll/process with test_request.json
    - Display response and verify format
    - Test error cases (invalid data, missing COBOL binary)
    - _Requirements: 1.1, 1.2, 1.3_

- [x] 10. Verify end-to-end integration






  - [x] 10.1 Start FastAPI server

    - Run `uvicorn backend.main:app --reload` and verify server starts without errors
    - Check that /docs endpoint is accessible and shows API documentation
    - Verify CORS headers are present in responses
    - _Requirements: 1.4, 8.1, 8.2_

  - [x] 10.2 Test payroll processing flow

    - Send POST request with valid employee data
    - Verify input.dat is created with correct format
    - Verify COBOL binary executes successfully
    - Verify output.rpt is parsed correctly
    - Verify JSON response matches expected calculations
    - Test error handling (invalid input, missing files)
    - _Requirements: 1.1, 1.2, 1.3, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5, 7.1, 7.2, 7.3, 7.4, 7.5_
