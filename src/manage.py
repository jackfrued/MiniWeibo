#!/usr/bin/env python

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from main import app
from libs.db import db
from user.models import User
from weibo.models import Weibo

db.init_app(app)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
