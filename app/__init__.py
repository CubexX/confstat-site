# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from flask import Flask
from flask_orator import Orator
from werkzeug.contrib.fixers import ProxyFix
import json

with open('config.json', 'r') as file:
    CONFIG = json.loads(file.read())

app = Flask(__name__, static_folder='../static')
app.config['ORATOR_DATABASES'] = {
    'mysql': {
        'driver': CONFIG['db']['driver'],
        'host': CONFIG['db']['host'],
        'database': CONFIG['db']['database'],
        'user': CONFIG['db']['user'],
        'password': CONFIG['db']['password']
    }
}
app.wsgi_app = ProxyFix(app.wsgi_app)

db = Orator(app)

from app.views import index, group, user

if __name__ == '__main__':
    app.run()
