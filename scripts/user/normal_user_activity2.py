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
        
        time.sleep(random.uniform(1, 3))  # Random delay between requests

def login(base_url, username, password):
    login_url = f"{base_url}/login.php"
    data = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(login_url, data=data)
        print(f"Logging in as {username}")
        print(f"Response status: {response.status_code}")
        return "Welcome" in response.text
    except Exception as e:
        print(f"Login error: {str(e)}")
        return False

def upload_file(base_url):
    upload_url = f"{base_url}/upload.php"
    files = {'file': ('benign_file.txt', 'This is a benign file content')}
    try:
        response = requests.post(upload_url, files=files)
        print("Uploading benign file")
        print(f"Response status: {response.status_code}")
    except Exception as e:
        print(f"Upload error: {str(e)}")

def main():
    base_url = "http://172.16.238.2"  # Replace with your web server's IP
    
    # Simulate normal browsing
    normal_web_usage(base_url)
    
    # Attempt login
    if login(base_url, "user1", "password123"):
        print("Login successful")
        # Perform actions as logged-in user
        normal_web_usage(base_url)
        upload_file(base_url)
    else:
        print("Login failed")

    print("Benign user simulation completed")

if __name__ == "__main__":
    main()

    simulation_id = os.environ.get('SIMULATION_ID', 'unknown')
    with open(f'/signals/user_done_{simulation_id}', 'w') as f:
        f.write('done')