# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import db


class UserStat(db.Model):
    __table__ = 'user_stats'
    __fillable__ = ['uid', 'cid', 'msg_count', 'last_activity']
