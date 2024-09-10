import requests
import time
import random

def normal_web_usage(base_url):
    actions = [
        "/",
        "/login?username=user1&password=pass1",
        "/profile?id=1",
        "/search?q=product",
        "/about",
        "/contact"
    ]

    for _ in range(10):  # Perform 10 random actions
        action = random.choice(actions)
        url = f"{base_url}{action}"
        try:
            response = requests.get(url)
            print(f"Accessing: {url}")
            print(f"Response status: {response.status_code}")
        except Exception as e:
            print(f"Error occurred: {str(e)}")
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    base_url = "http://172.16.238.2"
    normal_web_usage(base_url)

    simulation_id = os.environ.get('SIMULATION_ID', 'unknown')
    with open(f'/signals/user_done_{simulation_id}', 'w') as f:
        f.write('done')