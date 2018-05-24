# -*- coding:utf8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from form import RegistrationForm
import pymysql

app = Flask(__name__)

#實例化Bootstrap
bootstrap = Bootstrap(app)
#密鈅用於flask-wtf保護表單數據
app.config['SECRET_KEY'] = 'do not try to guess my string'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
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
        return render_template('login.html')

#獲取注冊請求並處理數據
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
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
        return redirect(url_for('index')) #提交完數據後返回首頁

if __name__ == '__main__':
    app.run(debug=True)