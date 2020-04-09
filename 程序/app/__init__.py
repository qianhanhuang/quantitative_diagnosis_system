from flask import Flask, Blueprint, redirect, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from config import *
from flask_login import LoginManager, login_user, logout_user, login_required



db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'


def create_app():
    app = Flask(__name__, template_folder='../templates',static_folder='../static')
    # app.config["SECRET_KEY"] = os.urandom(24)  # 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除
    app.config["SECRET_KEY"] = "abcdefghijklmnopqrstuvwx"  # 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除
    app.config['PERMANENT_SESSION_LIFETIME'] = 864000
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager.init_app(app)
    return app


class Route_map():
    def __init__(self, route_index, func, methods):
        self.route_index = route_index
        self.func = func
        self.methods = methods
