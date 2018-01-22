# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from flask import render_template

from app import app, cache
from app.models import Chat, ChatStat, User


@app.route('/')
def index():
    stats = cache.get('web_stats')
    msgs = 0

    # TODO: fix this by raw sql
    for c in Chat.all():
        res = ChatStat.where('cid', c.cid).order_by('id', 'desc').limit(1).first()
        msgs += res.msg_count

    if not stats:
        stats = {
            'users_count': User.all().count(),
            'chats_count': Chat.all().count(),
            'messages_count': msgs
        }
        cache.set('web_stats', stats, 300)

    return render_template('index.html',
                           page_title='Confstat',
                           users_count=stats['users_count'],
                           chats_count=stats['chats_count'],
                           messgaes_count=stats['messages_count'])
