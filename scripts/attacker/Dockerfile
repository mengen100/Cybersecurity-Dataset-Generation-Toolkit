FROM kalilinux/kali-rolling
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv tcpdump openssh-client nmap dnsutils curl iputils-ping

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate virtual environment and install packages
RUN /opt/venv/bin/pip install --upgrade pip && /opt/venv/bin/pip install paramiko requests python-nmap

# Set the virtual environment to be activated when the container starts
ENV PATH="/opt/venv/bin:$PATH"

COPY . /scripts
CMD ["tail", "-f", "/dev/null"]
