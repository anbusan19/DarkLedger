"""
Bridge module for COBOL integration.
Handles format conversion between JSON and fixed-width text formats.

THE STITCHING: Real work is done by the COBOL binary.
This module just translates between modern JSON and legacy fixed-width formats.
"""

import os
import re
import sys
import time
import logging
import subprocess
from decimal import Decimal
from typing import List, Dict
from backend.models import EmployeePayrollInput, PayrollRequest, PayrollResponse, EmployeePayrollOutput

# Configure logging for the bridge module
logger = logging.getLogger("payroll_bridge")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def json_to_fixed_width(employee: EmployeePayrollInput) -> str:
    """
    Convert JSON employee data to 23-byte fixed-width record for COBOL.
    
    Fixed-Width Format (23 bytes total):
    - Employee ID: positions 1-10 (left-aligned, space-padded)
    - Hours Worked: positions 11-15 (99999, implied 2 decimals, multiply by 100)
    - Hourly Rate: positions 16-21 (999999, implied 2 decimals, multiply by 100)
    - Tax Code: positions 22-23 (left-aligned)
    
    Example:
        Input: EmployeePayrollInput(
            employee_id="EMP001",
            hours_worked=Decimal("40.00"),
            hourly_rate=Decimal("25.50"),
            tax_code="US"
        )
        Output: "EMP001    0400002550US"
    
    Args:
        employee: Validated employee payroll input
        
    Returns:
        23-byte fixed-width string ready for COBOL consumption
    """
    # Format Employee ID: 10 characters, left-aligned, space-padded
    emp_id = employee.employee_id.ljust(10)[:10]
    
    # Format Hours Worked: 5 digits, multiply by 100 to remove decimals, zero-pad
    hours_cents = int(employee.hours_worked * 100)
    hours_str = str(hours_cents).zfill(5)
    
    # Format Hourly Rate: 6 digits, multiply by 100 to remove decimals, zero-pad
    rate_cents = int(employee.hourly_rate * 100)
    rate_str = str(rate_cents).zfill(6)
    
    # Format Tax Code: 2 characters, left-aligned
    tax_code = employee.tax_code.ljust(2)[:2]
    
    # Combine all fields into 23-byte record
    record = f"{emp_id}{hours_str}{rate_str}{tax_code}"
    
    return record


def parse_output_line(line: str) -> Dict:
    """
    Parse a 60-byte fixed-width output record from COBOL.
    
    Fixed-Width Format (60 bytes total):
    - Employee ID: positions 1-10
    - Gross Pay: positions 11-22 (9(8)V99 format, divide by 100)
    - Federal Tax: positions 23-34 (9(8)V99 format, divide by 100)
    - State Tax: positions 35-46 (9(8)V99 format, divide by 100)
    - Net Pay: positions 47-58 (9(8)V99 format, divide by 100)
    - Status: positions 59-60 ("OK" or "ER")
    
    Example:
        Input: "EMP0001234000001020000000015300000000051000000008160OK"
        Output: {
            "employee_id": "EMP0001234",
            "gross_pay": Decimal("1020.00"),
            "federal_tax": Decimal("153.00"),
            "state_tax": Decimal("51.00"),
            "net_pay": Decimal("816.00"),
            "status": "OK"
        }
    
    Args:
        line: 60-byte fixed-width output line from COBOL
        
    Returns:
        Dictionary with parsed values (monetary values as Decimal)
        
    Raises:
        ValueError: If line length is not 60 bytes or parsing fails
    """
    if len(line) < 60:
        raise ValueError(f"Output line too short: expected 60 bytes, got {len(line)}")
    
    # Extract Employee ID (positions 1-10, strip trailing spaces)
    employee_id = line[0:10].strip()
    
    # Extract monetary values (positions 11-22, 23-34, 35-46, 47-58)
    # These are stored as integers with implied 2 decimal places
    gross_pay_str = line[10:22].strip()
    federal_tax_str = line[22:34].strip()
    state_tax_str = line[34:46].strip()
    net_pay_str = line[46:58].strip()
    
    # Convert to Decimal, dividing by 100 to restore decimal places
    gross_pay = Decimal(gross_pay_str) / 100 if gross_pay_str else Decimal("0.00")
    federal_tax = Decimal(federal_tax_str) / 100 if federal_tax_str else Decimal("0.00")
    state_tax = Decimal(state_tax_str) / 100 if state_tax_str else Decimal("0.00")
    net_pay = Decimal(net_pay_str) / 100 if net_pay_str else Decimal("0.00")
    
    # Extract status (positions 59-60)
    status = line[58:60].strip()
    
    return {
        "employee_id": employee_id,
        "gross_pay": gross_pay,
        "federal_tax": federal_tax,
        "state_tax": state_tax,
        "net_pay": net_pay,
        "status": status
    }


def parse_summary_line(line: str) -> Dict[str, int]:
    """
    Parse summary line from COBOL output.
    
    Expected format: "SUMMARY: PROCESSED=nnnnn ERRORS=nnnnn"
    
    Example:
        Input: "SUMMARY: PROCESSED=00042 ERRORS=00003"
        Output: {"processed": 42, "errors": 3}
    
    Args:
        line: Summary line from COBOL output
        
    Returns:
        Dictionary with processed and error counts
        
    Raises:
        ValueError: If line format is invalid or numbers cannot be extracted
    """
    # Use regex to extract numeric values
    processed_match = re.search(r'PROCESSED=(\d+)', line)
    errors_match = re.search(r'ERRORS=(\d+)', line)
    
    if not processed_match or not errors_match:
        raise ValueError(f"Invalid summary line format: {line}")
    
    processed = int(processed_match.group(1))
    errors = int(errors_match.group(1))
    
    return {
        "processed": processed,
        "errors": errors
    }


def write_input_file(employees: List[EmployeePayrollInput]) -> None:
    """
    Write employee payroll data to input file for COBOL processing.
    
    Converts each employee record to fixed-width format and writes to data/input.dat.
    Each record is 23 bytes followed by a newline character.
    
    THE STITCHING: This prepares data for the COBOL binary to consume.
    
    Example:
        employees = [
            EmployeePayrollInput(employee_id="EMP001", hours_worked=40.00, ...),
            EmployeePayrollInput(employee_id="EMP002", hours_worked=35.50, ...)
        ]
        write_input_file(employees)
        # Creates data/input.dat with:
        # EMP001    0400002550US
        # EMP002    0355002550US
    
    Args:
        employees: List of validated employee payroll input records
        
    Raises:
        IOError: If file cannot be written (permissions, disk space, etc.)
        OSError: If data directory doesn't exist and cannot be created
    """
    input_file_path = "data/input.dat"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Convert all employees to fixed-width format
        records = [json_to_fixed_width(emp) for emp in employees]
        
        # Write all records to file with newlines
        with open(input_file_path, 'w') as f:
            for record in records:
                f.write(record + '\n')
                
    except PermissionError as e:
        raise IOError(f"Permission denied writing to {input_file_path}: {e}")
    except OSError as e:
        raise IOError(f"Failed to write input file {input_file_path}: {e}")


def read_output_file() -> List[str]:
    """
    Read COBOL output file and return all non-empty lines.
    
    Reads data/output.rpt which contains employee payroll results and a summary line.
    Empty lines are filtered out.
    
    THE STITCHING: This reads the results produced by the COBOL binary.
    
    Example:
        lines = read_output_file()
        # Returns:
        # [
        #   "EMP0001234000001020000000015300000000051000000008160OK",
        #   "EMP0005678000000890000000013350000000044500000007120OK",
        #   "SUMMARY: PROCESSED=00002 ERRORS=00000"
        # ]
    
    Returns:
        List of non-empty lines from the output file
        
    Raises:
        FileNotFoundError: If output.rpt doesn't exist (COBOL didn't run or failed)
        IOError: If file cannot be read (permissions, etc.)
    """
    output_file_path = "data/output.rpt"
    
    try:
        with open(output_file_path, 'r') as f:
            lines = f.readlines()
        
        # Strip whitespace and filter out empty lines
        lines = [line.strip() for line in lines if line.strip()]
        
        return lines
        
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Output file {output_file_path} not found. "
            "COBOL binary may not have executed successfully."
        )
    except PermissionError as e:
        raise IOError(f"Permission denied reading {output_file_path}: {e}")
    except OSError as e:
        raise IOError(f"Failed to read output file {output_file_path}: {e}")



def execute_cobol() -> subprocess.CompletedProcess:
    """
    Execute the COBOL payroll binary via subprocess.
    
    THE STITCHING: This invokes the legacy COBOL brain to perform calculations.
    Real work is done by the binary - Python just manages the execution.
    
    The function:
    - Detects the correct binary path based on OS (Windows vs Unix)
    - Executes the binary with timeout protection
    - Captures stdout and stderr for debugging
    - Logs execution details (command, returncode, duration)
    - Raises exceptions for execution failures
    
    Expected behavior:
    - COBOL binary reads from data/input.dat
    - COBOL binary writes to data/output.rpt
    - Returns CompletedProcess with returncode 0 on success
    
    Example:
        result = execute_cobol()
        # Logs: "Executing COBOL binary: cobol/bin/payroll"
        # Logs: "COBOL execution completed in 0.523s with returncode 0"
    
    Returns:
        subprocess.CompletedProcess object with stdout, stderr, and returncode
        
    Raises:
        FileNotFoundError: If COBOL binary doesn't exist at expected path
        subprocess.TimeoutExpired: If execution exceeds 30 seconds
        subprocess.CalledProcessError: If COBOL binary exits with non-zero code
        OSError: If subprocess execution fails for other reasons
    """
    # Determine the correct binary path based on operating system
    if sys.platform == "win32":
        binary_path = "cobol/bin/payroll.exe"
    else:
        binary_path = "cobol/bin/payroll"
    
    # Check if binary exists before attempting execution
    if not os.path.exists(binary_path):
        error_msg = (
            f"COBOL binary not found at {binary_path}. "
            "Please compile the COBOL source code first."
        )
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    # Log the execution attempt
    logger.info(f"Executing COBOL binary: {binary_path}")
    
    try:
        # Record start time for performance logging
        start_time = time.time()
        
        # Execute COBOL binary with subprocess.run()
        # Use list args (not shell=True) to prevent shell injection
        result = subprocess.run(
            [binary_path],
            capture_output=True,  # Capture stdout and stderr
            text=True,            # Return output as strings, not bytes
            timeout=30,           # 30 second timeout
            check=False           # Don't raise exception yet, we'll check manually
        )
        
        # Calculate execution duration
        duration = time.time() - start_time
        
        # Log execution results
        logger.info(
            f"COBOL execution completed in {duration:.3f}s with returncode {result.returncode}"
        )
        
        # Log stdout if present (for debugging)
        if result.stdout:
            logger.debug(f"COBOL stdout: {result.stdout}")
        
        # Log stderr if present (may contain warnings or errors)
        if result.stderr:
            logger.warning(f"COBOL stderr: {result.stderr}")
        
        # Check return code and raise exception if non-zero
        if result.returncode != 0:
            error_msg = (
                f"COBOL binary exited with non-zero status {result.returncode}. "
                f"stderr: {result.stderr}"
            )
            logger.error(error_msg)
            raise subprocess.CalledProcessError(
                result.returncode,
                [binary_path],
                output=result.stdout,
                stderr=result.stderr
            )
        
        return result
        
    except subprocess.TimeoutExpired as e:
        error_msg = f"COBOL execution timed out after 30 seconds"
        logger.error(error_msg)
        raise subprocess.TimeoutExpired(
            cmd=[binary_path],
            timeout=30,
            output=e.output,
            stderr=e.stderr
        )
    except OSError as e:
        error_msg = f"Failed to execute COBOL binary: {e}"
        logger.error(error_msg)
        raise OSError(error_msg)


def process_payroll(request: PayrollRequest) -> PayrollResponse:
    """
    Main orchestration function for payroll processing.
    
    THE STITCHING: This is the master conductor that coordinates all components:
    1. Converts JSON to fixed-width format
    2. Writes input file for COBOL
    3. Executes the COBOL binary (where the real work happens)
    4. Reads COBOL output file
    5. Parses results back to JSON
    6. Returns structured response
    
    This function wraps all operations in comprehensive error handling to ensure
    failures are reported clearly to the API consumer.
    
    Example:
        request = PayrollRequest(employees=[
            EmployeePayrollInput(
                employee_id="EMP001",
                hours_worked=Decimal("40.00"),
                hourly_rate=Decimal("25.50"),
                tax_code="US"
            )
        ])
        response = process_payroll(request)
        # Returns PayrollResponse with results and summary
    
    Args:
        request: PayrollRequest containing list of employees to process
        
    Returns:
        PayrollResponse with processed results and summary statistics
        
    Raises:
        IOError: If input file cannot be written or output file cannot be read
        FileNotFoundError: If COBOL binary or output file doesn't exist
        subprocess.CalledProcessError: If COBOL execution fails
        subprocess.TimeoutExpired: If COBOL execution exceeds timeout
        ValueError: If output parsing fails
        Exception: For any other unexpected errors during processing
    """
    logger.info(f"Starting payroll processing for {len(request.employees)} employees")
    
    try:
        # Step 1: Write input file
        # Convert JSON employee data to fixed-width format and write to data/input.dat
        logger.info("Writing input file for COBOL processing")
        try:
            write_input_file(request.employees)
            logger.info(f"Successfully wrote {len(request.employees)} records to data/input.dat")
        except IOError as e:
            error_msg = f"Failed to write input file: {e}"
            logger.error(error_msg)
            raise IOError(error_msg)
        
        # Step 2: Execute COBOL binary
        # THE BRAIN DOES THE WORK: Invoke the legacy COBOL payroll engine
        logger.info("Executing COBOL payroll binary")
        try:
            cobol_result = execute_cobol()
            logger.info("COBOL execution completed successfully")
        except FileNotFoundError as e:
            error_msg = f"COBOL binary not found: {e}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        except subprocess.TimeoutExpired as e:
            error_msg = f"COBOL execution timed out: {e}"
            logger.error(error_msg)
            raise subprocess.TimeoutExpired(
                cmd=e.cmd,
                timeout=e.timeout,
                output=e.output,
                stderr=e.stderr
            )
        except subprocess.CalledProcessError as e:
            error_msg = f"COBOL execution failed with exit code {e.returncode}: {e.stderr}"
            logger.error(error_msg)
            raise subprocess.CalledProcessError(
                returncode=e.returncode,
                cmd=e.cmd,
                output=e.output,
                stderr=e.stderr
            )
        except OSError as e:
            error_msg = f"Failed to execute COBOL binary: {e}"
            logger.error(error_msg)
            raise OSError(error_msg)
        
        # Step 3: Read output file
        # Read the results produced by COBOL from data/output.rpt
        logger.info("Reading COBOL output file")
        try:
            output_lines = read_output_file()
            logger.info(f"Successfully read {len(output_lines)} lines from output file")
        except FileNotFoundError as e:
            error_msg = f"Output file not found: {e}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        except IOError as e:
            error_msg = f"Failed to read output file: {e}"
            logger.error(error_msg)
            raise IOError(error_msg)
        
        # Step 4: Parse output lines
        # Separate employee results from summary line
        results = []
        summary = {"processed": 0, "errors": 0}
        
        logger.info("Parsing COBOL output")
        try:
            for line in output_lines:
                # Check if this is the summary line
                if line.startswith("SUMMARY:"):
                    summary = parse_summary_line(line)
                    logger.info(f"Parsed summary: {summary}")
                else:
                    # Parse employee result line
                    parsed_result = parse_output_line(line)
                    
                    # Convert to EmployeePayrollOutput model
                    employee_output = EmployeePayrollOutput(
                        employee_id=parsed_result["employee_id"],
                        gross_pay=parsed_result["gross_pay"],
                        federal_tax=parsed_result["federal_tax"],
                        state_tax=parsed_result["state_tax"],
                        net_pay=parsed_result["net_pay"],
                        status=parsed_result["status"]
                    )
                    results.append(employee_output)
            
            logger.info(f"Successfully parsed {len(results)} employee results")
            
        except ValueError as e:
            error_msg = f"Failed to parse output: {e}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error during output parsing: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # Step 5: Build and return response
        response = PayrollResponse(
            results=results,
            summary=summary
        )
        
        logger.info(
            f"Payroll processing completed successfully: "
            f"{summary['processed']} processed, {summary['errors']} errors"
        )
        
        return response
        
    except Exception as e:
        # Catch-all for any unexpected errors
        error_msg = f"Unexpected error during payroll processing: {e}"
        logger.error(error_msg)
        raise Exception(error_msg)
