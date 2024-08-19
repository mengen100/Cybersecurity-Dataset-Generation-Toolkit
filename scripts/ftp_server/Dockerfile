FROM ubuntu:latest

RUN apt-get update && apt-get install -y vsftpd

# Install utilities
RUN apt-get install -y tcpdump

# Create a user for FTP
RUN useradd -m ftpuser && echo "ftpuser:simulation_default_pass" | chpasswd

# Configure vsftpd
RUN echo "listen=YES" >> /etc/vsftpd.conf && \
	echo "listen_ipv6=NO" >> /etc/vsftpd.conf && \
    echo "local_enable=YES" >> /etc/vsftpd.conf && \
    echo "write_enable=YES" >> /etc/vsftpd.conf && \
    echo "chroot_local_user=YES" >> /etc/vsftpd.conf && \
    echo "allow_writeable_chroot=YES" >> /etc/vsftpd.conf && \
    echo "pasv_enable=YES" >> /etc/vsftpd.conf && \
    echo "pasv_min_port=30000" >> /etc/vsftpd.conf && \
    echo "pasv_max_port=30009" >> /etc/vsftpd.conf && \
    echo "userlist_enable=YES" >> /etc/vsftpd.conf && \
    echo "userlist_file=/etc/vsftpd.userlist" >> /etc/vsftpd.conf && \
    echo "userlist_deny=NO" >> /etc/vsftpd.conf && \
    echo "ftpuser" > /etc/vsftpd.userlist

# Create directory for FTP user
RUN mkdir -p /home/ftpuser/ftp && \
    chown nobody:nogroup /home/ftpuser/ftp && \
    chmod a-w /home/ftpuser/ftp && \
    mkdir /home/ftpuser/ftp/files && \
    chown ftpuser:ftpuser /home/ftpuser/ftp/files

EXPOSE 21 30000-30009

# Start vsftpd
CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]