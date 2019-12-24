#!/usr/bin/env python

from flask import Flask
from libs.db import db

app = Flask(__name__)

# 初始化数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://seamile:123@localhost/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'M\xd2\x16\xa0K\x01\x0f@\x9f(\xab2V\xd7\xe3\x00'
db.init_app(app)


@app.route('/')
def home():
    return 'Server is running...'


if __name__ == '__main__':
    from user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    app.debug = True
    app.run()
