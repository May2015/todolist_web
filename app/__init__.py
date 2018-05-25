# -*- coding:utf8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#初始化Bootstrap
bootstrap = Bootstrap()

#初始化數據庫
db = SQLAlchemy()

#初始化login登錄
login_manage = LoginManager()
login_manage.session_protection = 'strong'
login_manage.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    # 配置數據庫，改pymysql用flask_sqlalchemy來管理
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://root:9@127.0.0.1:3306/todolist'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    #debug mode
    app.config['DEBUG'] = True

    # 密鈅用於flask-wtf保護表單數據
    app.config['SECRET_KEY'] = 'do not try to guess my string'

    #實例化
    bootstrap.init_app(app)
    db.init_app(app)

    #實例化登錄
    login_manage.init_app(app)

    #注冊認證藍本
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


    return app