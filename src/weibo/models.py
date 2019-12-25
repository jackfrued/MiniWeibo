import datetime

from libs.db import db


class Weibo(db.Model):
    __tablename__ = 'weibo'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.now)  # 发布时间
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.now)  # 最后修改的时间
