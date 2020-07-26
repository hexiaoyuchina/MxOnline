
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.views.generic.base import View
from django.contrib.auth import authenticate,login,logout
from apps.users.forms import LoginForm,DynamicLoginForm,DynamicLoginPostForm,RegisterGetForm,RegisterPostForm,ImageUploadForm,UserInfoForm,ChangePwdForm,UpdateMobileForm
from apps.utils.YunPian import send_single_sms
from MxOnline.settings import yunpian_apikey,REDIS_HOST,REDIS_PORT
from apps.utils.random_str import generate_random
from apps.users.models import UserProfile
from apps.operations.models import UserCourse,UserFavorite,UserMessage
from apps.organizations.models import CourseOrg,Teacher
from apps.courses.models import Course
from pure_pagination import Paginator, PageNotAnInteger
from apps.operations.models import Banner
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
import redis
# Create your views here.
class CustomAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def message_nums(request):
    #配置全局变量，在seetingde TEMPLATES
    if request.user.is_authenticated:
        return {
            'unread_nums':request.user.usermessage_set.filter(has_read=False).count()
        }
    else:
        return {}

class MyMessageView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        messages=UserMessage.objects.filter(user=request.user)
        current_page = 'message'
        for mesage in messages:
            mesage.has_read=True
            mesage.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对课程机构进行分页
        p = Paginator(messages, per_page=1, request=request)

        messages = p.page(page)

        context={
            'messages':messages,
            'current_page':current_page
        }
        return render(request,'usercenter-message.html',context)

class MyFavCourseView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        cour_list =[]
        current_page='myfavcour'

        fav_cours=UserFavorite.objects.filter(user=request.user,fav_type=1)

        for fav_cour in fav_cours:
            cour=Course.objects.get(id=fav_cour.fav_id)
            cour_list.append(cour)

        context={
            'cour_list':cour_list,
            'current_page':current_page
        }

        return render(request,'usercenter-fav-course.html',context)

class MyFavTeaView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        tea_list =[]
        current_page='myfavtea'

        fav_teas=UserFavorite.objects.filter(user=request.user,fav_type=3)

        for fav_tea in fav_teas:
            tea=Teacher.objects.get(id=fav_tea.fav_id)
            tea_list.append(tea)

        context={
            'tea_list':tea_list,
            'current_page':current_page
        }

        return render(request,'usercenter-fav-teacher.html',context)


class MyFavOrgView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        org_list =[]

        current_page='myfavorg'
        fav_orgs=UserFavorite.objects.filter(user=request.user,fav_type=2)

        for fav_org in fav_orgs:
            org=CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)

        context={
            'org_list':org_list,
            'current_page':current_page
        }

        return render(request,'usercenter-fav-org.html',context)

class MyCourseView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        current_page='mycourse'
        mycourses=UserCourse.objects.filter(user=request.user)
        context={
            'mycourses':mycourses,
            'current_page':current_page
        }
        return render(request,'usercenter-mycourse.html',context)

class ChangeMobileView(LoginRequiredMixin,View):
    login_url = '/login/'
    def post(self,request,*args,**kwargs):
        mobile_forms=UpdateMobileForm(request.POST)

        if mobile_forms.is_valid():
            mobile=mobile_forms.cleaned_data['mobile']
            #已经存在的数据不能重复注册
            if UserProfile.objects.filter(mobile=mobile):
                return JsonResponse({'mobile':'该手机手机号已被占用'})
            user=request.user
            user.mobile=mobile
            user.username=mobile
            user.save()
            # login(request)
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse(mobile_forms.errors)

class ChangePwdView(View):
    def post(self,request,*args,**kwargs):
        pwd_form=ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1=request.POST.get('password1','')
            # pwd2=request.POST.get('password2','')
            # if pwd1!=pwd2:
            #     return JsonResponse({'status':'fail','msg':'密码不一致'})
            user=request.user
            user.set_password(pwd1)
            user.save()
            #修改成功后自动登录，不跳转到登录界面
            login(request,user)
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse(pwd_form.errors)

class UploadImageView(LoginRequiredMixin,View):
    # def save_file(self,file):
    #     with open("D:/LearningCode/Django_code/MxOnline/media/head_image/uploaded.jpg",'wb') as f:
    #         for chunk in file.chunks():
    #             f.write(chunk)

    def post(self,request,*args,**kwargs):
        login_url = "/login/"
        #request.POST只保存非文件类型的字段，为了传递image，加上参数request,指定哪个实例
        img_form=ImageUploadForm(request.POST,request.FILES,instance=request.user)
        if img_form.is_valid():
            img_form.save()
            return JsonResponse({
                'status': "success"
            })
        else:
            return JsonResponse({
                'status':"fail"
            })

        #处理用户上传头像
        # files=request.FILES['image']
        # self.save_file(files)
        # pass

class UserInfoView(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,request,*args,**kwargs):
        captcha_form=RegisterPostForm()
        current_page='info'
        context={
            'captcha_form':captcha_form,
            'current_page':current_page
        }
        return render(request,'usercenter-info.html',context)

    def post(self,request,*args,**kwargs):
        user_info_form=UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse(user_info_form.errors)


class RegisterView(View):
    def get(self,request,*args,**kwargs):
        register_get_form=RegisterGetForm()
        context={'register_get_form':register_get_form}
        return render(request,'register.html',context=context)

    def post(self,request,*args,**kwargs):
        dynamic_login = True
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data['mobile']
            password = register_post_form.cleaned_data['password']
            # 新建用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            # 验证码错误
            register_get_form=RegisterGetForm()
            context={'register_get_form':register_get_form,'register_post_form':register_post_form}
            return render(request, 'register.html', context=context)

class DynamicLoginView(View):
    def get(self,request,*args,**kwargs):
        banners = Banner.objects.all()[:3]
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        next = request.GET.get("next", '')
        login_form=DynamicLoginForm()
        context={
            'login_form':login_form,
            'next':next,
            'banners':banners
                 }
        return render(request,'login.html',context=context)
    #手机动态登录
    def post(self,request,*args,**kwargs):
        dynamic_login=True
        banners = Banner.objects.all()[:3]
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
            next = request.GET.get("next", '')
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse('index'))
        else:
            # 验证码错误
            d_form=DynamicLoginForm()
            context = {'login_form': login_form,'dynamic_login':dynamic_login,'d_form':d_form,
            'banners':banners}
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
        banners=Banner.objects.all()[:3]
        next = request.GET.get("next", '')
        login_form=DynamicLoginForm()
        context={
            'login_form':login_form,
            'next':next,
            'banners':banners
                 }
        return render(request,'login.html',context=context)
    def post(self,request,*args,**kwargs):
        login_form=LoginForm(request.POST)
        banners = Banner.objects.all()[:3]
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
                next=request.GET.get("next",'')
                if next:
                    return HttpResponseRedirect(next)
                #登录成功后跳转页面
                return HttpResponseRedirect(reverse('index'))
            else:

                context = {'msg': '用户名或密码错误','login_form':login_form,
            'banners':banners}
                return render(request, 'login.html', context=context)
        else:
            #未查询到用户
            context={'login_form':login_form,
            'banners':banners}
            return render(request,'login.html',context=context)


