# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from datetime import datetime

from app import cache, db


class User(db.Model):
    __table__ = 'users'
    __timestamps__ = False
    __fillable__ = ['uid', 'username', 'fullname', 'public']

    @staticmethod
    def get(uid):
        cached = cache.get('web_user_{}'.format(uid))

        if cached:
            return cached
        else:
            user = User.where('uid', uid).get()[0]
            if user:
                cache.set('web_user_{}'.format(uid), user)
                return user
            else:
                return False

    """ ADMIN PANEL """

    # Today active users at all
    @staticmethod
    def today_all_active_users():
        t = datetime.today()
        today = int(datetime(t.year, t.month, t.day, 0).timestamp())

        return len(db.select('SELECT DISTINCT uid FROM messages '
                             'WHERE date >= {}'.format(today)))

    """ /ADMIN PANEL """
