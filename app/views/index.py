# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import app
from app.models import User, Chat, ChatStat
from flask import render_template
from datetime import datetime


@app.route('/')
def index():
    users_count = User.all().count()
    chats_count = Chat.all().count()
    messages_count = 0

    t = datetime.today()
    today_ts = datetime(t.year, t.month, t.day, hour=00).timestamp()

    for chat in ChatStat.where('last_time', '>', today_ts).get().all():
        messages_count += chat.msg_count

    return render_template('index.html',
                           page_title='Confstat',
                           users_count=users_count,
                           chats_count=chats_count,
                           messgaes_count=messages_count)
