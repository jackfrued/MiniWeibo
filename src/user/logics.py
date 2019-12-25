import os
from functools import wraps

from flask import session
from flask import redirect
from flask import render_template


def save_avatar(nickname, avatar_file):
    '''保存用户头像'''
    base_dir = os.path.dirname(os.path.abspath(__name__))
    file_path = os.path.join(base_dir, 'static', 'upload', nickname)
    avatar_file.save(file_path)


def login_required(view_func):
    '''登陆验证装饰器'''
    @wraps(view_func)
    def check(*args, **kwargs):
        if 'uid' in session:
            return view_func(*args, **kwargs)
        else:
            return render_template('login.html', error='请您先登录')
    return check
