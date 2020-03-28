# 阿里大于短信验证码sdk
# import hashlib
# from time import time
# import logging
# import requests

# class AlidayuAPI(object):
#
#     APP_KEY_FIELD = 'ALIDAYU_APP_KEY'
#     APP_SECRET_FIELD = 'ALIDAYU_APP_SECRET'
#     SMS_SIGN_NAME_FIELD = 'ALIDAYU_SIGN_NAME'
#     SMS_TEMPLATE_CODE_FIELD = 'ALIDAYU_TEMPLATE_CODE'
#
#
#     def __init__(self, app=None):
#         self.url = 'https://eco.taobao.com/router/rest'
#         self.headers = {
#             'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
#             "Cache-Control": "no-cache",
#             "Connection": "Keep-Alive",
#         }
#         if app:
#             self.init_app(app)
#
#
#     def init_app(self,app):
#         config = app.config
#         try:
#             self.key = config[self.APP_KEY_FIELD]
#             self.secret = config[self.APP_SECRET_FIELD]
#             self.sign_name = config[self.SMS_SIGN_NAME_FIELD]
#             self.api_params = {
#                 'sms_free_sign_name': config[self.SMS_SIGN_NAME_FIELD],
#                 'sms_template_code': config[self.SMS_TEMPLATE_CODE_FIELD],
#                 'extend': '',
#                 'sms_type': "normal",
#                 "method": "alibaba.aliqin.fc.sms.num.send",
#                 "app_key": self.key,
#                 "format": "json",
#                 "v": "2.0",
#                 "partner_id": "",
#                 "sign_method": "md5",
#             }
#         except Exception as e:
#             logging.error(e.args)
#             raise ValueError('请填写正确的阿里大鱼配置！')
#
#
#     def send_sms(self,telephone,**params):
#         self.api_params['timestamp'] = str(int(time() * 1000))
#         self.api_params['sms_param'] = str(params)
#         self.api_params['rec_num'] = telephone
#
#         newparams = "".join(["%s%s" % (k, v) for k, v in sorted(self.api_params.items())])
#         newparams = self.secret + newparams + self.secret
#         sign = hashlib.md5(newparams.encode("utf-8")).hexdigest().upper()
#         self.api_params['sign'] = sign
#
#         resp = requests.post(self.url,params=self.api_params,headers=self.headers)
#         data = resp.json()
#         try:
#             result = data['alibaba_aliqin_fc_sms_num_send_response']['result']['success']
#             return result
#         except:
#             print('='*10)
#             print("阿里大于错误信息：",data)
#             print('='*10)
#             return False

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

#阿里大于相关配置
accessKeyId = 'LTAI4FcNN2hKFCERN3SThvhH'
accessSecret = 'tQCx4fFGwLowtCP5M00V5fS80YdT8R'
SignName = 'NotebookBBS'
TemplateCode = 'SMS_186576101'
REGION = 'cn-hangzhou'


def send_sms(telephone, code):
    client = AcsClient(accessKeyId, accessSecret, REGION)

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', REGION)
    request.add_query_param('PhoneNumbers', telephone)
    request.add_query_param('SignName', SignName)
    request.add_query_param('TemplateCode', TemplateCode)
    request.add_query_param('TemplateParam', code)

    try:
        response = client.do_action_with_exception(request)
        print(response)
        return True
    except Exception:
        print(Exception)
        return False


