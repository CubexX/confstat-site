# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from datetime import datetime

from app import db


class Message(db.Model):
    __table__ = 'messages'
    __timestamps__ = False
    __fillable__ = ['uid', 'cid', 'date']

    @staticmethod
    def today_chat_count(cid):
        t = datetime.today()
        today = int(datetime(t.year, t.month, t.day, 0).timestamp())

        return db.select('SELECT COUNT(*) AS count FROM messages'
                         ' WHERE cid = {} AND date >= {}'.format(cid, today))[0]['count']

    @staticmethod
    def today_all_count():
        t = datetime.today()
        today = int(datetime(t.year, t.month, t.day, 0).timestamp())

        return db.select('SELECT COUNT(*) AS count FROM messages'
                         ' WHERE date >= {}'.format(today))[0]['count']

    @staticmethod
    def count_in_chat(cid):
        return db.select('SELECT COUNT(*) AS count FROM messages'
                         ' WHERE cid = {}'.format(cid))[0]['count']
