# -*- coding:utf8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

# 初始化Bootstrap
bootstrap = Bootstrap()

# 初始化數據庫
db = SQLAlchemy()

# 初始化login登錄
login_manage = LoginManager()
login_manage.session_protection = 'strong'
login_manage.login_view = 'auth.login'

# 初始化郵件發送服務
mail = Mail()

def create_app():
    app = Flask(__name__)

    # 配置數據庫，改pymysql用flask_sqlalchemy來管理
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://root:9@127.0.0.1:3306/todolist'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    #配置發送確認郵件的郵箱
    app.config['MAIL_SERVER'] = 'smtp.126.com'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = "jiulixiang_88@126.com"   # bug: dangerous username
    app.config['MAIL_PASSWORD'] = "xiaoman520"   # bug: dangerous passwords
    app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Todolist]'
    app.config['FLASKY_MAIL_SENDER'] = 'jiulixiang_88@126.com'
    app.config['FLASKY_ADMIN'] = "jiulixiang_88@126.com"

    #debug mode
    app.config['DEBUG'] = True

    # 密鈅用於flask-wtf保護表單數據
    app.config['SECRET_KEY'] = 'do not try to guess my string'

    # 實例化
    bootstrap.init_app(app)
    # 實例化數據庫
    db.init_app(app)
    # 實例化登錄
    login_manage.init_app(app)
    # 實例化郵件發送服務
    mail.init_app(app)


    #注冊認證藍本
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


    return app