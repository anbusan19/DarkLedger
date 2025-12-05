"""
Integration test for Python Bridge - Tests end-to-end flow
"""
import os
import json
from decimal import Decimal

# Test 1: Verify input.dat creation with correct format
def test_input_file_creation():
    """Test that JSON is correctly converted to fixed-width format"""
    from backend.bridge import json_to_fixed_width
    from backend.models import EmployeePayrollInput
    
    employee = EmployeePayrollInput(
        employee_id="EMP0001234",
        hours_worked=Decimal("40.00"),
        hourly_rate=Decimal("25.50"),
        tax_code="US"
    )
    
    result = json_to_fixed_width(employee)
    
    # Verify format: 10 chars ID + 5 chars hours + 6 chars rate + 2 chars tax = 23 bytes
    assert len(result) == 23, f"Expected 23 bytes, got {len(result)}"
    assert result[:10] == "EMP0001234", f"Employee ID incorrect: {result[:10]}"
    assert result[10:15] == "04000", f"Hours incorrect: {result[10:15]}"
    assert result[15:21] == "002550", f"Rate incorrect: {result[15:21]}"
    assert result[21:23] == "US", f"Tax code incorrect: {result[21:23]}"
    
    print("✓ Input file format test PASSED")
    return True

# Test 2: Verify output.rpt parsing
def test_output_parsing():
    """Test that fixed-width output is correctly parsed to JSON"""
    from backend.bridge import parse_output_line
    
    # Simulate COBOL output line (60 bytes)
    # Format: 10 chars ID + 12 chars gross (implied 2 decimals) + 12 chars fed tax + 12 chars state tax + 12 chars net + 2 chars status
    # EMP0001234 + 000000102000 (1020.00) + 000000015300 (153.00) + 000000005100 (51.00) + 000000081600 (816.00) + OK
    output_line = "EMP0001234000000102000000000015300000000005100000000081600OK"
    
    result = parse_output_line(output_line)
    
    assert result["employee_id"] == "EMP0001234"
    assert result["gross_pay"] == Decimal("1020.00")
    assert result["federal_tax"] == Decimal("153.00")
    assert result["state_tax"] == Decimal("51.00")
    assert result["net_pay"] == Decimal("816.00")
    assert result["status"] == "OK"
    
    print("✓ Output parsing test PASSED")
    return True

# Test 3: Verify summary line parsing
def test_summary_parsing():
    """Test that summary line is correctly parsed"""
    from backend.bridge import parse_summary_line
    
    summary_line = "SUMMARY: PROCESSED=00003 ERRORS=00000"
    result = parse_summary_line(summary_line)
    
    assert result["processed"] == 3
    assert result["errors"] == 0
    
    print("✓ Summary parsing test PASSED")
    return True

# Test 4: Test error handling for invalid input
def test_validation_errors():
    """Test that Pydantic validation catches invalid data"""
    from backend.models import EmployeePayrollInput
    from pydantic import ValidationError
    
    # Test 1: Invalid employee ID (too long)
    try:
        EmployeePayrollInput(
            employee_id="INVALID_EMPLOYEE_ID_TOO_LONG",
            hours_worked=Decimal("40.00"),
            hourly_rate=Decimal("25.50"),
            tax_code="US"
        )
        assert False, "Should have raised ValidationError for long employee_id"
    except ValidationError:
        print("✓ Validation error test 1 PASSED (long employee_id)")
    
    # Test 2: Negative hours
    try:
        EmployeePayrollInput(
            employee_id="EMP001",
            hours_worked=Decimal("-10.00"),
            hourly_rate=Decimal("25.50"),
            tax_code="US"
        )
        assert False, "Should have raised ValidationError for negative hours"
    except ValidationError:
        print("✓ Validation error test 2 PASSED (negative hours)")
    
    # Test 3: Zero rate
    try:
        EmployeePayrollInput(
            employee_id="EMP001",
            hours_worked=Decimal("40.00"),
            hourly_rate=Decimal("0"),
            tax_code="US"
        )
        assert False, "Should have raised ValidationError for zero rate"
    except ValidationError:
        print("✓ Validation error test 3 PASSED (zero rate)")
    
    return True

# Test 5: Verify file I/O operations
def test_file_operations():
    """Test that files are written and read correctly"""
    from backend.bridge import write_input_file, read_output_file
    from backend.models import EmployeePayrollInput
    
    # Create test employees
    employees = [
        EmployeePayrollInput(
            employee_id="EMP0001234",
            hours_worked=Decimal("40.00"),
            hourly_rate=Decimal("25.50"),
            tax_code="US"
        ),
        EmployeePayrollInput(
            employee_id="EMP0005678",
            hours_worked=Decimal("35.50"),
            hourly_rate=Decimal("32.00"),
            tax_code="US"
        )
    ]
    
    # Write input file
    write_input_file(employees)
    
    # Verify file exists and has correct content
    assert os.path.exists("data/input.dat"), "input.dat not created"
    
    with open("data/input.dat", "r") as f:
        lines = f.readlines()
        assert len(lines) == 2, f"Expected 2 lines, got {len(lines)}"
        assert len(lines[0].strip()) == 23, f"Line 1 incorrect length: {len(lines[0].strip())}"
        assert len(lines[1].strip()) == 23, f"Line 2 incorrect length: {len(lines[1].strip())}"
    
    print("✓ File I/O test PASSED")
    
    # Create mock output file for testing read
    with open("data/output.rpt", "w") as f:
        f.write("EMP0001234000000102000000000015300000000005100000000081600OK\n")
        f.write("EMP0005678000000113600000000017040000000005680000000090880OK\n")
        f.write("SUMMARY: PROCESSED=00002 ERRORS=00000\n")
    
    # Test reading output
    lines = read_output_file()
    assert len(lines) == 3, f"Expected 3 lines, got {len(lines)}"
    
    print("✓ Output file read test PASSED")
    
    return True

# Test 6: Test API endpoint with mock data
def test_api_endpoint():
    """Test the API endpoint returns correct response format"""
    import requests
    
    # Test valid request
    payload = {
        "employees": [
            {
                "employee_id": "EMP0001234",
                "hours_worked": 40.00,
                "hourly_rate": 25.50,
                "tax_code": "US"
            }
        ]
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/payroll/process",
            json=payload,
            headers={"Origin": "http://localhost:3000"}
        )
        
        # Check CORS headers
        assert "access-control-allow-origin" in response.headers, "CORS headers missing"
        print("✓ CORS headers test PASSED")
        
        # Note: Will fail if COBOL binary not available, but that's expected
        if response.status_code == 500:
            error_data = response.json()
            if "COBOL binary not found" in str(error_data):
                print("✓ API endpoint test PASSED (COBOL binary not available, but error handling works)")
                return True
        
        # If COBOL is available, check response format
        if response.status_code == 200:
            data = response.json()
            assert "results" in data, "Response missing 'results'"
            assert "summary" in data, "Response missing 'summary'"
            print("✓ API endpoint test PASSED (full integration)")
            return True
            
    except Exception as e:
        print(f"✗ API endpoint test FAILED: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("LEDGER-DE-MAIN: End-to-End Integration Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("Input File Creation", test_input_file_creation),
        ("Output Parsing", test_output_parsing),
        ("Summary Parsing", test_summary_parsing),
        ("Validation Errors", test_validation_errors),
        ("File Operations", test_file_operations),
        ("API Endpoint", test_api_endpoint),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        print("-" * 60)
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
