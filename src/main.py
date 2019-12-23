#!/usr/bin/env python

from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    return 'Server is running...'


if __name__ == '__main__':
    app.debug = True
    app.run()
