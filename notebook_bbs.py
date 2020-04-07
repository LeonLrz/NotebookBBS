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
from datetime import datetime

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

    # 自定义时间过滤器
    @app.template_filter('handle_time')
    def handle_time(time):
        """
        time距离现在的时间间隔
        1. 如果时间间隔小于1分钟以内，那么就显示“刚刚”
        2. 如果是大于1分钟小于1小时，那么就显示“xx分钟前”
        3. 如果是大于1小时小于24小时，那么就显示“xx小时前”
        4. 如果是大于24小时小于30天以内，那么就显示“xx天前”
        5. 否则就是显示具体的时间 2020/03/20 16:15
        """
        if isinstance(time, datetime):
            now = datetime.now()
            timestamp = (now - time).total_seconds()
            if timestamp < 60:
                return "刚刚"
            elif timestamp >= 60 and timestamp < 60 * 60:
                minutes = timestamp / 60
                return "%s分钟前" % int(minutes)
            elif timestamp >= 60 * 60 and timestamp < 60 * 60 * 24:
                hours = timestamp / (60 * 60)
                return '%s小时前' % int(hours)
            elif timestamp >= 60 * 60 * 24 and timestamp < 60 * 60 * 24 * 30:
                days = timestamp / (60 * 60 * 24)
                return "%s天前" % int(days)
            else:
                return time.strftime('%Y/%m/%d %H:%M')
        else:
            return time

    @app.template_filter("exact_time")
    def exact_time(time):
        '''
        将具体时间格式化成2020年3月20日 16:15
        '''
        return time.strftime('%Y{y}%m{m}%d{d} %H:%M').format(y='年', m='月', d='日')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
