from . import db, login_manage
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime

#UserMixin用於支持用戶登錄
class User(db.Model, UserMixin):
    '''
    record info about username email and password
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # 爲安全，存儲密碼的hash值
    password_hash = db.Column(db.String(128))
    # 賬戶郵件確認
    confirmed = db.Column(db.Boolean, default=False)
    # users events 一對多關系表
    events = db.relationship('Event', backref = 'sponsor', lazy='dynamic')

    # 加密令牌用於生成用戶的確認url鏈接
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        return s.dumps({'confirm': self.id})

    # 確認鏈接中的URL令牌與用戶id進行比對確認
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    # 密碼進行加密存儲
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>'%self.username

# 用於管理登錄
@login_manage.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    category = db.Column(db.String(64))
    completion = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    @staticmethod
    def insert_categories():
        cate = ['Study', 'Work', 'Life', 'Plans']
        for c in cate:
            category = Category.query.filter_by(name=c).first()
            if category is None:
                category = Category(name=c)
            db.session.add(category)
        db.session.commit()




