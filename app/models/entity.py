# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from app import db


class Entity(db.Model):
    __table__ = 'entities'
    __timestamps__ = False
    __fillable__ = ['cid', 'type', 'title', 'count']

    @staticmethod
    def generate_list(cid=None):
        # Generating entities
        entities = {'total': 0,
                    'photo': 0,
                    'audio': 0,
                    'video': 0,
                    'document': 0,
                    'url': 0,
                    'hashtag': 0,
                    'bot_command': 0,
                    'mention': 0}
        urls = []
        i = 0

        if cid is None:
            _entities = Entity.all()
        else:
            _entities = Entity.where('cid', cid).order_by('count', 'desc').get().all()

        for entity in _entities:
            if entity.type == 'voice':
                entities['audio'] += entity.count
            else:
                entities[entity.type] += entity.count
            entities['total'] += entity.count

            # Generating urls list
            if entity.type == 'url' and i < 9:
                urls.append({'link': entity.title,
                             'count': entity.count})
                i += 1

        return entities, urls
