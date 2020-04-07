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


class LaptopInfo(db.Model):
    __tablename__ = 'laptopinfo'

    id = db.Column(db.Integer, primary_key=True)
    laptop_model = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    brand = db.Column(db.String(200), server_default=db.FetchedValue())
    url = db.Column(db.String(300), nullable=False, server_default=db.FetchedValue())
    pic = db.Column(db.String(300), nullable=False, server_default=db.FetchedValue())
    rate = db.Column(db.String(4), nullable=False, server_default=db.FetchedValue())
    hash = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    detail_url = db.Column(db.String(300), nullable=False, server_default=db.FetchedValue())
    parameter_url = db.Column(db.String(300), nullable=False, server_default=db.FetchedValue())
    laptop_position = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    laptop_price = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    laptop_cpu = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    laptop_cpu_freq = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    laptop_cpu_core = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    laptop_gpu = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    laptop_ram = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    laptop_rom = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    laptop_weight = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
