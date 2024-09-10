#!/bin/bash

# Wait for MySQL to be ready
while ! mysqladmin ping -h"db" --silent; do
    sleep 1
done

# Initialize the database
mysql -h db -u root -ppassword < /docker-entrypoint-initdb.d/init.sql

# Start Apache
apache2-foreground