from flask import Blueprint

from .models import User

user_bp = Blueprint('user', import_name='user')
user_bp.template_folder = './templates'


@user_bp.route('/login')
def login():
    '''登陆页面'''
    return 'user login'


@user_bp.route('/register')
def register():
    '''注册页面'''
    pass


@user_bp.route('/logout')
def logout():
    '''退出'''
    pass


@user_bp.route('/info')
def info():
    '''用户个人资料页'''
    pass
