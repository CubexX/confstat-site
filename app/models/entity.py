# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import db


class Entity(db.Model):
    __table__ = 'entities'
    __fillable__ = ['cid', 'type', 'title', 'count']
