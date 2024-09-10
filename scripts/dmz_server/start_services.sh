#!/bin/bash
service ssh start
ip route add 172.16.240.0/24 via 172.16.239.2
python3 /app/app.py
