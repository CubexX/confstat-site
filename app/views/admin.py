# -*- coding: utf-8 -*-
__author__ = 'CubexX'


import hashlib
import json
from datetime import datetime

from flask import redirect, render_template, request, session

from app import CONFIG, app, cache
from app.models import Chat, ChatStat, Entity, User, UserStat


def login_required(func):
    def wrapper(*args, **kwargs):
        if not session or session['hash'] != generate_hash(CONFIG['password']):
            return redirect('/admin/login')
        else:
            return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/admin')
@app.route('/admin/')
@login_required
def admin():
    today_chats = cache.get('today_chats')
    today_messages = cache.get('today_messages')

    last_chats = ChatStat.order_by('last_time', 'desc').limit(9).get()

    stats = {'all_users': User.count(),
             'today_users': User.get_today(),
             'all_chats': Chat.count(),
             'today_chats': today_chats if today_chats else 0,
             'all_messages': sum(u.msg_count for u in UserStat.all()),
             'today_messages': today_messages if today_messages else 0,
             'last_chats': last_chats}

    return render_template('admin/index.html',
                           stats=stats,
                           entities=Entity.generate_list()[0],
                           Chat=Chat,
                           format_time=format_time,
                           logs=get_logs())


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['hash'] = generate_hash(request.form['password'])

        if session['hash'] == generate_hash(CONFIG['password']):
            return redirect('/admin')
        else:
            return redirect('/admin/login')
    return render_template('admin/login.html')


@app.route('/admin/exit')
def exit_admin():
    session.pop('hash', None)
    return redirect('/')


@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def settings():
    with open('config.json', 'r') as jsonFile:
        data = json.load(jsonFile)

    if request.method == 'POST':
        form = request.form

        if form['db_driver']:
            data['db']['driver'] = form['db_driver']

        if form['db_host']:
            data['db']['host'] = form['db_host']

        if form['db_database']:
            data['db']['database'] = form['db_database']

        if form['db_user']:
            data['db']['user'] = form['db_user']

        if form['db_password']:
            data['db']['password'] = form['db_password']

        if form['cache_server']:
            data['cache']['servers'][0] = form['cache_server']

        if form['cache_debug']:
            data['cache']['debug'] = bool(int(form['cache_debug']))

        if form['admin_password']:
            data['password'] = form['admin_password']

        if form['salt']:
            data['salt'] = form['salt']

        with open("config.json", "w") as jsonFile:
            json.dump(data, jsonFile)

    return render_template('admin/settings.html',
                           data=data,
                           logs=get_logs())


def format_time(ts):
    return datetime.fromtimestamp(ts).strftime('%H:%M, %d.%m.%y')


def generate_hash(text):
    text = str(text).encode('utf-8')
    salt = str(CONFIG['salt']).encode('utf-8')

    return hashlib.md5(text + salt).hexdigest()


def get_logs():
    with open('../confstat-bot/bot.log', 'r') as log:
        log = log.read()
        log_list = [line.split(' - ') for line in reversed(log.split('\n')) if "Timed out" not in line]

        return log_list[:10]
