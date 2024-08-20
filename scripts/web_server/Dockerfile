FROM python:3.9
RUN pip install flask mysql-connector-python
WORKDIR /app
COPY app.py /app/
CMD ["python", "app.py"]