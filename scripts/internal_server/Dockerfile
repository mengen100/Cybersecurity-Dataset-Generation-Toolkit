FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    mysql-server

# Set up SSH
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Create a user with sudo privileges
RUN useradd -m internaladmin && echo "internaladmin:secretpass123" | chpasswd
RUN usermod -aG sudo internaladmin

RUN mkdir -p /home/internaladmin
RUN chown internaladmin:internaladmin /home/internaladmin

# Copy the custom MySQL configuration
COPY my.cnf /etc/mysql/mysql.conf.d/mysqld.cnf

# Initialize MySQL data directory
RUN mkdir -p /var/lib/mysql /var/run/mysqld \
    && chown -R mysql:mysql /var/lib/mysql /var/run/mysqld \
    && chmod 777 /var/run/mysqld

# Start MySQL, create user, and set permissions
RUN service mysql start && \
    mysql -e "CREATE USER 'root'@'%' IDENTIFIED BY 'password';" && \
    mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;" && \
    mysql -e "FLUSH PRIVILEGES;"

EXPOSE 22 3306

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]