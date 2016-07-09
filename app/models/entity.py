# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import db


class Entity(db.Model):
    __table__ = 'entities'
    __timestamps__ = False
    __fillable__ = ['cid', 'type', 'title', 'count']
