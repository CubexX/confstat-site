# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from datetime import datetime

from app import cache, db

from .message import Message


class Chat(db.Model):
    __table__ = 'chats'
    __timestamps__ = False
    __fillable__ = ['cid', 'title', 'public_link', 'add_time', 'hash']

    @staticmethod
    def get(cid):
        cached = cache.get('web_chat_{}'.format(cid))

        if cached:
            return cached
        else:
            chat = Chat.where('cid', cid).get()[0]
            if chat:
                cache.set('web_chat_{}'.format(cid), chat)
                return chat
            else:
                return False

    # All users in chat
    @staticmethod
    def all_chat_users(cid):
        return len(db.select('SELECT DISTINCT uid FROM messages WHERE cid = {}'.format(cid)))

    # Today active users in chat
    @staticmethod
    def today_chat_users(cid):
        t = datetime.today()
        today = int(datetime(t.year, t.month, t.day, 0).timestamp())

        return len(db.select('SELECT DISTINCT uid FROM messages '
                             'WHERE cid = {} AND date >= {}'.format(cid, today)))

    @staticmethod
    def today_new_count():
        t = datetime.today()
        today = int(datetime(t.year, t.month, t.day, 0).timestamp())

        return db.select('SELECT COUNT(*) AS count FROM chats'
                         ' WHERE add_time >= {}'.format(today))[0]['count']

    @staticmethod
    def last_chats_list():
        chats = []

        _chats = db.select('SELECT DISTINCT cid FROM messages ORDER BY id DESC LIMIT 9')
        for chat in _chats:
            current = Chat.get(int(chat['cid']))
            last_date = db.select('SELECT date FROM messages WHERE cid = {} '
                                  'ORDER BY id DESC LIMIT 1'.format(current.cid))[0]['date']

            chats.append(
                {
                    'hash': current.hash,
                    'title': current.title,
                    'msg_count': Message.count_in_chat(current.cid),
                    'last_date': last_date
                }
            )

        return chats
