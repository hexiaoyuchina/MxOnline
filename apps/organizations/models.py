from django.db import models

from apps.users.models import BaseModle


class City(BaseModle):
    name=models.CharField(max_length=10,verbose_name='城市名称')
    desc=models.CharField(max_length=200,verbose_name='描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='城市'
        verbose_name_plural=verbose_name

# Create your models here.
class CourseOrg(BaseModle):
    name=models.CharField(max_length=200,verbose_name='机构名称')
    desc=models.TextField(verbose_name='机构描述')
    tag=models.CharField(default='全国知名',max_length=100,verbose_name='机构标签')
    category=models.CharField(choices=(('pxjg','培训机构'),('gr','个人'),('gx','高校')),max_length=4,verbose_name='类别')
    click_nums=models.PositiveIntegerField(default=0,verbose_name='点击数')
    fav_nums=models.PositiveIntegerField(default=0,verbose_name='收藏数')
    log=models.ImageField(upload_to='org/%Y/%m',max_length=100,verbose_name='logo')
    address=models.CharField(max_length=150,verbose_name='地址')
    students=models.PositiveIntegerField(default=0,verbose_name='学习人数')
    course_nums=models.PositiveIntegerField(default=0,verbose_name='课程数')
    city=models.ForeignKey(City,on_delete=models.CASCADE,verbose_name='所在城市')
    is_auth=models.BooleanField(default=False,verbose_name='是否认证')
    is_gold = models.BooleanField(default=False, verbose_name='是否金牌')
    def courses(self):
        # from apps.courses.models import Course
        # Course.objects.filter(course_org=self)
        #模型名称_set，course中定义course_org的外键，使用course_set反向取course
        courses=self.course_set.filter(is_classic=True)[:3]
        return courses


    def __str__(self):
        return self.name

    class Meta:
        verbose_name='课程机构'
        verbose_name_plural=verbose_name

#from apps.operations import models


class Teacher(BaseModle):

    #user=models.OneToOneField(UserProfile,null=True,on_delete=models.SET_NULL,verbose_name="用户")

    org=models.ForeignKey(CourseOrg,on_delete=models.CASCADE,verbose_name='所属机构')
    name=models.CharField(max_length=50,verbose_name='教师名')
    work_years=models.PositiveIntegerField(default=0,verbose_name='工作年限')
    work_company=models.CharField(max_length=50,verbose_name='就职公司')
    work_position=models.CharField(max_length=50,verbose_name='公司职位')
    points=models.CharField(max_length=50,verbose_name='教学特点')
    click_nums=models.PositiveIntegerField(default=0,verbose_name='点击数')
    fav_nums=models.PositiveIntegerField(default=0,verbose_name='收藏数')
    age=models.PositiveIntegerField(default=18,verbose_name='年龄')
    image=models.ImageField(upload_to='teacher/%Y/%m',max_length=100,verbose_name='头像')

    def count_nums(self):
        return self.course_set.count()
    def __str__(self):
        return self.name

    class Meta:
        verbose_name='教师信息'
        verbose_name_plural=verbose_name