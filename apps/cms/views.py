from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
    abort
)
from .forms import (
    LoginForm,
    ResetpwdForm,
    ResetEmailForm,
    AddBannerForm,
    UpdateBannerForm,
    AddBoardForm,
    UpdateBoardForm,
    CMSBlackFrontUserForm
)
from ..models import BannerModel, BoardModel,PostModel,HighlightPostModel
from .models import CMSUser, CMSPermission
from ..front.models import FrontUser
from .decorators import login_required, permission_required
import config
from exts import db, mail
from flask_mail import Message
from utils import restful, mycache
import string
import random
from flask_paginate import Pagination,get_page_parameter

bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.route("/")
@login_required
def index():
    return render_template("cms/cms_index.html")


@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for("cms.login"))


@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    total = PostModel.query.count()
    pagination_config = {
        "bs_version": 3,
        "page": page,
        "total":total,
        "outer_window": 0,
        "inner_window": 2,
        "display_msg":'''本页展示第 <b>{start} - {end}</b> {record_name} 共有 <b>{total}</b>篇帖子''',
        "record_name": "篇帖子",
    }
    pagination = Pagination(**pagination_config)
    context = {
        'pagination': pagination,
        'posts':PostModel.query.order_by(PostModel.create_time.desc()).slice(start, end)
    }
    return render_template('cms/cms_posts.html',**context)


@bp.route('/hpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def hpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error("请传入帖子id！")
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")

    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/uhpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def uhpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error("请传入帖子id！")
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")
    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/rmpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def rmpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error("请传入帖子id！")
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")
    post.is_removed = 1
    db.session.commit()
    return restful.success()


@bp.route('/urmpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def urmpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error("请传入帖子id！")
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")
    post.is_removed = 0
    db.session.commit()
    return restful.success()


@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    board_models = BoardModel.query.all()
    context = {
        'boards':board_models
    }
    return render_template('cms/cms_boards.html',**context)


@bp.route('/aboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/uboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有该板块！")
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def dboard():
    board_id = request.form.get("board_id")
    if not board_id:
        return restful.params_error(message="请传入板块id！")

    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message='没有这个板块！')

    db.session.delete(board)
    db.session.commit()
    return restful.success()


@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    sort = request.args.get('sort')
    # 1:  按加入时间排序
    # 2： 按发表帖子数量排序
    # 3： 按评论数量排序
    front_users = None
    # 如果没有sort，默认按时间排序
    if not sort or sort == '1':
        front_users = FrontUser.query.order_by(FrontUser.join_time.desc()).all()
    else:
        front_users = FrontUser.query.all()
    context = {
        'front_users': front_users,
        'current_sort': sort
    }
    return render_template('cms/cms_fusers.html', **context)

@bp.route('/edit_frontuser/')
@login_required
def edit_frontuser():
    user_id = request.args.get('id')
    if not user_id:
        abort(404)

    user = FrontUser.query.get(user_id)
    if not user:
        abort(404)
    return render_template('cms/cms_editfrontuser.html',current_user=user)

@bp.route('/black_front_user/',methods=['POST'])
def black_front_user():
    form = CMSBlackFrontUserForm(request.form)
    if form.validate():
        user_id = form.user_id.data
        is_black =form.is_black.data
        user = FrontUser.query.get(user_id)
        if not user:
            abort(404)
        user.is_active = not is_black
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)


@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.image_url.data
        priority = form.priority.data
        banner = BannerModel(
            name=name,
            image_url=image_url,
            link_url=link_url,
            priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有该轮播图！")
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message="请输入轮播图id！")

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()


@bp.route('/unauth/')
def unauth():
    return render_template('cms/cms_unauth.html')


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template("cms/cms_login.html", message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    # 默认31天过期,配置文件中改为7天
                    session.permanent = True
                return redirect(url_for("cms.index"))
            else:
                return self.get(message="邮箱或密码错误")
        else:
            message = form.get_error()
            return self.get(message=message)


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("cms/cms_resetpwd.html")

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # {"code":200,"message":"密码错误"}
                return restful.success()
            else:
                return restful.params_error("旧密码错误!")
        else:
            return restful.params_error(form.get_error())


class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("cms/cms_resetemail.html")

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


@bp.route('/profile/')
@login_required
def profile():
    return render_template("cms/cms_profile.html")


@bp.route('/email_captcha/')
def email_captcha():
    # 查询字符串方式传递邮箱
    # /email_captcha/?email=xxx@xx.com
    email = request.args.get("email")
    if not email:
        return restful.params_error("请输入邮箱！")
    source = list(string.ascii_letters)
    source.extend(map(str, range(0, 10)))
    captcha = "".join(random.sample(source, 6))
    # 给该邮箱发邮件
    message = Message(
        "NotebooksBBS验证邮件",
        recipients=[email],
        body="您的验证码是：" + captcha)
    try:
        mail.send(message)
    except BaseException:
        return restful.server_error("验证码发送失败！")
    mycache.set(email, captcha)
    return restful.success("验证码发送成功！")


bp.add_url_rule('/login/',
                view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',
                view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
