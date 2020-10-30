from flask import Flask
from flask_pymongo import PyMongo

# 플라스크앱 등록, config파일로 config 일괄 등록
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

mongo = PyMongo(app)


# 블루프린트 등록
from .members import members_blueprint
from .books import books_blueprint
from .boards import boards_blueprint
from .draws import draw_blueprint

from . import routes

app.register_blueprint(members_blueprint)
app.register_blueprint(books_blueprint)
app.register_blueprint(boards_blueprint)
app.register_blueprint(draw_blueprint)


# TODO : 첨부파일 링크 or 파일 저장한거 불러오기 
# -> 구글 드라이브? 에버노트? 유튜브
# 목차마다 관련링크 저장
# TODO : 공부방이나 채팅 (소켓) 해보고 나중에 httpd나 nginx이용해서 화상채팅 