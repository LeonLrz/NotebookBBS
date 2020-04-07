from flask import Blueprint, request,make_response,jsonify
from utils import alidayu
from utils import restful,mycache
from .forms import SMSCaptchaForm
from utils.captcha import Captcha
from io import BytesIO
import qiniu
import config


bp = Blueprint("common",__name__,url_prefix="/c")

# 加密混淆前
# @bp.route('/sms_captcha/')
# def sms_captcha():
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message="请传入手机号码！")
#
#     captcha = Captcha.gene_text(4)
#     if alidayu.send_sms(telephone,code=captcha):
#         return restful.success()
#     else:
#         return restful.params_error(message="短信验证码发送失败！")
#     # 暂未实现阿里大于接口 使用1234作为验证码
#     # captcha = '1234'
#     # return restful.success()


@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    # telephone
    # timestamp
    # md5(ts+telephone+salt)
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        # 暂未实现阿里大于接口 使用1234作为验证码
        # captcha = Captcha.gene_text(4)
        # if alidayu.send_sms(telephone,code=captcha):
        #     return restful.success()
        # else:
        #     return restful.params_error(message="短信验证码发送失败！")
        captcha = Captcha.gene_text(4)
        print("发送的验证码是：%s"%captcha)
        mycache.set(telephone, captcha.lower())
        return restful.success()
    else:
        return restful.params_error(message='参数错误！')


@bp.route('/captcha/')
def graph_captcha():
    #获取验证码
    text,image = Captcha.gene_graph_captcha()
    mycache.set(text.lower(),text.lower())
    # BytesIO,字节流
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/uptoken/')
def uptoken():
    access_key = config.QINIU_ACCESS_KEY
    secret_key = config.QINIU_SECRET_KEY
    q = qiniu.Auth(access_key,secret_key)

    bucket = config.QINIU_BUCKET_NAME
    token = q.upload_token(bucket)
    return jsonify({'uptoken':token})

