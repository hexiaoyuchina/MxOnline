from django import forms
from captcha.fields import CaptchaField
import redis
from MxOnline.settings import REDIS_HOST,REDIS_PORT
from apps.users.models import UserProfile

class UpdateMobileForm(forms.Form):
    # 手机验证码登录
    mobile = forms.CharField(min_length=11, max_length=11, required=True)
    code = forms.CharField(min_length=4, max_length=4, required=True)
    def clean_mobile(self):
        mobile = self.data.get('mobile')
        # 验证手机号码是否已经注册
        user = UserProfile.objects.filter(
            mobile=mobile
        )
        if user:
            raise forms.ValidationError('手机号码已注册')
        return mobile

class ChangePwdForm(forms.Form):

    password1=forms.CharField(required=True,min_length=5)
    password2=forms.CharField(required=True,min_length=5)
    def clean(self):
        pwd1=self.cleaned_data['password1']
        pwd2=self.cleaned_data['password2']
        if pwd1!=pwd2:
            raise forms.ValidationError('密码不一致')
        return self.cleaned_data

class UserInfoForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["nick_name","gender",'birthday','address']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["image"]

class RegisterGetForm(forms.Form):
    captcha=CaptchaField()

class RegisterPostForm(forms.Form):
    # 手机验证码登录
    mobile = forms.CharField(min_length=11, max_length=11, required=True)
    code = forms.CharField(min_length=4, max_length=4, required=True)
    password=forms.CharField(required=True)
    def clean_mobile(self):
        mobile = self.data.get('mobile')
        # 验证手机号码是否已经注册
        user = UserProfile.objects.filter(
            mobile=mobile
        )
        if user:
            raise forms.ValidationError('手机号码已注册')
        return mobile

    def clean_code(self):
        # 只验证某个字段，先于clean执行，而cleaned_data的使用必须先clean执行后
        mobile = self.data.get('mobile')
        code = self.data.get('code')
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError('验证码错误')

        return code


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

