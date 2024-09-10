FROM php:7.4-apache

RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

RUN apt-get update && apt-get install -y default-mysql-client netcat-traditional iputils-ping iproute2

COPY ./web_app /var/www/html/
COPY init.sql /docker-entrypoint-initdb.d/

RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

RUN mkdir /var/www/html/uploads && \
    chown www-data:www-data /var/www/html/uploads && \
    chmod 777 /var/www/html/uploads

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]