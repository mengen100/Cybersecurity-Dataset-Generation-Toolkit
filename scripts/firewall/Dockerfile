FROM ubuntu:latest

RUN apt-get update && apt-get install -y iptables nginx openssh-client tcpdump curl iputils-ping

COPY firewall_config/iptables.rules /etc/iptables.rules
COPY firewall_config/nginx.conf /etc/nginx/nginx.conf

RUN chmod +x /etc/iptables.rules

# Enable IP forwarding in the image
RUN echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

CMD ["bash", "-c", "iptables-restore < /etc/iptables.rules && sysctl -p && nginx -g 'daemon off;'"]