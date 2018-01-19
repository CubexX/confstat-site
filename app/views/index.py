# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import app, cache
from app.models import User, Chat, ChatStat
from flask import render_template


@app.route('/')
def index():
    stats = cache.get('web_stats')

    if not stats:
        stats = {
            'users_count': User.all().count(),
            'chats_count': Chat.all().count(),
            'messages_count': sum(chat.msg_count for chat in ChatStat.all())
        }
        cache.set('web_stats', stats, 300)

    return render_template('index.html',
                           page_title='Confstat',
                           users_count=stats['users_count'],
                           chats_count=stats['chats_count'],
                           messgaes_count=stats['messages_count'])
