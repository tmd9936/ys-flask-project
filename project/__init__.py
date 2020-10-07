from flask import Flask
from flask_pymongo import PyMongo

# 플라스크앱 등록, config파일로 config 일괄 등록
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

mongo = PyMongo(app)


# 블루프린트 등록
from .members import members_blueprint

from . import routes

app.register_blueprint(members_blueprint)