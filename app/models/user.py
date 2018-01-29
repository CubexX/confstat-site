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

    @staticmethod
    def get_today():
        t = datetime.today()
        today = round(datetime(t.year, t.month, t.day, 0).timestamp())
        yesterday = round(datetime(t.year, t.month, t.day - 1, 0).timestamp())

        today_users = db.select('SELECT COUNT(*) AS count FROM '
                                '(SELECT DISTINCT cid FROM user_stats '
                                'WHERE last_activity > {} '
                                'AND last_activity < {}) '
                                'user_stats'.format(yesterday, today))

        return today_users[0]['count']
