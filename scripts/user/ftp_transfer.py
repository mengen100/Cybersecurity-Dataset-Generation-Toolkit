import ftplib
import time
import random
import os

def ftp_transfer(host, user, password):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to FTP server (attempt {attempt + 1})")
            ftp = ftplib.FTP(host)
            ftp.login(user, password)
            print("Connected to FTP server")
            
            # Simulate file transfers
            for i in range(3):
                filename = f"file_{i}.txt"
                with open(filename, "w") as f:
                    f.write(f"This is file {i}")
                
                ftp.storbinary(f"STOR {filename}", open(filename, "rb"))
                print(f"Uploaded {filename}")
                
                time.sleep(random.uniform(1, 3))
            
            ftp.quit()
            break
        except Exception as e:
            print(f"Error: {str(e)}. Retrying in 5 seconds...")
            time.sleep(5)
    else:
        print("Failed to connect to FTP server after multiple attempts")

if __name__ == "__main__":
    host = os.environ.get('FTP_HOST', 'ftp_server')
    user = os.environ.get('FTP_USER', 'ftpuser')
    password = os.environ.get('FTP_PASSWORD', 'simulation_default_pass')
    ftp_transfer(host, user, password)
    
    simulation_id = os.environ.get('SIMULATION_ID', 'unknown')
    with open(f'/signals/user_done_{simulation_id}', 'w') as f:
        f.write('done')