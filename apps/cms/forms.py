from wtforms import StringField, IntegerField
from wtforms.validators import Email, InputRequired,Length,EqualTo
from ..forms import BaseForm
from utils import mycache
from wtforms import ValidationError
from flask import g

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20,message="请输入正确长度的密码！")])
    remember = IntegerField()


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message="请输入正确格式的旧密码！")])
    newpwd = StringField(validators=[Length(6,20,message="请输入正确格式的新密码！")])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message="两次请输入相同的密码！")])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱！')])
    captcha = StringField(validators=[Length(min=6,max=6,message='请输入正确长度的验证码！')])

    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = mycache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误！')

    def validate_email(self,field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError("请勿使用相同邮箱！")


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称！')])
    image_url = StringField(validators=[InputRequired(message="请输入轮播图图片链接！")])
    link_url = StringField(validators=[InputRequired(message="请输入轮播图跳转链接！")])
    priority = IntegerField(validators=[InputRequired(message="请输入轮播图优先级！")])


class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图的id！')])


class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称！')])


class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message="请输入板块id")])

class CMSBlackFrontUserForm(BaseForm):
    user_id = StringField(validators=[InputRequired(message=u'必须传入id！')])
    is_black = IntegerField(validators=[InputRequired(message=u'必须指定是否加入黑名单！')])