# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import db, cache


class User(db.Model):
    __table__ = 'users'
    __timestamps__ = False
    __fillable__ = ['uid', 'username', 'fullname']

    @staticmethod
    def get(uid):
        cached = cache.get('user_{}'.format(uid))

        if cached:
            return cached
        else:
            user = User.where('uid', uid).get()[0]
            if user:
                cache.set('user_{}'.format(uid), user)
                return user
            else:
                return False
