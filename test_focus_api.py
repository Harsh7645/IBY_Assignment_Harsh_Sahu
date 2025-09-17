import requests
import json

def test_focus_endpoints():
    base_url = "http://localhost:8000/api/focus"
    
    try:
        print("Testing daily-progress endpoint...")
        response = requests.get(f"{base_url}/daily-progress")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {str(e)}")
    
    try:
        print("\nTesting targets endpoint...")
        response = requests.get(f"{base_url}/targets")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {str(e)}")
    
    try:
        print("\nTesting active-session endpoint...")
        response = requests.get(f"{base_url}/active-session")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {str(e)}")

if __name__ == "__main__":
    test_focus_endpoints()