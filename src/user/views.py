import datetime

from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from sqlalchemy.exc import IntegrityError

from libs.db import db
from libs.utils import gen_password, check_password
from .models import User
from .logics import save_avatar

user_bp = Blueprint('user', import_name='user')
user_bp.template_folder = './templates'


@user_bp.route('/register', methods=('GET', 'POST'))
def register():
    '''
    注册页面

    开发时的异常处理：
        1. 明确处理每一个异常
        2. try 和 except 之间的语句越少越好
        3. 不要隐藏异常，而应该定向处理异常
    '''
    if request.method == 'POST':
        # 先取出所有的参数
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()
        gender = request.form.get('gender', '').strip()
        bio = request.form.get('bio', '').strip()
        city = request.form.get('city', '').strip()
        birthday = request.form.get('birthday', '').strip()
        avatar = request.files.get('avatar')

        # 创建用户
        user = User(
            nickname=nickname,
            password=gen_password(password),
            gender=gender if gender in ['male', 'female'] else 'male',
            bio=bio,
            city=city,
            birthday=birthday,
            avatar='/static/upload/%s' % nickname,
            created=datetime.datetime.now()
        )

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('register.html', error='昵称已被占用，请换一个')

        save_avatar(nickname, avatar)
        return redirect('/user/login')
    else:
        return render_template('register.html')


@user_bp.route('/login', methods=('GET', 'POST'))
def login():
    '''登陆页面'''
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(nickname=nickname).first()
        if user is None:
            return render_template('login.html', error='用户名有误，请重新输入')
        if check_password(password, user.password):
            # 记录用户登陆状态
            session['uid'] = user.id
            return redirect('/user/info')
        else:
            return render_template('login.html', error='密码有误，请重新输入')
    else:
        if 'uid' in session:
            return redirect('/user/info')
        else:
            return render_template('login.html')


@user_bp.route('/logout')
def logout():
    '''退出'''
    session.pop('uid')
    return redirect('/')


@user_bp.route('/info')
def info():
    '''用户个人资料页'''
    uid = session.get('uid')
    if uid:
        user = User.query.get(uid)
        return render_template('info.html', user=user)
    else:
        return render_template('login.html', error='请先登录！')
