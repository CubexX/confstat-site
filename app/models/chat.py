# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import db, cache


class Chat(db.Model):
    __table__ = 'chats'
    __timestamps__ = False
    __fillable__ = ['cid', 'title']

    @staticmethod
    def get(cid):
        cached = cache.get('chat_{}'.format(cid))

        if cached:
            return cached
        else:
            chat = Chat.where('cid', cid).get()[0]
            if chat:
                cache.set('chat_{}'.format(cid), chat)
                return chat
            else:
                return False
