'''
后端开发者在处理参数时的原则:
1. 后端不要依赖前端页面的检查
2. 前端传来的所有数据对后端来说都不可信
3. 所有的数据都必须做检查
4. 后端能自己获取的数据不要依赖前端
5. 接口的参数和返回值能少则少，不要一次传递太多数据
'''

import datetime
from math import ceil
from collections import OrderedDict

from flask import abort
from flask import request
from flask import session
from flask import redirect
from flask import Blueprint
from flask import render_template
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

from .models import Weibo
from .models import Like
from user.models import User
from user.models import Follow
from comment.models import Comment
from libs.db import db
from user.logics import login_required

weibo_bp = Blueprint('weibo', import_name='weibo')
weibo_bp.template_folder = './templates'


@weibo_bp.route('/')
@weibo_bp.route('/index')
def index():
    '''显示最新的前 50 条微博'''
    # 获取微博数据
    page = int(request.args.get('page', 1))
    n_per_page = 10
    offset = (page - 1) * n_per_page
    # 当前页要显示的微博
    # select * from weibo order by updated desc limit 10 offset 20;
    wb_list = Weibo.query.order_by(Weibo.updated.desc()).limit(10).offset(offset)
    n_weibo = Weibo.query.count()  # 微博总数
    n_page = 5 if n_weibo >= 50 else ceil(n_weibo / n_per_page)  # 总页数

    # 获取微博对应的作者
    uid_list = {wb.uid for wb in wb_list}  # 取出微博对应的用户 ID
    # select id, nickname from user id in ...;
    users = dict(User.query.filter(User.id.in_(uid_list)).values('id', 'nickname'))
    return render_template('index.html', page=page, n_page=n_page, wb_list=wb_list, users=users)


@weibo_bp.route('/follow_weibo')
@login_required
def follow_weibo():
    uid = session['uid']
    page = int(request.args.get('page', 1))

    # 获取关注的人的 ID 列表
    fid_list = [fid for (fid,) in Follow.query.filter_by(uid=uid).values('fid')]

    # 获取微博数据
    n_per_page = 10
    offset = (page - 1) * n_per_page
    wb_list = Weibo.query.filter(Weibo.uid.in_(fid_list)).order_by(Weibo.updated.desc()).limit(10).offset(offset)
    n_weibo = Weibo.query.filter(Weibo.uid.in_(fid_list)).count()  # 关注的微博总数
    n_page = 5 if n_weibo >= 50 else ceil(n_weibo / n_per_page)  # 总页数

    # 获取微博对应的作者
    users = dict(User.query.filter(User.id.in_(fid_list)).values('id', 'nickname'))
    return render_template('follow_weibo.html', page=page, n_page=n_page, wb_list=wb_list, users=users)


@weibo_bp.route('/post', methods=('POST', 'GET'))
@login_required
def post():
    if request.method == 'POST':
        content = request.form.get('content').strip()
        if not content:
            return render_template('post.html', error='微博内容不允许为空！')
        else:
            weibo = Weibo(uid=session['uid'], content=content)
            weibo.updated = datetime.datetime.now()
            db.session.add(weibo)
            db.session.commit()
            return redirect('/weibo/show?wid=%s' % weibo.id)
    else:
        return render_template('post.html')


@weibo_bp.route('/edit', methods=('POST', 'GET'))
@login_required
def edit():
    if request.method == 'POST':
        wid = int(request.form.get('wid'))
        content = request.form.get('content').strip()
        if not content:
            return render_template('post.html', error='微博内容不允许为空！')
        else:
            weibo = Weibo.query.get(wid)
            if weibo.uid != session['uid']:
                abort(403)
            weibo.content = content
            weibo.updated = datetime.datetime.now()
            db.session.add(weibo)
            db.session.commit()
            return redirect('/weibo/show?wid=%s' % weibo.id)
    else:
        wid = int(request.args.get('wid'))
        weibo = Weibo.query.get(wid)
        return render_template('edit.html', weibo=weibo)


@weibo_bp.route('/show')
def show():
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    if weibo is None:
        abort(404)
    else:
        user = User.query.get(weibo.uid)

        # 获取当前微博的所有评论
        comments = Comment.query.filter_by(wid=weibo.id).order_by(Comment.created.desc())
        all_uid = {c.uid for c in comments}  # 所有评论的作者的 ID
        cmt_users = dict(User.query.filter(User.id.in_(all_uid)).values('id', 'nickname'))
        comments = OrderedDict([[cmt.id, cmt] for cmt in comments])  # 将所有评论转成有序字典
        return render_template('show.html', weibo=weibo, user=user, cmt_users=cmt_users, comments=comments)


@weibo_bp.route('/delete')
@login_required
def delete():
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    if weibo.uid != session['uid']:
        abort(403)
    else:
        db.session.delete(weibo)
        db.session.commit()
    return redirect('/')


@weibo_bp.route('/like')
@login_required
def like():
    uid = session['uid']
    wid = int(request.args.get('wid'))

    lk = Like(uid=uid, wid=wid)
    db.session.add(lk)
    try:
        Weibo.query.filter_by(id=wid).update({'n_like': Weibo.n_like + 1})
        db.session.commit()
    except (FlushError, IntegrityError):
        db.session.rollback()
        Like.query.filter_by(uid=uid, wid=wid).delete()
        Weibo.query.filter_by(id=wid).update({'n_like': Weibo.n_like - 1})
        db.session.commit()

    last_url = request.referrer or '/weibo/show?wid=%s' % wid
    return redirect(last_url)


@weibo_bp.route('/top50')
def top50():
    '''最近一个月的热门微博'''
    now = datetime.datetime.now()
    start = now - datetime.timedelta(30)
    wb_list = Weibo.query.filter(Weibo.created > start).order_by(Weibo.n_like.desc()).limit(50)

    # 获取微博对应的作者
    uid_list = {wb.uid for wb in wb_list}  # 取出微博对应的用户 ID
    users = dict(User.query.filter(User.id.in_(uid_list)).values('id', 'nickname'))
    return render_template('top50.html', wb_list=wb_list, users=users)
