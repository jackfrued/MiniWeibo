from flask import Blueprint
from flask import abort
from flask import abort
from flask import request
from flask import redirect

from libs.db import db
from user.logics import login_required
from .models import Comment

comment_bp = Blueprint('comment', import_name='comment')


@comment_bp.route('/comment', methods=('POST',))
@login_required
def comment():
    uid = session['uid']
    wid = int(request.form.get('wid'))
    content = request.form.get('content')
    cmt = Comment(uid=uid, wid=wid, content=content)
    db.session.add(cmt)
    db.session.commit()
    return redirect('/weibo/show?wid=%s' % wid)


@comment_bp.route('/reply', methods=('POST',))
@login_required
def reply():
    uid = session['uid']
    wid = int(request.form.get('wid'))
    cid = int(request.form.get('cid'))
    content = request.form.get('content')
    cmt = Comment(uid=uid, wid=wid, cid=cid, content=content)
    db.session.add(cmt)
    db.session.commit()
    return redirect('/weibo/show?wid=%s' % wid)


@comment_bp.route('/delete')
@login_required
def delete():
    cid = int(request.args.get('cid'))
    cmt = Comment.query.get(cid)

    # 检查是否是在删除自己的评论
    if cmt.uid != session['uid']:
        abort(403)

    if cmt.cid == 0:
        Comment.query.filter_by(cid=cmt.id).delete()
    db.session.delete(cmt)
    db.session.commit()

    return redirect('/weibo/show?wid=%s' % cmt.wid)
