# -*- coding:utf8 -*-
from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    return render_template('login.html')

#獲取注冊請求並處理數據
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
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
        sql_insert = "insert into user (`id`, `username`, `password`) values(default, '"+username+"', '"+password+"')"

        try:
            cur.execute(sql_insert)
            #提交
            db.commit()
        except Exception as e:
            db.rollback()
        finally:
            db.close()
        return redirect(url_for('index')) #提交完數據後返回首頁




if __name__ == '__main__':
    app.run(debug=True)