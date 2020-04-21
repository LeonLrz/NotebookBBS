from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    url_for,
    g,
    abort,
    redirect
)
from utils import restful, safeutils,mycache
from .forms import SignupForm, SigninForm, AddPostForm, AddCommentForm,StarPostForm,SettingsForm,ResetEmailForm,ResetpwdForm
from .models import FrontUser,LaptopInfo
from exts import db,mail
from flask_mail import Message
import config
from ..models import BannerModel, BoardModel, PostModel, CommentModel, HighlightPostModel,PostStarModel
from .decorators import login_required
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import func
from datetime import datetime
import string
import random

bp = Blueprint("front", __name__)


@bp.route("/")
def index():
    board_id = request.args.get("bd", type=int, default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    sort = request.args.get('st', type=int, default=1)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(3)
    boards = BoardModel.query.all()
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.filter(PostModel.is_removed == 0).order_by(PostModel.create_time.desc())
    elif sort == 2:
        # 加精的时间倒序排序
        query_obj = db.session.query(PostModel).filter(PostModel.is_removed == 0).outerjoin(HighlightPostModel). \
            order_by(HighlightPostModel.create_time.desc(), PostModel.create_time.desc())
    elif sort == 3:
        # 按点赞数量排序
        query_obj = db.session.query(PostModel).filter(PostModel.is_removed == 0).outerjoin(PostStarModel).group_by(PostModel.id).\
            order_by(func.count(PostStarModel.id).desc(), PostModel.create_time.desc())
    elif sort == 4:
        # 按照评论数量排序
        query_obj = db.session.query(PostModel).filter(PostModel.is_removed == 0).outerjoin(CommentModel).group_by(PostModel.id). \
            order_by(func.count(CommentModel.id).desc(), PostModel.create_time.desc())
    if board_id:
        query_obj = query_obj.filter(PostModel.board_id == board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2,per_page_parameter=config.PER_PAGE)
    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort
    }
    return render_template("front/front_index.html", **context)


@bp.route('/profile/<user_id>/',methods=['GET'])
def profile(user_id=0):
    if not user_id:
        return abort(404)

    user = FrontUser.query.get(user_id)
    if user:
        context = {
            'current_user': user
        }
        return render_template('front/front_profile.html',**context)
    else:
        return abort(404)


@bp.route('/profile/posts/',methods=['GET'])
def profile_posts():
    user_id = request.args.get('user_id')
    if not user_id:
        return abort(404)

    user = FrontUser.query.get(user_id)
    if user:
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page - 1) * 8
        end = start + 8
        posts = PostModel.query.filter_by(author_id=user_id).slice(start, end)
        total_posts = PostModel.query.filter_by(author_id=user_id).count()
        pagination_config = {
            "bs_version": 3,
            "outer_window": 0,
            "inner_window": 2,
            "per_page": 8
        }
        post_pagination = Pagination(**pagination_config,page=page,total=total_posts)
        context = {
            'posts':posts,
            'p_pagination':post_pagination,
            'current_user': user,
        }
        return render_template('front/front_profile_posts.html',**context)
    else:
        return abort(404)


@bp.route('/settings/',methods=['POST','GET'])
@login_required
def settings():
    if request.method == 'GET':
        return render_template('front/front_settings.html')
    else:
        form = SettingsForm(request.form)
        if form.validate():
            username = form.username.data
            realname = form.realname.data
            qq = form.qq.data
            avatar = request.form.get("avatar")
            signature = form.signature.data
            gender = request.form.get("gender",type=int)

            user_model = g.front_user
            user_model.username = username
            if realname:
                user_model.realname = realname
            if qq:
                user_model.qq = qq
            if avatar != "/static/common/images/avatar.png":
                user_model.avatar = avatar
            if signature:
                user_model.signature = signature
            if gender:
                user_model.gender = gender
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


@bp.route('/logout/')
@login_required
def logout():
    del session[config.FRONT_USER_ID]
    return redirect(url_for("front.index"))


@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    posts_list = PostModel.query.order_by(PostModel.read_count.desc())[0:10]
    if not post:
        abort(404)
    # 获取这篇帖子的所有赞的作者的id，方便模版中判断
    post.read_count += 1
    db.session.commit()
    print(post.read_count)
    star_author_ids = [star_model.author.id for star_model in post.stars]
    context = {
        'post': post,
        'star_author_ids': star_author_ids,
        'posts_list':posts_list
    }
    return render_template('front/front_pdetail.html', **context)


@bp.route('/notebooks/')
def notebooks():
    brand = request.args.get("brand")
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * 12
    end = start + 12
    if brand:
        notebooks = LaptopInfo.query.filter_by(brand=brand).slice(start,end)
        total = LaptopInfo.query.filter_by(brand=brand).count()
    else:
        notebooks = LaptopInfo.query.slice(start, end)
        total = LaptopInfo.query.count()
    pagination_config = {
        "bs_version": 3,
        "page": page,
        "total":total,
        "outer_window": 0,
        "inner_window": 2,
        "per_page":12
    }
    pagination = Pagination(**pagination_config)
    context = {
        'pagination': pagination,
        'notebooks':notebooks,
        'brand':brand
    }
    return render_template('front/notebooks.html', **context)


@bp.route("/notebooks/<notebook_id>/")
def notebook_detail(notebook_id):
    notebook = LaptopInfo.query.get(notebook_id)
    ranked_notebooks = LaptopInfo.query.filter_by(brand=notebook.brand).order_by(LaptopInfo.rate.desc()).limit(10)
    related_notebooks = LaptopInfo.query.filter_by(laptop_position=notebook.laptop_position).order_by(LaptopInfo.rate.desc()).limit(4)
    context = {
        'notebook':notebook,
        'ranked_notebooks':ranked_notebooks,
        'related_notebooks':related_notebooks
    }
    return render_template('front/notebook_detail.html',**context)


class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


@bp.route('/acomment/',methods=['POST','GET'])
@login_required
def add_comment():
    if request.method == 'GET':
        post_id = request.args.get('post_id',type=int)
        comment_id = request.args.get('comment_id',type=int)
        context = {
            'post': PostModel.query.get(post_id)
        }
        if comment_id:
            context['origin_comment'] = CommentModel.query.get(comment_id)
        return render_template('front/front_addcomment.html',**context)
    else:
        if g.front_user:
            if not g.front_user.is_active:
                return restful.params_error(message="对不起，您的账号已被封禁，无法发表评论！")
        form = AddCommentForm(request.form)
        if form.validate():
            content = form.content.data
            post_id = form.post_id.data
            post = PostModel.query.get(post_id)
            if post:
                comment = CommentModel(content=content)
                comment.post = post
                comment.author = g.front_user
                origin_comment_id = request.form.get("origin_comment_id", type=int)
                comment.origin_comment_id = origin_comment_id
                if origin_comment_id:
                    g.front_user.points += 1
                else:
                    g.front_user.points += 3
                db.session.add(comment)
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error("没有这篇帖子")
        else:
            return restful.params_error(message=form.get_error())


@bp.route('/star_post/',methods=['POST'])
@login_required
def star_post():
    form = StarPostForm(request.form)
    if form.validate():
        post_id = form.post_id.data
        is_star = form.is_star.data

        post_model = PostModel.query.get(post_id)
        star_model = PostStarModel.query.filter_by(author_id=g.front_user.id, post_id=post_id).first()
        if is_star:
            # 要从数据库中查找一下，当前这个点赞是否存在，如果不存在，就添加，否则就提示已经点赞了
            if star_model:
                return restful.params_error(message=u'您已经给这篇帖子点赞了，无需再点！')
            star_model = PostStarModel()
            star_model.author = g.front_user
            star_model.post = post_model
            db.session.add(star_model)
            db.session.commit()
            return restful.success()
        else:
            if star_model:
                db.session.delete(star_model)
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error(message=u'你尚未对该帖子进行点赞！')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/apost/', methods=['POST', 'GET'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html', boards=boards)
    else:
        if g.front_user:
            if not g.front_user.is_active:
                return restful.params_error(message="对不起，您的账号已被封禁，无法发帖！")
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message="没有这个版块！")
            post = PostModel(title=title, content=content)
            post.board = board
            post.author = g.front_user
            g.front_user.points += 5
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for("front.signin") and safeutils.is_safe_url(
                return_to):
            return render_template("front/front_signin.html", return_to=return_to)
        else:
            return render_template("front/front_signin.html")

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                user.last_login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db.session.commit()
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                    return restful.success()
            else:
                return restful.params_error(message="手机号或密码错误！")
        else:
            return restful.params_error(message=form.get_error())


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("front/front_resetpwd.html")

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.front_user
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
        return render_template("front/front_resetemail.html")

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.front_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


@bp.route('/forget/')
def forget():
    return render_template('front/front_forgetpwd.html')


@bp.route('/forgetpwd_chekemail/',methods=["GET","POST"])
def forgetpwd_chekemail():
    email = request.form.get("email")
    captcha = request.form.get("captcha")
    user = FrontUser.query.filter_by(email=email).first()
    if not user:
        return restful.params_error("该邮箱不存在！")
    captcha_cache = mycache.get(email)
    if not captcha_cache or captcha.lower() != captcha_cache.lower():
        return restful.params_error('邮箱验证码错误！')
    return restful.success(data={'user_id': user.id})


@bp.route('/findpwd/<user_id>/',methods=["GET","POST"])
def findpwd(user_id):
    if request.method == "GET":
        user = FrontUser.query.get(user_id)
        return render_template("front/front_findpwd.html",user=user)
    else:
        newpwd = request.form.get("newpwd")
        newpwd2 = request.form.get("newpwd2")
        if newpwd != newpwd2:
            return restful.params_error("两次密码输入不一致！")
        user = FrontUser.query.get(user_id)
        user.password = newpwd
        db.session.commit()
        return restful.success()


@bp.route('/search/')
def search():
    s_type = int(request.args.get('type'))
    s_keyword = request.args.get("kw").strip()
    if not s_keyword:
        results = None
        page = 0
        total = 0
    else:
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page - 1) * 12
        end = start + 12
        if s_type == 1:
            query_obj = PostModel.query.filter(PostModel.title.contains(s_keyword))\
                .order_by(PostModel.create_time.desc())
            results = query_obj.slice(start, end)
            total = query_obj.count()
        elif s_type == 2:
            query_obj = LaptopInfo.query.filter(LaptopInfo.laptop_model.contains(s_keyword))\
                .order_by(LaptopInfo.rate.desc())
            results = query_obj.slice(start, end)
            total = query_obj.count()

    pagination_config = {
        "bs_version": 3,
        "page": page,
        "total": total,
        "outer_window": 0,
        "inner_window": 2,
        "per_page": 12
    }
    pagination = Pagination(**pagination_config)
    context = {
        'type': s_type,
        'total':total,
        'keyword': s_keyword,
        'results': results,
        'pagination':pagination
    }
    return render_template('front/front_search.html', **context)


@bp.route('/email_captcha/')
def email_captcha():
    # 查询字符串方式传递邮箱
    # /email_captcha/?email=xxx@xx.com
    email = request.args.get("email")
    forget_para = request.args.get('forget',type=int)
    if forget_para != 1:
        user = FrontUser.query.filter_by(email=email).first()
        if user:
            return restful.params_error("该邮箱已被占用，请更换邮箱！")
        old_email = g.front_user.email
        if email == old_email:
            return restful.params_error("请勿使用相同的邮箱！")
    if not email:
        return restful.params_error("请输入邮箱！")
    source = list(string.ascii_letters)
    source.extend(map(str, range(0, 10)))
    captcha = "".join(random.sample(source, 6))
    # 给该邮箱发邮件
    message = Message(
        "NotebooksBBS验证邮件",
        recipients=[email],
        body="您正在绑定或修改邮箱！验证码是：" + captcha + "\n请勿告诉任何人！")
    try:
        mail.send(message)
    except BaseException:
        return restful.server_error("请输入正确的邮箱！")
    mycache.set(email, captcha)
    return restful.success("验证码发送成功！")


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))
bp.add_url_rule('/resetpwd/',
                view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
