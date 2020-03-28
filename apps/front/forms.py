from wtforms import StringField,IntegerField,BooleanField
from ..forms import BaseForm
from wtforms.validators import Regexp,EqualTo,ValidationError,InputRequired,URL
from utils import mycache


class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}',message="请输入正确的手机号码！")])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}',message="请输入正确的短信验证码！")])
    username = StringField(validators=[Regexp(r".{2,20}",message="请输入2到20位长度的用户名！")])
    password1 = StringField(validators=[Regexp(r".{6,20}",message="请输入6到20位的密码！")])
    password2 = StringField(validators=[EqualTo("password1",message="两次输入的密码不一致！")])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}',message="请输入正确的图形验证码！")])

    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data
        mem = mycache.get(telephone)
        if not mem or mem.lower() != sms_captcha.lower():
            raise ValidationError(message='短信验证码错误！')
        # pass

    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        mem = mycache.get(graph_captcha.lower())
        if not mem:
            raise ValidationError(message='图形验证码错误！')
        # pass


class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}',message="请输入正确的手机号码！")])
    password = StringField(validators=[Regexp(r".{6,20}", message="请输入6到20位的密码！")])
    remember = StringField()


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message="请输入标题！")])
    content = StringField(validators=[InputRequired(message='请输入内容！')])
    board_id = IntegerField(validators=[InputRequired(message='请输入版块id!')])


class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message="请输入评论内容！")])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子id!')])

class StarPostForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'必须输入帖子id！')])
    is_star = BooleanField(validators=[InputRequired(message=u'必须输入赞的行为！')])

class SettingsForm(BaseForm):
    username = StringField(validators=[InputRequired(message=u'必须输入用户名！')])
    realname = StringField()
    qq = StringField()
    avatar = StringField(validators=[URL(message=u'头像格式不对！')])
    signature = StringField()