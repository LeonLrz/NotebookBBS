from exts import db
import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from datetime import datetime


class GenderType(object):
    MAN = 1
    WOMAN = 2
    SECRET = 3
    UNKNOW = 4


class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    telephone = db.Column(db.String(11),nullable=False,unique=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50),unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Integer, default=GenderType.UNKNOW)
    join_time = db.Column(db.DateTime,default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    last_login_time = db.Column(db.DateTime, nullable=True)
    old_login_time = db.Column(db.DateTime)
    qq = db.Column(db.String(20))
    points = db.Column(db.Integer,default=0)

    def __init__(self,*args,**kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(FrontUser,self).__init__(*args,**kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result