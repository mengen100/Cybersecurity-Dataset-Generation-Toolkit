FROM python:3.9
RUN pip install flask mysql-connector-python
RUN apt-get update && apt-get install -y default-mysql-client netcat-traditional iputils-ping dnsutils
WORKDIR /app
COPY app.py /app/
CMD ["python", "app.py"]