#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return 'Server is running...'


if __name__ == '__main__':
    from user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    app.debug = True
    app.run()
