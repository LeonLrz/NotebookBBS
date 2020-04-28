# 轮播图模型

from exts import db
from datetime import datetime
from sqlalchemy.orm import backref


class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    image_url = db.Column(db.String(255),nullable=False)
    link_url = db.Column(db.String(255),nullable=False)
    priority = db.Column(db.Integer,default=0)
    create_time = db.Column(db.DateTime,default=datetime.now)


class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class PostModel(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(200),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
    read_count = db.Column(db.Integer,default=0)
    is_removed = db.Column(db.Boolean,default=False)

    board_id = db.Column(db.Integer,db.ForeignKey("board.id"),nullable=False)
    author_id = db.Column(db.String(100),db.ForeignKey("front_user.id"),nullable=False)

    board = db.relationship('BoardModel',backref=backref('posts',cascade="all"))
    author = db.relationship("FrontUser",backref='posts')


class HighlightPostModel(db.Model):
    __tablename__='highlight_post'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
    create_time = db.Column(db.DateTime,default=datetime.now)

    post = db.relationship("PostModel",backref='highlight')


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    is_removed = db.Column(db.Boolean, default=False)

    post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
    author_id = db.Column(db.String(100), db.ForeignKey("front_user.id"), nullable=False)
    origin_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    post = db.relationship("PostModel",backref='comments')
    author = db.relationship("FrontUser", backref='comments')
    origin_comment = db.relationship('CommentModel', backref='replys', remote_side=[id])


class PostStarModel(db.Model):
    __tablename__ = 'post_star'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.String(100),db.ForeignKey('front_user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))

    author = db.relationship('FrontUser',backref='stars')
    post = db.relationship('PostModel',backref='stars')

