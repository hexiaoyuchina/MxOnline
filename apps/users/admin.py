from django.contrib import admin
#用户信息通过这个绑定，admin创建的用户的密码才能使用刚登陆
from django.contrib.auth.admin import UserAdmin

from apps.users.models import UserProfile
# Register your models here.
class UserProFileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile,UserAdmin)