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
        commands = ["whoami", "pwd", "ls -l", "date", "uptime"]
        for i in range(5):
            # command = random.choice(commands)
            stdin, stdout, stderr = client.exec_command(commands[i])
            print(f"Executed command: {commands[i]}")
            print(stdout.read().decode())
            time.sleep(random.uniform(1, 3))

        client.close()
        print("SSH session closed")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    hostname = "ssh_server"
    username = "root"
    password = "simulation_default_pass" 
    ssh_normal_usage(hostname, username, password)

    simulation_id = os.environ.get('SIMULATION_ID', 'unknown')
    with open(f'/signals/user_done_{simulation_id}', 'w') as f:
        f.write('done')
