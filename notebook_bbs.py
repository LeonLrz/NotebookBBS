# config.py 配置文件
# exts.py 第三方库文件
# manage.py 管理项目运行的文件
# apps存储前台front、后台cms、公共部分common三个蓝图模块,分别包括
# models.py模型文件/
# views.py视图函数/
# forms.py表单模型分别存储在不同蓝图中
# utils包，包含工具模块，restful是前后端返回的json格式规范

from flask import Flask
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
from apps.ueditor import bp as ueditor_bp
import config
from exts import db,mail
from flask_wtf import CSRFProtect


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(ueditor_bp)

    db.init_app(app)
    CSRFProtect(app)
    mail.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
