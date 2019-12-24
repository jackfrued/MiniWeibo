from flask_sqlalchemy import SQLAlchemy

from main import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://seamile:123@localhost/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
