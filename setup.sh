#!/bin/bash

# Change to the script's directory
cd "$(dirname "$0")"

# Check if curl is installed and install it if it's not
if ! command -v curl &> /dev/null; then
    echo "curl could not be found, installing curl..."
    sudo apt-get update && sudo apt-get install -y curl
fi

# Check if Docker is installed and install it if it's not
if ! command -v docker &> /dev/null; then
    echo "Docker could not be found, installing Docker..."
    curl -sSL https://get.docker.com/ | sh
else
    echo "Docker is already installed."
fi

# Add the current user to the docker group if not already added
if ! groups $USER | grep -q '\bdocker\b'; then
    echo "Adding user to docker group..."
    sudo usermod -aG docker $USER
    echo "Please log out and log back in so that group changes take effect."
    exit 1
fi

# Ensure the Docker service is started
if ! sudo systemctl is-active --quiet docker; then
    echo "Starting Docker service..."
    sudo systemctl start docker
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

# Check if Python is installed and install it if it's not
if ! command -v python3 &> /dev/null; then
    echo "Python3 could not be found, installing Python3..."
    sudo apt-get update && sudo apt-get install -y python3 python3-pip
else
    echo "Python3 is already installed."
fi

# Check if pip3 is installed and install it if it's not
if ! command -v pip3 &> /dev/null; then
    echo "pip3 could not be found, installing pip3..."
    sudo apt-get install -y python3-pip
fi

# Check if Flask is installed and install it if it's not
if ! python3 -c 'import flask' &> /dev/null; then
    echo "Flask could not be found, installing Flask..."
    sudo pip3 install Flask flask-socketio
else
    echo "Flask is already installed."
fi

# Build Docker images with sudo
sudo docker build -t attacker:latest scripts/attacker/
sudo docker build -t user:latest scripts/user/
sudo docker build -t ftp_server:latest scripts/ftp_server/
sudo docker build -t ssh_server:latest scripts/ssh_server/
sudo docker build -t web_server:latest scripts/web_server/
sudo docker build -t firewall:latest scripts/firewall/

# Return to the original directory
cd -

echo "Setup completed!"
