from flask import Flask
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['TRAFFIC_DIR'] = os.path.join(basedir, '../traffic')

from app import views