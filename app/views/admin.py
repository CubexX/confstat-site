# -*- coding: utf-8 -*-
__author__ = 'CubexX'


from datetime import datetime

from Crypto.Hash import MD5
from flask import redirect, render_template, request, session

from app import CONFIG, app, cache
from app.models import Chat, ChatStat, Entity, User, UserStat


@app.route('/admin')
@app.route('/admin/')
def admin():
    if not session or session['hash'] != generate_hash(CONFIG['password']):
        return redirect('/admin/login')

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
                           format_time=format_time)


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


def format_time(ts):
    t = datetime.fromtimestamp(ts).strftime('%H:%M, %d.%m.%y')
    return t


def generate_hash(text):
    salt = str(CONFIG['salt']).encode('utf-8')
    text = str(text).encode('utf-8')

    h = MD5.new(text)
    h.update(salt)

    return h.hexdigest()
