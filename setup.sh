#!/bin/bash

# Change to the script's directory
cd "$(dirname "$0")"

# Check if Docker is installed and install it if it's not
if ! command -v docker &> /dev/null; then
    echo "Docker could not be found, installing Docker..."
    curl -sSL https://get.docker.com/ | sh
else
    echo "Docker is already installed."
fi

# Ensure the Docker service is started
if ! systemctl is-active --quiet docker; then
    echo "Starting Docker service..."
    systemctl start docker
else
    echo "Docker service is already running."
fi

# Check for docker-compose and install it if necessary
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    echo "Docker Compose is already installed."
fi


# Change to the script's directory
cd "$(dirname "$0")"

# # Build the kali-attacker image
# echo "Building kali-attacker Docker image..."
# docker build -t kali-attacker docker/attacks/

# # Build the scapy-benign-traffic image
# echo "Building scapy-benign-traffic/ Docker image..."
# docker build -t scapy-benign-traffic docker/scapy-benign-traffic/


docker build -t attacker:latest scripts/attacker/
docker build -t user:latest scripts/user/
docker build -t ftp_server:latest scripts/ftp_server/
docker build -t ssh_server:latest scripts/ssh_server/
docker build -t web_app:latest scripts/web_app/
docker build -t firewall:latest scripts/firewall/

# # Build the ostinato image
# echo "Building ostinato-client Docker image..."
# docker build -t ostinato-client docker/ostinato/

# Return to the original directory
cd -

echo "Setup completed!"


