FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo

# Set up SSH
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Create a user with sudo privileges
RUN useradd -m internaladmin && echo "internaladmin:secretpass123" | chpasswd
RUN usermod -aG sudo internaladmin

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]