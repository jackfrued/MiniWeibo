from flask import request
from flask import session
from flask import redirect
from flask import Blueprint
from flask import render_template

from .models import Weibo
from user.models import User
from libs.db import db
from user.logics import login_required

weibo_bp = Blueprint('weibo', import_name='weibo')
weibo_bp.template_folder = './templates'


@weibo_bp.route('/')
@weibo_bp.route('/index')
def index():
    '''显示全部微博'''
    return render_template('index.html')


@weibo_bp.route('/post', methods=('POST', 'GET'))
@login_required
def post():
    if request.method == 'POST':
        content = request.form.get('content').strip()
        if not content:
            return render_template('post.html', error='微博内容不允许为空！')
        else:
            weibo = Weibo(uid=session['uid'], content=content)
            db.session.add(weibo)
            db.session.commit()
            return redirect('/weibo/show?wid=%s' % weibo.id)
    else:
        return render_template('post.html')


@weibo_bp.route('/edit')
def edit():
    return render_template('edit.html')


@weibo_bp.route('/show')
def show():
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    user = User.query.get(weibo.uid)
    return render_template('show.html', weibo=weibo, user=user)


@weibo_bp.route('/delete')
def delete():
    return render_template('delete.html')
