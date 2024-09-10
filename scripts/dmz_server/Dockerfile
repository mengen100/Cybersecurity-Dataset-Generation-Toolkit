FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    openssh-server \
    nmap \
    netcat-traditional \
    iproute2 \
    net-tools \
    sshpass \
    python3-venv \
    iputils-ping

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate virtual environment and install packages
RUN /opt/venv/bin/pip install --upgrade pip && /opt/venv/bin/pip install flask

# Set the virtual environment to be activated when the container starts
ENV PATH="/opt/venv/bin:$PATH"

COPY app.py /app/app.py

COPY config_files /etc/config_files

# Set up SSH
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Create a user with sudo privileges
RUN useradd -m dmzuser && echo "dmzuser:dmzpassword" | chpasswd
RUN usermod -aG sudo dmzuser


# Copy and set permissions for start_services.sh
COPY start_services.sh /start_services.sh
RUN chmod +x /start_services.sh

# Ensure the file has Unix-style line endings
RUN sed -i 's/\r$//' /start_services.sh

EXPOSE 80 22
ENTRYPOINT ["/bin/bash", "/start_services.sh"]
