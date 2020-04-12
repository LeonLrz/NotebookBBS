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
from utils import restful, safeutils
from .forms import SignupForm, SigninForm, AddPostForm, AddCommentForm,StarPostForm,SettingsForm
from .models import FrontUser,LaptopInfo
from exts import db
import config
from ..models import BannerModel, BoardModel, PostModel, CommentModel, HighlightPostModel,PostStarModel
from .decorators import login_required
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import func
from datetime import datetime

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
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort
    }
    return render_template("front/front_index.html", **context)


@bp.route('/profile/<user_id>',methods=['GET'])
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
        context = {
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
            avatar = form.avatar.data
            signature = form.signature.data

            user_model = g.front_user
            user_model.username = username
            if realname:
                user_model.realname = realname
            if qq:
                user_model.qq = qq
            if avatar:
                user_model.avatar = avatar
            if signature:
                user_model.signature = signature
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


@bp.route('/notebook/')
def notebook():
    notebooks = LaptopInfo.query.all()
    context = {
        'notebooks':notebooks
    }
    return render_template('front/notebook.html',**context)


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


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))
