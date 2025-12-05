"""
Quick test to verify backend is ready for frontend integration
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✓ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_payroll():
    """Test payroll processing endpoint"""
    print("\nTesting payroll processing...")
    payload = {
        "employees": [
            {
                "employee_id": "EMP001",
                "hours_worked": "40.00",
                "hourly_rate": "25.50",
                "tax_code": "US",
                "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/payroll/process",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.ok:
            result = response.json()
            print(f"✓ Payroll processing successful")
            print(f"  Employee: {result['results'][0]['employee_id']}")
            print(f"  Net Pay: {result['results'][0]['net_pay']}")
            return True
        else:
            print(f"✗ Payroll processing failed: {response.status_code}")
            print(f"  {response.text}")
            return False
    except Exception as e:
        print(f"✗ Payroll processing failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("FRONTEND INTEGRATION TEST")
    print("=" * 60)
    print("\nMake sure the backend is running:")
    print("  cd backend")
    print("  uvicorn main:app --reload")
    print("\n" + "=" * 60 + "\n")
    
    health_ok = test_health()
    
    if health_ok:
        test_payroll()
    
    print("\n" + "=" * 60)
    print("If all tests pass, start the frontend:")
    print("  cd frontend")
    print("  npm run dev")
    print("=" * 60)
