from . import db

class User(db.Model):
    '''
    record info about username email and password
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    #爲安全，存儲密碼的hash值
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>'%self.username