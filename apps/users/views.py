from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.views.generic.base import View
from django.contrib.auth import authenticate,login,logout
from apps.users.forms import LoginForm,DynamicLoginForm,DynamicLoginPostForm
from apps.utils.YunPian import send_single_sms
from MxOnline.settings import yunpian_apikey,REDIS_HOST,REDIS_PORT
from apps.utils.random_str import generate_random
from apps.users.models import UserProfile
import redis
# Create your views here.
class DynamicLoginView(View):
    #手机动态登录
    def post(self,request,*args,**kwargs):
        dynamic_login=True
        #验证手机号及手机验证码
        login_form=DynamicLoginPostForm(request.POST)
        if login_form.is_valid():
            #没有注册仍然可以使用
            mobile=login_form.cleaned_data['mobile']
            code=login_form.changed_data['code']

            existed_user=UserProfile.objects.filter(mobile=mobile)
            if existed_user:
                user=existed_user[0]
            else:
                #新建用户
                user=UserProfile(username=mobile)
                password = generate_random(10, 2)
                user.set_password(password)
                user.mobile=mobile
                user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            # 验证码错误
            d_form=DynamicLoginForm()
            context = {'login_form': login_form,'dynamic_login':dynamic_login,'d_form':d_form}
            return render(request, 'login.html', context=context)

class SendSmsView(View):
    def post(self,request,*args,**kwargs):
        #验证手机号及图片验证码
        send_sms_form=DynamicLoginForm(request.POST)
        re_dict={}
        if send_sms_form.is_valid():
            mobile=send_sms_form.cleaned_data['mobile']
            #随机生成验证码
            code=generate_random(4,0)
            #调用云片网接口发送短信，传递apikey,验证码，手机号
            res_json=send_single_sms(yunpian_apikey,code,mobile=mobile)
            if res_json['code']==0:#发送成功，将该手机号的验证码存入redis
                re_dict['status']='success'
                r=redis.Redis(host=REDIS_HOST,port=REDIS_PORT,db=0,charset='utf8',decode_responses=True)
                r.set(str(mobile),code)
                r.expire(str(mobile),5*60)#五分钟过期
            else:#发送失败
                re_dict['msg']=res_json['msg']
        else:
            for key,value in send_sms_form.errors.items():
                re_dict[key]=value[0]
        return JsonResponse(re_dict)


class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('login'))

class LoginView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        login_form=DynamicLoginForm()
        context={'login_form':login_form}
        return render(request,'login.html',context=context)
    def post(self,request,*args,**kwargs):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            # username=request.POST.get('username','')
            # password=request.POST.get('password','')
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            # if not username:
            #     context={'msg':'请输入用户名'}
            #     return render(request,'login.html',context=context)
            # if not password:
            #     context = {'msg': '请输入密码'}
            #     return render(request, 'login.html', context=context)
            # if len(password)<3:
            #     context = {'msg': '输入密码格式不正确'}
            #     return render(request, 'login.html', context=context)
            #表单验证

            #通过用户名和密码查询用户是否存在
            user=authenticate(username=username,password=password)
            #1.通过用户名查询用户2.需要先加密通过加 密后的代码查询
            # user=UserProfie.objects.get(username=username,password=password)
            if user is not None:
                #登录用户
                login(request,user)
                #登录成功后跳转页面
                return HttpResponseRedirect(reverse('index'))
            else:

                context = {'msg': '用户名或密码错误','login_form':login_form}
                return render(request, 'login.html', context=context)
        else:
            #未查询到用户
            context={'login_form':login_form}
            return render(request,'login.html',context=context)


