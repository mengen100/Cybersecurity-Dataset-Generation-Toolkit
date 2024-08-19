import paramiko
import time
import random

def ssh_normal_usage(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password)
        print(f"Connected to {hostname}")

        # Simulate normal SSH usage
        commands = ["ls -l", "pwd", "date", "whoami", "uptime"]
        for _ in range(5):
            command = random.choice(commands)
            stdin, stdout, stderr = client.exec_command(command)
            print(f"Executed command: {command}")
            print(stdout.read().decode())
            time.sleep(random.uniform(1, 3))

        client.close()
        print("SSH session closed")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    hostname = "target_server"
    username = "root"
    password = "password"  # The correct password
    ssh_normal_usage(hostname, username, password)
