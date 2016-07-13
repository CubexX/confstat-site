# -*- coding: utf-8 -*-
__author__ = 'CubexX'

from flask import render_template, redirect, request
from app.models import User, UserStat, Chat
from datetime import datetime
from app import app, cache


@app.route('/user/<uid>')
@app.route('/user/<uid>/<token>')
def user_view(uid, token=None):
    user = User.where('uid', uid).get().first()

    if user:
        if user.public or token == cache.get('user_token_{}'.format(uid)):
            # Get user statistics
            stats = UserStat.where('uid', uid).get().all()
            info = {'first_act': 0,
                    'last_act': 0,
                    'total_msg': 0,
                    'groups': []}
            if stats:
                for stat in stats:
                    info['total_msg'] += stat.msg_count

                    # Generating groups list
                    info['groups'].append({
                        'title': Chat.get(stat.cid).title,
                        'msg_count': stat.msg_count
                    })
                    # Get last activity timestamp
                    if info['last_act'] < stat.last_activity:
                        info['last_act'] = stat.last_activity

                # Generating date from timestamps
                info['first_act'] = datetime.fromtimestamp(stats[-1].last_activity).strftime('%d.%m.%y')
                info['last_act'] = datetime.fromtimestamp(info['last_act']).strftime('%d.%m.%y (%H:%M)')

            page_title = '{} - Confstat'.format(user.fullname)
        else:
            user = None
            info = None
            page_title = 'Confstat'

        return render_template('user.html',
                               page_title=page_title,
                               user=user,
                               info=info,
                               token=token)
    else:
        redirect('/')
