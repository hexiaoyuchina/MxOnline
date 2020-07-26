from datetime import datetime

from django.db import models
from apps.users.models import BaseModle
from apps.organizations.models import Teacher
from apps.organizations.models import CourseOrg

# Create your models here.
class Course(BaseModle):
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')

    learn_time = models.PositiveIntegerField(default=0, verbose_name='课时长(min)')
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')),max_length=4, verbose_name='难度')
    students = models.PositiveIntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.PositiveIntegerField(default=0, verbose_name='收藏数')
    click_nums = models.PositiveIntegerField(default=0, verbose_name='点击数')
    category = models.CharField(default=u'后端开发', max_length=20, verbose_name='课程种类')
    tag = models.CharField(default='', max_length=10, verbose_name='课程标签')
    youneed_know = models.CharField(default='', max_length=300, verbose_name='课程须知')
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name='讲师')
    course_org=models.ForeignKey(CourseOrg,null=True,blank=True,on_delete=models.CASCADE,verbose_name='课程机构')
    teacher_tell = models.CharField(default='', max_length=300, verbose_name='老师告诉你')
    notes=models.CharField(max_length=200,default='',verbose_name="课程公告")
    detail = models.TextField(verbose_name='副文本 ')
    is_classic=models.BooleanField(default=False,verbose_name='是否是经典课程')
    is_banner=models.BooleanField(default=False,verbose_name='是否是广告位')
    image = models.ImageField(upload_to='courese/%Y/%m', max_length=100, verbose_name='封面图')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name
    def lesson_nums(self):
        return self.lesson_set.all().count()

class CourseTag(BaseModle):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name='课程')
    tag=models.CharField(max_length=100,verbose_name='标签')
    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = '课程标签'
        verbose_name_plural = verbose_name

class Lesson(BaseModle):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='章节名')
    learn_time = models.PositiveIntegerField(default=0, verbose_name='学习时长（分钟)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '章节信息'
        verbose_name_plural = verbose_name


class Video(BaseModle):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名')
    learn_time = models.PositiveIntegerField(default=0, verbose_name='学习时长')
    url = models.URLField(max_length=200, verbose_name='访问地址')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name


class CourseResource(BaseModle):
    name = models.CharField(max_length=100, default='',verbose_name="名称")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    file = models.FileField(upload_to='course/resource/%Y/%m', max_length=200, verbose_name='下载地址')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
