from apps.forms import BaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import Regexp
import hashlib
salt = 'suibiangei!@#$asdzx132%'


class SMSCaptchaForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[Regexp(r'\d{13}')])
    sign = StringField(validators=[IntegerField()])

    def validate(self):
        # result = super(SMSCaptchaForm, self).validate()
        # if not result:
        #     return False
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data


        # md5(timestamp+telephone+salt)
        # md5函数必须穿一个bytes类型的字符串进去
        sign2 = hashlib.md5((timestamp+telephone+salt).encode('utf-8')).hexdigest()
        if sign == sign2:
            return True
        else:
            return False


