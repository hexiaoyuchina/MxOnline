from django.urls import path
from apps.organizations.views import OrgView,AddAskView,OrgHomeView,OrgTeacherView,OrgCourseView,OrgDescView,TeacherView
app_name='org'
urlpatterns = [
#机构相关也main
    path('list/',OrgView.as_view(),name='list'),
    path('add_ask/',AddAskView.as_view(),name='add_ask'),
    path('<int:org_id>/',OrgHomeView.as_view(),name='home'),
    path('<int:org_id>/teacher/',OrgTeacherView.as_view(),name='teacher'),
    path('<int:org_id>/course/',OrgCourseView.as_view(),name='course'),
    path('<int:org_id>/desc/',OrgDescView.as_view(),name='desc'),
    path('teachers/',TeacherView.as_view(),name='teachers'),
]