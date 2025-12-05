"""
Test API Endpoint

Tests the /api/payroll/process-and-settle endpoint
"""

import requests
import json

def test_api():
    """Test the combined payroll and settlement endpoint"""
    
    print("=" * 60)
    print("🧟‍♂️ TESTING API ENDPOINT")
    print("=" * 60)
    print()
    
    # API endpoint
    url = "http://127.0.0.1:8000/api/payroll/process-and-settle"
    
    # Test payload
    payload = {
        "employees": [
            {
                "employee_id": "EMP001",
                "hours_worked": "40.00",
                "hourly_rate": "25.50",
                "tax_code": "US",
                "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2"
            },
            {
                "employee_id": "EMP002",
                "hours_worked": "35.00",
                "hourly_rate": "30.00",
                "tax_code": "US",
                "wallet_address": "0x1234567890123456789012345678901234567890"
            }
        ]
    }
    
    print("Sending POST request to API...")
    print(f"URL: {url}")
    print(f"Payload: {len(payload['employees'])} employees")
    print()
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ API Response:")
            print()
            print("Payroll Results:")
            for result in data['payroll']['results']:
                print(f"  {result['employee_id']}: ${result['net_pay']} ({result['status']})")
            print()
            
            print("Settlement Results:")
            print(f"  Processed: {data['settlement']['total_processed']}")
            print(f"  Succeeded: {data['settlement']['total_succeeded']}")
            print(f"  Failed: {data['settlement']['total_failed']}")
            print()
            
            for result in data['settlement']['results']:
                status_icon = "✅" if result['status'] == 'success' else "❌"
                print(f"  {status_icon} {result.get('employee_id', 'N/A')}: {result['amount']} USDC")
                if result['status'] == 'success':
                    print(f"     TX: {result['transaction_hash'][:30]}...")
            
            print()
            print("=" * 60)
            print("🎉 API TEST SUCCESSFUL!")
            print("=" * 60)
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API")
        print("   Make sure the server is running:")
        print("   uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_api()
