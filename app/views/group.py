# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import app
from app.models import Chat, User, Entity, ChatStat, UserStat
from flask import render_template
from datetime import datetime


@app.route('/group/<chat_hash>')
def group(chat_hash):
    # Get chat statistics
    chat_stats = ChatStat.where('hash', chat_hash).limit(21).get()

    if chat_stats:
        # Chat id
        cid = chat_stats[0].cid
        # Chat title
        chat_title = Chat.where('cid', cid).get()[0].title
        # Bot add date, dd.mm.yy
        add_date = datetime.fromtimestamp(chat_stats[0].last_time).strftime('%d.%m.%y')
        # Today messages
        msg_count = chat_stats[-1].msg_count
        # Today active users
        active_users = chat_stats[-1].users_count

        average_users = 0
        chart = {'labels': [], 'msg_values': [], 'users_values': []}

        # Charts generator
        i = 0
        for chat in chat_stats:
            average_users += chat.users_count

            # Dates, dd/mm
            d = datetime.fromtimestamp(chat.last_time).strftime('%d/%m')

            chart['labels'].append(str(d))
            chart['msg_values'].append(chat.msg_count)
            chart['users_values'].append(chat.users_count)

            i += 1

        # Average number of users
        average_users = round(average_users / i, 1)

        # Generating user list
        users = []
        user_stats = UserStat.where('cid', cid).order_by('msg_count', 'desc').limit(50).get().all()
        for ustat in user_stats:
            users.append({'name': User.where('uid', ustat.uid).get()[0].fullname,
                          'msg_count': ustat.msg_count,
                          'uid': ustat.uid})

        # Generating entities
        entities = {'total': 0,
                    'photos': 0,
                    'audio': 0,
                    'videos': 0,
                    'files': 0,
                    'links': 0,
                    'hashtags': 0,
                    'commands': 0,
                    'mentions': 0}
        _entities = Entity.where('cid', cid).get().all()
        for entity in _entities:
            if entity.type == 'photo':
                entities['photos'] = entity.count

            if entity.type == 'audio' or entity.type == 'voice':
                entities['audio'] += entity.count

            if entity.type == 'video':
                entities['videos'] = entity.count

            if entity.type == 'document':
                entities['files'] = entity.count

            if entity.type == 'url':
                entities['links'] += entity.count

            if entity.type == 'hashtag':
                entities['hashtags'] += entity.count

            if entity.type == 'bot_command':
                entities['commands'] += entity.count

            if entity.type == 'mention':
                entities['mentions'] += entity.count

            entities['total'] += entity.count

        return render_template('group.html',
                               page_title='{} - Confstat'.format(chat_title),
                               chat_title=chat_title,
                               add_date=add_date,
                               msg_count=msg_count,
                               active_users=active_users,
                               average_users=average_users,
                               chart=chart,
                               users=users,
                               entities=entities)

    else:
        return '404'
