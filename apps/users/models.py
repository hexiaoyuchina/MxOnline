from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserProfile(AbstractUser):
    GENDER_CHOICES =(
        ('male','男'),
        ('female','女')
    )
    nick_name=models.CharField(max_length=50,default='',verbose_name='昵称')
    birthday=models.DateField(null=True,blank=True,verbose_name='生日')
    gender=models.CharField(choices=GENDER_CHOICES,default='male',max_length=6,verbose_name='性别')
    address=models.CharField(max_length=100,default='',verbose_name='地址')
    mobile=models.CharField(max_length=11,unique=True,verbose_name='手机号')
    image=models.ImageField(upload_to='head_image/%Y/%m',default='head_image/default.jpg')
    class Meta:
        verbose_name='用户信息'
        verbose_name_plural=verbose_name
    def __str__(self):
        if self.nick_name:
            return self.nick_name
        return self.username
class BaseModle(models.Model):
    add_time=models.DateField(auto_now_add=True,default=datetime.now,verbose_name='创建时间')
    class Meta:#继承时不会生成表
        abstract=True







