"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView

import xadmin
from apps.users.views import LoginView,LogoutView,SendSmsView,DynamicLoginView,RegisterView
from apps.organizations.views import OrgView
from apps.operations.views import IndexView
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from MxOnline.settings import MEDIA_ROOT
#from MxOnline.settings import STATIC_ROOT

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('captcha/',include('captcha.urls')),
    path('send_sms/',csrf_exempt(SendSmsView.as_view()),name='send_sms'),
    path('',IndexView.as_view(),name='index'),
    path('login/',LoginView.as_view(),name='login'),
    path('d_login/',DynamicLoginView.as_view(),name='d_login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/',RegisterView.as_view(),name='register'),

    #配置文件上传访问的url
    re_path(r'media/(?P<path>.*$)',serve,{"document_root":MEDIA_ROOT}),
    #re_path(r'static/(?P<path>.*$)',serve,{"document_root":STATIC_ROOT}),
    #课程机构
    path('org/',include('apps.organizations.urls')),
    #用户相关操作
    path('op/',include('apps.operations.urls')),
    #课程相关
    path('course/',include('apps.courses.urls')),
    path('users/',include('apps.users.urls')),

]
