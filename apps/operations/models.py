from django.db import models
from django.contrib.auth import get_user_model
from apps.users.models import BaseModle
from apps.courses.models import Course

UserProfile = get_user_model()


# Create your models here.
class UserAsk(BaseModle):
    name = models.CharField(max_length=20, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    course_name = models.CharField(max_length=50, verbose_name='课程名')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


class CoureseComment(BaseModle):
    # 用户的关联使用get_user_model,不直接使用UserProfile类，因为如果后期更改，和这个相关联的字段都需要更改
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    comments = models.CharField(max_length=200, verbose_name='评论内容')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class UserFavoriate(BaseModle):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    # 收藏类型不使用外键关联，使用如下类型，增加或减少字段无须修改表结构
    fav_id = models.IntegerField(verbose_name='数据id')
    fav_type = models.IntegerField(choices=((1, '课程'), (2, '课程机构'), (3, '讲师')), default=1, verbose_name='收藏类型')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(BaseModle):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    message = models.CharField(max_length=200, verbose_name='消息内容')
    has_read = models.BooleanField(default=False, verbose_name='消息是否已读')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class UserCourse(BaseModle):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name
