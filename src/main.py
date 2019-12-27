#!/usr/bin/env python

from flask import Flask
from flask import redirect
from flask import render_template

from libs.db import db
from user import user_bp
from weibo import weibo_bp
from comment import comment_bp

app = Flask(__name__)
app.secret_key = 'M\xd2\x16\xa0K\x01\x0f@\x9f(\xab2V\xd7\xe3\x00'

# 初始化数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://seamile:123@localhost/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)


@app.route('/')
def home():
    return redirect('/weibo/')


app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(weibo_bp, url_prefix='/weibo')
app.register_blueprint(comment_bp, url_prefix='/comment')


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
