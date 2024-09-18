import requests
import time
import random
import os

def normal_activity(base_url):
    actions = [
        ('GET', '/'),
        ('GET', '/login'),
        ('POST', '/login', {'username': 'user', 'password': 'password'}),
        ('GET', '/profile'),
        ('GET', '/contact'),
    ]

    session = requests.Session()

    for _ in range(10):
        action = random.choice(actions)
        url = base_url + action[1]
        
        try:
            if action[0] == 'GET':
                response = session.get(url)
            elif action[0] == 'POST':
                response = session.post(url, data=action[2])
            
            print(f"{action[0]} {url} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {url}: {str(e)}")
        
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    base_url = "http://172.16.238.2"
    normal_activity(base_url)

    simulation_id = os.environ.get('SIMULATION_ID', 'unknown')
    with open(f'/signals/user_done_{simulation_id}', 'w') as f:
        f.write('done')