import os
import time
import threading
import uuid
import subprocess
from flask import render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from app import app
import yaml


socketio = SocketIO(app, cors_allowed_origins="*")

simulation_status = {}
simulation_ids = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCKER_COMPOSE_DIR = os.path.join(BASE_DIR, '../docker_compose_files')
SIGNALS_DIR = os.path.join(BASE_DIR, '../signals')


# Scenario definitions
SCENARIOS = {
    1: [
        {
            "id": "file_transfer_bruteforce",
            "name": "1. FTP File Transfer and Brute Force Attack",
            "description": "Simulates normal FTP file transfers alongside a brute force attack attempt on the FTP server.",
            "topology": {
                "attacker": {"image": "attacker:latest", "ports": []},
                "user": {"image": "user:latest", "ports": []},
                "ftp_server": {"image": "ftp_server:latest", "ports": ["21:21"]}
            },
            "traffic": {
                "benign": ["ftp_transfer"],
                "malicious": ["ftp_bruteforce"]
            },
            "yaml_file": "file_transfer_bruteforce.yml",
            "image_url": "/static/images/L1FTP.png"
        },

        {
            "id": "ssh_login_bruteforce",
            "name": "2. SSH Normal Usage and Brute Force Attack",
            "description": "Simulates routine SSH commands and an SSH brute force attack attempt.",
            "topology": {
                "attacker": {"image": "attacker:latest", "ports": []},
                "user": {"image": "user:latest", "ports": []},
                "ssh_server": {"image": "ssh_server:latest", "ports": ["22:22"]}
            },
            "traffic": {
                "benign": ["ssh_transfer"],
                "malicious": ["ssh_bruteforce"]
            },
            "yaml_file": "ssh_login_bruteforce.yml",
            "image_url": "/static/images/L1SSH.png"
        }
    ],
    2: [
        {
            "id": "web_app_sql_injection",
            "name": "1. Web Application with SQL Injection",
            "description": "Combines normal web traffic with SQL injection attempts against a firewalled web application.",
            "topology": {
                "attacker": {"image": "attacker:latest", "ports": []},
                "user": {"image": "user:latest", "ports": []},
                "firewall": {"image": "firewall:latest", "ports": ["80:80"]},
                "web_server": {"image": "web_app:latest", "ports": ["80"]},
                "database": {"image": "mysql:latest", "ports": ["3306"]}
            },
            "traffic": {
                "benign": ["web_browsing", "database_queries"],
                "malicious": ["sql_injection"]
            },
            "yaml_file": "web_app_sql_injection.yml",
            "image_url": "/static/images/L2.png"
        },

        {
            "id": "dos_attack",
            "name": "2. Denial of Service Attack",
            "description": "Simulates regular web usage and a DoS attack targeting a firewalled web server.",
            "yaml_file": "web_app_dos_attack.yml",
            "image_url": "/static/images/L2.png"
        }
    ],
    3: [
        {
            "id": "multi_stage_attack",
            "name": "1. Multi-Stage Network Penetration",
            "description": "Simulates a complex attack involving port scanning, vulnerability exploitation, and lateral movement.",
            "yaml_file": "multi_stage_attack.yml",
            "image_url": "/static/images/L3.png"
        },
        {
            "id": "data_exfiltration",
            "name": "2. Data Exfiltration Scenario",
            "description": "Simulates data exfiltration attempts from both external attackers and insider threats.",
            "yaml_file": "data_exfiltration.yml",
            "image_url": "/static/images/L3.png"
        }
    ],
}

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
IMAGES_FOLDER = os.path.join(APP_ROOT, 'static', 'images')

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_FOLDER, filename)

@app.route('/')
def index():
    return render_template('index.html')

def generate_password(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/get_scenarios', methods=['GET'])
def get_scenarios():
    level = int(request.args.get('level', 1))
    return jsonify(SCENARIOS.get(level, []))

def clean_signal_files(SIGNALS_DIR):
    for f in os.listdir(SIGNALS_DIR):
        if f.startswith(('attacker_done_', 'user_done_')):  # Add other prefixes as needed
            os.remove(os.path.join(SIGNALS_DIR, f))

def check_simulation_complete(scenario_id, file_path, simulation_id):
    
    expected_signals = ['attacker_done', 'user_done']  # Add more as needed
    timeout = 600  # 10 minutes timeout, adjust as needed
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        completed_signals = [f for f in expected_signals if os.path.exists(os.path.join(SIGNALS_DIR, f"{f}_{simulation_id}"))]
        if len(completed_signals) == len(expected_signals):
            return True
        time.sleep(5)  # Check every 5 seconds
    
    return False

def run_simulation(scenario_id, file_path):
    simulation_id = simulation_ids[scenario_id]
    
    try:
        # Clean up any existing signal files before starting
        clean_signal_files(SIGNALS_DIR)
        
        # Start the simulation
        env = os.environ.copy()
        env['SIMULATION_ID'] = simulation_id
        subprocess.run(["docker-compose", "-f", file_path, "up", "-d"], env=env, check=True)
        
        # Wait for simulation to complete
        simulation_complete = check_simulation_complete(scenario_id, file_path, simulation_id)
        
        if simulation_complete:
            # Stop the simulation
            subprocess.run(["docker-compose", "-f", file_path, "down"], check=True)
            
            # Update status and notify frontend
            simulation_status[scenario_id] = "completed"
            socketio.emit('simulation_complete', {'scenario_id': scenario_id})
        else:
            raise Exception("Simulation timed out")
    except Exception as e:
        simulation_status[scenario_id] = "error"
        socketio.emit('simulation_error', {'scenario_id': scenario_id, 'error': str(e)})
    finally:
        # Ensure containers are stopped even if an error occurred
        subprocess.run(["docker-compose", "-f", file_path, "down"], check=True)
        
        # Clean up all signal files after the simulation
        clean_signal_files(SIGNALS_DIR)

@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    scenario_id = request.form['scenario_id']
    level = int(request.form['sophistication_level'])
    
    scenario = next((s for s in SCENARIOS[level] if s['id'] == scenario_id), None)
    if not scenario:
        return jsonify({"error": "Invalid scenario"}), 400
    
    yaml_file = scenario['yaml_file']
    file_path = os.path.join(DOCKER_COMPOSE_DIR, yaml_file)
    
    simulation_status[scenario_id] = "running"
    simulation_ids[scenario_id] = str(uuid.uuid4())
    
    # Start simulation in a separate thread
    thread = threading.Thread(target=run_simulation, args=(scenario_id, file_path))
    thread.start()
    
    return jsonify({"message": "Simulation started successfully. This may take a few moments to complete..."})

@app.route('/simulation_status', methods=['GET'])
def get_simulation_status():
    scenario_id = request.args.get('scenario_id')
    status = simulation_status.get(scenario_id, "not_found")
    return jsonify({"status": status})

if __name__ == '__main__':
    socketio.run(app, debug=True)


