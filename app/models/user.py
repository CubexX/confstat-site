# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import db


class User(db.Model):
    __table__ = 'users'
    __fillable__ = ['uid', 'username', 'fullname']
