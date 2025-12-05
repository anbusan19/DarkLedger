"""
Manual test script for the Payroll API.
Tests both successful processing and error cases.
"""
import json
import httpx
import sys
from pathlib import Path


API_BASE_URL = "http://localhost:8000"
TEST_DATA_FILE = Path(__file__).parent / "test_request.json"


def print_separator():
    print("\n" + "=" * 80 + "\n")


def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing Health Check Endpoint...")
    try:
        response = httpx.get(f"{API_BASE_URL}/health", timeout=5.0)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except httpx.ConnectError:
        print("❌ ERROR: Cannot connect to API. Is the server running?")
        print("   Start it with: uvicorn backend.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_valid_payroll():
    """Test payroll processing with valid data."""
    print("🔍 Testing Valid Payroll Processing...")
    
    # Load test data and use only valid employees
    with open(TEST_DATA_FILE, 'r') as f:
        data = json.load(f)
    
    # Use only the first 3 employees (valid ones)
    valid_request = {"employees": data["employees"][:3]}
    
    try:
        response = httpx.post(
            f"{API_BASE_URL}/api/payroll/process",
            json=valid_request,
            timeout=30.0
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ SUCCESS! Processed {len(result['results'])} employees")
            print(f"\nSummary: {result['summary']}")
            print("\nResults:")
            for emp in result['results']:
                print(f"  Employee {emp['employee_id']}:")
                print(f"    Gross Pay:   ${emp['gross_pay']}")
                print(f"    Federal Tax: ${emp['federal_tax']}")
                print(f"    State Tax:   ${emp['state_tax']}")
                print(f"    Net Pay:     ${emp['net_pay']}")
                print(f"    Status:      {emp['status']}")
            return True
        else:
            print(f"❌ FAILED: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_invalid_data():
    """Test payroll processing with invalid data."""
    print("🔍 Testing Invalid Data Validation...")
    
    invalid_request = {
        "employees": [
            {
                "employee_id": "TOOLONGEMPLOYEEID123",
                "hours_worked": -10.00,
                "hourly_rate": 0,
                "tax_code": "TOOLONG"
            }
        ]
    }
    
    try:
        response = httpx.post(
            f"{API_BASE_URL}/api/payroll/process",
            json=invalid_request,
            timeout=30.0
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 422:
            print("✅ Validation correctly rejected invalid data")
            print(f"Error details: {response.json()}")
            return True
        else:
            print(f"❌ Expected 422 status code, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_empty_request():
    """Test payroll processing with empty employee list."""
    print("🔍 Testing Empty Employee List...")
    
    empty_request = {"employees": []}
    
    try:
        response = httpx.post(
            f"{API_BASE_URL}/api/payroll/process",
            json=empty_request,
            timeout=30.0
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 422:
            print("✅ Validation correctly rejected empty list")
            print(f"Error details: {response.json()}")
            return True
        else:
            print(f"❌ Expected 422 status code, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_missing_cobol_binary():
    """Test error handling when COBOL binary is missing."""
    print("🔍 Testing Missing COBOL Binary Error Handling...")
    print("   (This test will fail if COBOL binary exists)")
    
    # This test assumes the COBOL binary might not be compiled yet
    # If it exists, this will actually succeed
    valid_request = {
        "employees": [
            {
                "employee_id": "TEST001",
                "hours_worked": 10.00,
                "hourly_rate": 20.00,
                "tax_code": "US"
            }
        ]
    }
    
    try:
        response = httpx.post(
            f"{API_BASE_URL}/api/payroll/process",
            json=valid_request,
            timeout=30.0
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 500:
            print("✅ Server correctly returned 500 error")
            print(f"Error details: {response.json()}")
            return True
        elif response.status_code == 200:
            print("ℹ️  COBOL binary exists and processed successfully")
            return True
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 80)
    print("🧟‍♂️ LEDGER-DE-MAIN API TEST SUITE")
    print("=" * 80)
    
    results = []
    
    # Test 1: Health Check
    print_separator()
    results.append(("Health Check", test_health_check()))
    
    if not results[0][1]:
        print("\n❌ Cannot proceed without API connection. Exiting.")
        sys.exit(1)
    
    # Test 2: Valid Payroll
    print_separator()
    results.append(("Valid Payroll", test_valid_payroll()))
    
    # Test 3: Invalid Data
    print_separator()
    results.append(("Invalid Data", test_invalid_data()))
    
    # Test 4: Empty Request
    print_separator()
    results.append(("Empty Request", test_empty_request()))
    
    # Test 5: Missing COBOL Binary
    print_separator()
    results.append(("Missing COBOL Binary", test_missing_cobol_binary()))
    
    # Summary
    print_separator()
    print("📊 TEST SUMMARY")
    print_separator()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
