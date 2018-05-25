# -*- coding:utf8 -*-
from flask import render_template, request, redirect, url_for, flash
from app.auth.form import RegistrationForm, LoginForm
from . import auth
from app import db
from app.models import User
import pymysql

@auth.route('/')
def index():
    return render_template('index.html')

@auth.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            return redirect(url_for('auth.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

#獲取注冊請求並處理數據
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('auth/register.html', form=form)
    else:
        if form.validate_on_submit():
            user = User(email=form.email.data,
                        username = form.username.data,
                        password = form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("You can now login.")
            return redirect(url_for('auth.login')) #提交完數據後返回首頁


