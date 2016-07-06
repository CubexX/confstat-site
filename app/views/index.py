# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html', page_title='Confstat')
