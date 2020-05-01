from django import forms
from captcha.fields import CaptchaField
import redis
from MxOnline.settings import REDIS_HOST,REDIS_PORT
class LoginForm(forms.Form):
    username=forms.CharField(required=True,min_length=2)
    password=forms.CharField(required=True,min_length=2)
class DynamicLoginForm(forms.Form):
    #图片验证码
    mobile=forms.CharField(min_length=11,max_length=11,required=True)
    captcha=CaptchaField()
class DynamicLoginPostForm(forms.Form):
    #手机验证码登录
    mobile = forms.CharField(min_length=11, max_length=11, required=True)
    code=forms.CharField(min_length=4,max_length=4,required=True)

    def clean_code(self):
        #只验证某个字段，先于clean执行，而cleaned_data的使用必须先clean执行后
        mobile = self.data.get('mobile')
        code = self.data.get('code')
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError('验证码错误')
        return self.changed_data

