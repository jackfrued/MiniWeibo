#!/usr/bin/env python

import random
import datetime
from string import ascii_lowercase

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from main import app
from libs.db import db
from user.models import User
from weibo.models import Weibo
from libs.utils import gen_password

db.init_app(app)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


def rand_content(n_words=10):
    rand_word = lambda: ''.join(random.sample(ascii_lowercase, random.randint(3, 5)))
    rand_content = ' '.join([rand_word() for i in range(n_words)])
    return rand_content.capitalize()


@manager.command
def insert_weibo_data():
    '''插入一些微博数据'''
    # 创建一批测试用户
    users = []
    for i in range(10):
        user = User(
            nickname='test-%x' % random.randint(100, 999),
            password=gen_password('1234567890'),
            gender=random.choice(['male', 'female']),
            bio=rand_content(5),
            city=random.choice(['北京', '上海', '深圳']),
            avatar='/static/img/logo.png',
            birthday='1990-02-%s' % random.randint(1, 28),
        )
        users.append(user)
        print('add user %s' % user.nickname)
    db.session.add_all(users)
    db.session.commit()
    user_id_list = [u.id for u in users]  # 取出这些用户的 ID

    # 添加一些微博
    wb_list = []
    for i in range(10000):
        y = random.randint(2015, 2018)
        m = random.randint(1, 12)
        d = random.randint(1, 28)
        h = random.randint(0, 23)
        M = random.randint(0, 59)
        s = random.randint(0, 59)
        created = datetime.datetime(y, m, d, h, M, s)
        wb = Weibo(uid=random.choice(user_id_list),
                   content=rand_content(20),
                   created=created,
                   updated=created)
        wb_list.append(wb)
        print('add weibo: %s' % wb.content)
    db.session.add_all(wb_list)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
