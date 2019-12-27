from libs.db import db


class User(db.Model):
    '''用户表'''
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), unique=True, nullable=False, index=True)
    password = db.Column(db.String(128), nullable=True)
    gender = db.Column(db.String(10), default='unknow')
    bio = db.Column(db.String(200))
    city = db.Column(db.String(16), default='上海')
    avatar = db.Column(db.String(128))
    birthday = db.Column(db.Date, default='1990-01-01')
    created = db.Column(db.DateTime)


class Follow(db.Model):
    '''关注表'''
    __tablename__ = 'follow'

    uid = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer, primary_key=True)
