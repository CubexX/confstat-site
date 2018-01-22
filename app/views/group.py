# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from datetime import datetime

from flask import redirect, render_template

from app import app, db
from app.models import Chat, Entity, User, UserStat


@app.route('/group/<chat_hash>')
def group(chat_hash):
    # Get chat statistics
    chat_stats = db.select('(SELECT * FROM chat_stats '
                           'WHERE hash =  "{}" '
                           'ORDER BY id DESC LIMIT 21) '
                           'ORDER BY id ASC'.format(chat_hash))

    if chat_stats:
        # Chat
        cid = chat_stats[0].cid
        chat = Chat.get(cid)

        # Chat title
        chat_title = chat.title

        # Bot add date, dd.mm.yy
        add_date = datetime.fromtimestamp(chat.add_time).strftime('%d.%m.%y')

        # Today messages
        msg_count = chat_stats[-1].msg_count

        # All number of users
        all_users = UserStat.where('cid', cid).count()

        # Today active users
        active_users = chat_stats[-1].users_count

        # Last update
        last_update = datetime.fromtimestamp(chat_stats[-1].last_time).strftime('%d.%m.%y (%H:%M)')

        # Link for public chats
        public_link = chat.public_link

        average_users = 0
        chart = {'labels': [], 'msg_values': [], 'users_values': []}

        # Charts generator
        i = 0
        for chat in chat_stats:
            average_users += chat.users_count

            # Dates, dd/mm
            d = datetime.fromtimestamp(chat.last_time).strftime('%d')

            chart['labels'].append(str(d))
            chart['msg_values'].append(chat.msg_count)
            chart['users_values'].append(chat.users_count)

            i += 1

        # Average number of users
        average_users = round(average_users / i)

        # Generating user list
        users = []
        user_stats = UserStat.where('cid', cid).order_by('msg_count', 'desc').limit(50).get().all()
        for ustat in user_stats:
            user = User.get(ustat.uid)
            users.append({'name': user.fullname,
                          'msg_count': ustat.msg_count,
                          'uid': ustat.uid,
                          'public': user.public})

        # Generating entities
        entities = {'total': 0,
                    'photo': 0,
                    'audio': 0,
                    'video': 0,
                    'document': 0,
                    'url': 0,
                    'hashtag': 0,
                    'bot_command': 0,
                    'mention': 0}
        urls = []
        i = 0
        _entities = Entity.where('cid', cid).order_by('count', 'desc').get().all()
        for entity in _entities:
            if entity.type == 'voice':
                entities['audio'] += entity.count
            else:
                entities[entity.type] += entity.count
            entities['total'] += entity.count

            # Generating urls list
            if entity.type == 'url' and i < 9:
                urls.append({'link': entity.title,
                             'count': entity.count})
                i += 1

        return render_template('group.html',
                               page_title='{} - Confstat'.format(chat_title),
                               chat_title=chat_title,
                               add_date=add_date,
                               msg_count=msg_count,
                               all_users=all_users,
                               active_users=active_users,
                               average_users=average_users,
                               chart=chart,
                               users=users,
                               entities=entities,
                               urls=urls,
                               last_update=last_update,
                               public_link=public_link)

    else:
        return redirect('/')
