# -*- coding:utf8 -*-
from flask import render_template, request, redirect, url_for
from app.auth.form import RegistrationForm, LoginForm
from . import auth
import pymysql

@auth.route('/')
def index():
    return render_template('auth/index.html')

@auth.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('auth/login.html', form=form)
    else:
        #連接數據庫
        db = pymysql.connect(host='127.0.0.1', user='root', password='9',
                             db = 'todolist', port=3306)

        cur = db.cursor()

        #sql 查詢
        username = request.form.get('username')
        password = request.form.get('password')
        query_sql = "select * from user where username='"+username+"' and password=''"+password+"'"

        try:
            cur.execute(query_sql)
            results = cur.fetchall()
            print(len(results))
            if len(results) == 1:
                return redirect(url_for('index'))
            else:
                print('Invalid username or password.')
            db.commit()
        except Exception as e:
            db.rollback()
        finally:
            print('close db connection')
            cur.close()
            db.close()
        return render_template('auth/login.html')

#獲取注冊請求並處理數據
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('auth/register.html', form=form)
    else:
        #將用戶名和密碼加入數據庫
        #手動連接數據庫前，先mysql命令手動建立數據庫與user表
        #此過程可手動導入sql腳本實現
        #port 請用show global variables like 'port' 查看
        db = pymysql.connect(host='127.0.0.1', user='root', password='9',
                             db = 'todolist', port=3306)

        #cursor()方法得到遊標操作數據庫
        cur = db.cursor()

        #插入數據的sql語句,變量插入爲外單引號，內雙綽號
        username = request.form.get('username')
        password = request.form.get('password')
        insert_sql = "insert into user (`id`, `username`, `password`) values(default, '"+username+"', '"+password+"')"

        try:
            cur.execute(insert_sql)
            #提交
            db.commit()
        except Exception as e:
            db.rollback()
        finally:
            cur.close()
            db.close()
        return redirect(url_for('auth/index')) #提交完數據後返回首頁


