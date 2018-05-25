#! /usr/bin/env python3
import os
from app import create_app, db
from app.models import User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app()
#命令行啓動設置選項支持
manager = Manager(app)
#爲管理數據庫更新進行配置migrate命令
migrate = Migrate(app, db)

# 建立數據庫與表
#if db:
    #db.drop_all(app)
#db.create_all(app)

#添加shell命令行支持
def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()