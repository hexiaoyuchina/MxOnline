
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from apps.users.views import UserInfoView,UploadImageView,ChangePwdView,ChangeMobileView,MyCourseView,MyFavOrgView,MyFavTeaView,MyFavCourseView,MyMessageView
app_name='users'

urlpatterns=[
    path('info/',UserInfoView.as_view(),name='info'),
    path('image/upload/',UploadImageView.as_view(),name='image'),
    path('update/pwd/',ChangePwdView.as_view(),name='update'),
    path('update/mobile/',ChangeMobileView.as_view(),name='update_mobile'),
    #path('mycourse/',MyCourseView.as_view(),name='mycourse')#只有get方法，写 一个视图函数，或者直接使用下面的方式
    path('mycourse/',login_required(TemplateView.as_view(template_name="usercenter-mycourse.html"),login_url="/login/"),{"current_page":"mycourse"},name='mycourse'),
    path('myfavorg/',MyFavOrgView.as_view(),name='myfavorg'),
    path('myfavtea/',MyFavTeaView.as_view(),name='myfavtea'),
    path('myfavcour/',MyFavCourseView.as_view(),name='myfavcour'),
    path('messages/',MyMessageView.as_view(),name='messages'),

]