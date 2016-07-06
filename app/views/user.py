# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import app
from flask import render_template


@app.route('/user/<uid>')
def user(uid):
    if uid:
        return render_template('user.html',
                               page_title='{} - Confstat'.format(uid),
                               uid=uid)
