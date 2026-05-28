import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_route(path, method="GET", expected_status=200):
    url = f"{BASE_URL}{path}"
    try:
        if method == "GET":
            response = requests.get(url, allow_redirects=True)
        else:
            response = requests.post(url, allow_redirects=True)
            
        print(f"Testing {method} {path}...")
        if response.status_code == expected_status:
            print(f"  SUCCESS: Status {response.status_code}")
        else:
            print(f"  FAILED: Status {response.status_code} (Expected {expected_status})")
            return False
        return True
    except requests.exceptions.ConnectionError:
        print(f"  ERROR: Could not connect to {BASE_URL}. Is the server running?")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def main():
    print("Starting Verification...")
    
    # 1. Test Home
    test_route("/")
    
    # 2. Test 404
    test_route("/nonexistent_path_123", expected_status=404)
    
    # 3. Test POST-only routes now redirected on GET
    test_route("/admindashboard", expected_status=200) # Should redirect to login
    test_route("/emp_Registration_process", expected_status=200) # Should redirect to Registration
    test_route("/search_emp_process", expected_status=200) # Should redirect to search page
    test_route("/leave_action", expected_status=200) # Should redirect
    
    print("\nVerification Complete.")

if __name__ == "__main__":
    main()
