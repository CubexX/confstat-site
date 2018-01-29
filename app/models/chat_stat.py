# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import db


class ChatStat(db.Model):
    __table__ = 'chat_stats'
    __timestamps__ = False
    __fillable__ = ['cid', 'users_count', 'msg_count', 'last_time']
