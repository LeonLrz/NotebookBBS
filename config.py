DEBUG = True
from datetime import timedelta
SECRET_KEY = '\xf9AR\x1d\\\xf0\xd3\x0e\xa3\x16(f\xd0\xd0\xb7\xfb~\x81\x8a\xeb\x12\xbb\x986'

# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'a8824481'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'notebook_bbs'


PERMANENT_SESSION_LIFETIME = timedelta(days=7)

DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".\
    format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = 'wuyiyizifuchuan'
FRONT_USER_ID = 'suibiangeide'

# 发送者邮箱的服务器地址
MAIL_SERVER = "smtp.qq.com"
# qq不支持非加密ssl协议，ssl端口号为587/465
# 使用TLS协议，端口号587
# 使用SSL协议，端口号465
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL = True/False
# MAIL_DEBUG = True/False
MAIL_USERNAME = "920592896@qq.com"
MAIL_PASSWORD = "pvlblrcpuokybfhc"
MAIL_DEFAULT_SENDER = "920592896@qq.com"

# UEditor的相关配置
# UEditor 使用七牛作为存储文件的服务器
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = 'yyuGQ23-tev5MH3frrHRlywopGfNOSo1jFuJ0WMR'
UEDITOR_QINIU_SECRET_KEY = 'QoM8Tta-a3epznleHtq-tuyn59w92HIaH34vGxjy'
UEDITOR_QINIU_BUCKET_NAME = 'lrzleonstore'
UEDITOR_QINIU_DOMAIN = 'http://q7ng4sydq.bkt.clouddn.com/'

#七牛相关配置
QINIU_ACCESS_KEY = UEDITOR_QINIU_ACCESS_KEY
QINIU_SECRET_KEY = UEDITOR_QINIU_SECRET_KEY
QINIU_BUCKET_NAME = UEDITOR_QINIU_BUCKET_NAME
# 这个域名需要到用到七牛的js文件中去配置，如front_settings.html/ cms_banners.js
QINIU_DOMAIN = UEDITOR_QINIU_DOMAIN

# flask-paginate相关配置
PER_PAGE = 10
