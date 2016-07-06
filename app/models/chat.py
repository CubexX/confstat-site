# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import db


class Chat(db.Model):
    __table__ = 'chats'
    __fillable__ = ['cid', 'title']
