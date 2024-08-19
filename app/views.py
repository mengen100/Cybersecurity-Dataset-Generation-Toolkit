import os
import subprocess
from flask import render_template, request, jsonify
from app import app
import yaml


current_script_path = os.path.dirname(os.path.abspath(__file__))

NEW_TEST_PATH = os.path.join(current_script_path, '../new_test')

VULHUB_BASE_PATH = os.path.join(current_script_path, '../docker/vulhub-master')
SCAPY_BASE_PATH = os.path.join(current_script_path, '../docker/scapy-benign-traffic')
DOCKER_COMPOSE_PATH = os.path.join(current_script_path, '../docker/vulhub-master/php/8.1-backdoor/docker-compose.yml')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCKER_COMPOSE_DIR = os.path.join(BASE_DIR, '../docker_compose_files')


# Scenario definitions
SCENARIOS = {
    1: [
        {
            "id": "file_transfer_bruteforce",
            "name": "FTP File Transfer and Brute Force Attack",
            "description": "Simulates a file transfer server and a brute force attack attempt.",
            "topology": {
                "attacker": {"image": "attacker:latest", "ports": []},
                "user": {"image": "user:latest", "ports": []},
                "public_server": {"image": "ftp_server:latest", "ports": ["21:21"]}
            },
            "traffic": {
                "benign": ["ftp_transfer"],
                "malicious": ["ftp_bruteforce"]
            }
        },

        {
            "id": "ssh_login_bruteforce",
            "name": "SSH Normal Usage and Brute Force Attack",
            "description": "Simulates a normal SSH login usage and a brute force attack attempt.",
            "topology": {
                "attacker": {"image": "attacker:latest", "ports": []},
                "user": {"image": "user:latest", "ports": []},
                "public_server": {"image": "ssh_server:latest", "ports": ["22:22"]}
            },
            "traffic": {
                "benign": ["ssh_transfer"],
                "malicious": ["ssh_bruteforce"]
            }
        }
    ],
    2: [
        {
            "id": "web_app_sql_injection",
            "name": "Web Application with SQL Injection",
            "description": "Simulates a web application behind a firewall, targeted by SQL injection.",
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
            }
        }
    ]
    # Add more levels and scenarios as needed
}

@app.route('/')
def index():
    return render_template('index.html')

def generate_password(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/get_scenarios', methods=['GET'])
def get_scenarios():
    level = int(request.args.get('level', 1))
    return jsonify(SCENARIOS.get(level, []))



# @app.route('/configure_network', methods=['POST'])
# def configure_network():
#     level = int(request.form['sophistication_level'])
#     scenario_id = request.form['scenario_id']
    
#     scenario = next((s for s in SCENARIOS[level] if s['id'] == scenario_id), None)
#     if not scenario:
#         return jsonify({"error": "Invalid scenario"}), 400

#     docker_compose = generate_docker_compose(scenario)
    
#     file_path = os.path.join(DOCKER_COMPOSE_DIR, f"{scenario_id}.yml")
#     with open(file_path, 'w') as f:
#         f.write(docker_compose)

#     traffic_dir = os.path.join(BASE_DIR, '../traffic')
#     os.makedirs(traffic_dir, exist_ok=True)

#     return jsonify({"message": "Network configured successfully", "file": file_path})


# def generate_docker_compose(scenario):
#     config = {
#         'version': '3',
#         'services': {},
#         'networks': {
#             'simulation_network': {'driver': 'bridge'}
#         }
#     }

#     for node, details in scenario['topology'].items():
#         config['services'][node] = {
#             'image': details['image'],
#             'networks': ['simulation_network'],
#             'volumes': [
#                 '../scripts:/scripts', 
#                 '../traffic:/traffic'
#             ]
#         }
#         if details['ports']:
#             config['services'][node]['ports'] = details['ports']

#     return yaml.dump(config, default_flow_style=False)


# @app.route('/build_images', methods=['POST'])
# def build_images():
#     try:
#         # Change to the VULHUB_BASE_PATH directory
#         os.chdir(NEW_TEST_PATH)

#         # Build the Docker images
#         subprocess.run(["docker-compose", "build"], check=True)
#         # not working yet
#         return jsonify({
#             "message": "Docker images built successfully",
#         }), 200
#     except subprocess.CalledProcessError as e:
#         return jsonify({
#             "error": "Failed to build Docker images",
#             "details": str(e)
#         }), 500
#     except Exception as e:
#         return jsonify({
#             "error": "An unexpected error occurred",
#             "details": str(e)
#         }), 500

# def generate_docker_compose(scenario):
#     config = {
#         'version': '3',
#         'services': {},
#         'networks': {
#             'simulation_network': {'driver': 'bridge'}
#         }
#     }

#     for node, details in scenario['topology'].items():
#         config['services'][node] = {
#             'image': details['image'],
#             'networks': ['simulation_network'],
#             'volumes': [
#                 './scripts:/scripts'
#             ]
#         }
#         if details['ports']:
#             config['services'][node]['ports'] = details['ports']

#     return yaml.dump(config, default_flow_style=False)

# def generate_docker_compose(sophistication_level, malicious_traffic, benign_traffic):
#     network_config = {
#         'version': '3',
#         'services': {},
#         'networks': {}
#     }

#     # Common services
#     network_config['services']['attacker'] = {
#         'build': './attacker',
#         'image': 'attacker_image:latest',
#         'networks': ['internet'],
#         'volumes': [
#             './malicious_traffic:/malicious_traffic',
#             './traffic_scripts:/traffic_scripts'
#         ],
#         'environment': [
#             f"MALICIOUS_TRAFFIC={','.join(malicious_traffic)}",
#             "TARGET_HOST=public_server"
#         ],
#         'cap_add': ['NET_ADMIN', 'NET_RAW'],
#         'command': 'python3 /traffic_scripts/generate_malicious_traffic.py'
#     }
#     network_config['services']['user'] = {
#         'build': './user',
#         'image': 'user_image:latest',
#         'networks': ['internet'],
#         'volumes': [
#             './benign_traffic:/benign_traffic',
#             './traffic_scripts:/traffic_scripts'
#         ],
#         'environment': [
#             f"BENIGN_TRAFFIC={','.join(benign_traffic)}",
#             "TARGET_HOST=public_server"
#         ],
#         'cap_add': ['NET_ADMIN', 'NET_RAW'],
#         'command': 'python3 /traffic_scripts/generate_benign_traffic.py'
#     }


#     # Add networks
#     network_config['networks']['internet'] = None

#     if sophistication_level >= 1:
#         network_config['services']['public_server'] = {
#             'image': 'nginx:latest',
#             'networks': ['internet']
#         }

#     if sophistication_level >= 2:
#         network_config['services']['firewall'] = {
#             'image': 'alpine:latest',
#             'networks': ['internet', 'internal']
#         }
#         network_config['networks']['internal'] = None
#         network_config['services']['public_server']['networks'] = ['internal']

#     if sophistication_level >= 3:
#         network_config['services']['dmz_switch'] = {
#             'image': 'alpine:latest',
#             'networks': ['dmz']
#         }
#         network_config['services']['internal_switch'] = {
#             'image': 'alpine:latest',
#             'networks': ['internal']
#         }
#         network_config['services']['internal_desktop'] = {
#             'image': 'ubuntu:latest',
#             'networks': ['internal']
#         }
#         network_config['services']['internal_server'] = {
#             'image': 'ubuntu:latest',
#             'networks': ['internal']
#         }
#         network_config['networks']['dmz'] = None

#     if sophistication_level >= 4:
#         network_config['services']['subnet1'] = {
#             'image': 'alpine:latest',
#             'networks': ['internal']
#         }
#         network_config['services']['subnet2'] = {
#             'image': 'alpine:latest',
#             'networks': ['internal']
#         }
#         network_config['services']['internal_desktop_2'] = {
#             'image': 'ubuntu:latest',
#             'networks': ['internal']
#         }
#         network_config['services']['internal_server_2'] = {
#             'image': 'ubuntu:latest',
#             'networks': ['internal']
#         }

#     # Add environment variables for traffic types
#     network_config['services']['attacker']['environment'] = [f"MALICIOUS_TRAFFIC={','.join(malicious_traffic)}"]
#     network_config['services']['user']['environment'] = [f"BENIGN_TRAFFIC={','.join(benign_traffic)}"]

#     return yaml.dump(network_config, default_flow_style=False)

# @app.route('/configure_network', methods=['POST'])
# def configure_network():
#     try:
#         sophistication_level = int(request.form['sophistication_level'])
#         malicious_traffic = request.form.getlist('malicious_traffic')
#         benign_traffic = request.form.getlist('benign_traffic')

#         docker_compose_content = generate_docker_compose(sophistication_level, malicious_traffic, benign_traffic)

#         os.makedirs(NEW_TEST_PATH, exist_ok=True)
#         file_path = os.path.join(NEW_TEST_PATH, 'docker-compose.yml')

#         with open(file_path, 'w') as file:
#             file.write(docker_compose_content)

#         # Create directories for traffic capture and scripts
#         os.makedirs(os.path.join(NEW_TEST_PATH, 'malicious_traffic'), exist_ok=True)
#         os.makedirs(os.path.join(NEW_TEST_PATH, 'benign_traffic'), exist_ok=True)
#         os.makedirs(os.path.join(NEW_TEST_PATH, 'traffic_scripts'), exist_ok=True)
#         os.makedirs(os.path.join(NEW_TEST_PATH, 'attacker'), exist_ok=True)
#         os.makedirs(os.path.join(NEW_TEST_PATH, 'user'), exist_ok=True)

#         return jsonify({
#             "message": "Docker Compose file generated successfully",
#             "file_path": file_path
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "error": "Failed to generate Docker Compose file",
#             "details": str(e)
#         }), 500


@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    scenario_id = request.form['scenario_id']
    file_path = os.path.join(DOCKER_COMPOSE_DIR, f"{scenario_id}.yml")

    traffic_dir = os.path.join(BASE_DIR, '../traffic')
    os.makedirs(traffic_dir, exist_ok=True)
    
    try:
        subprocess.run(["docker-compose", "-f", file_path, "up", "-d"], check=True)
        return jsonify({"message": "Simulation started successfully"})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stop_simulation', methods=['POST'])
def stop_simulation():
    scenario_id = request.form['scenario_id']
    file_path = os.path.join(DOCKER_COMPOSE_DIR, f"{scenario_id}.yml")
    
    try:
        subprocess.run(["docker-compose", "-f", file_path, "down"], check=True)
        return jsonify({"message": "Simulation stopped successfully"})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500


