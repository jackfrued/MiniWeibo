import datetime

from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
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
        pass
    else:
        return render_template('login.html')


@user_bp.route('/logout')
def logout():
    '''退出'''
    pass


@user_bp.route('/info')
def info():
    '''用户个人资料页'''
    pass
