from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.courses.models import Course,CourseTag,CourseResource,Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from apps.operations.models import UserFavorite,UserCourse,CourseComments

# Create your views here.
class CourseListView(View):
    def get(self,request,*args,**kwargs):
        '''获取课程列表'''
        all_courses=Course.objects.order_by('-add_time')
        hot_courses=Course.objects.order_by('-click_nums')[:3]
        sort=request.GET.get('sort')
        if sort=='students':
            all_courses=all_courses.order_by('-students')
        elif sort=='hot':
            all_courses=all_courses.order_by('-click_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对课程机构进行分页
        p = Paginator(all_courses, per_page=5, request=request)

        all_courses = p.page(page)
        context={
            'all_courses':all_courses,
            'sort':sort,
            'hot_courses':hot_courses
        }
        return render(request,'course-list.html',context)

class CourseDetailView(View):
    def get(self,request,course_id,*args,**kwargs):
        course=Course.objects.get(id=int(course_id))
        course.click_nums+=1
        course.save()
        has_fav_course=False
        has_fav_org=False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_id,fav_type=1):
                has_fav_course=True

            if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2):
                has_fav_org=True

        #通过课程tag找到同类推荐
        # tag=course.tag
        # relate_course=[]
        # if tag:
        #     relate_course=Course.objects.filter(tag=tag).exclude(id_in=[course.id])[:3]
        tags=course.coursetag_set.all()
        tag_list=[tag.tag for tag in tags]
        course_tags=CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)
        relate_course=set()
        for course_tag in course_tags:
            relate_course.add(
                course_tag.course
            )

        context={
            'course':course,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
            'relate_course':relate_course
        }

        return render(request,'course-detail.html',context)

class CourseLessonView(LoginRequiredMixin,View):
    # 用户登录验证使用django自带的LoginRequiredMixin类装饰器
    login_url = "/login/"
    def get(self,request,*args,course_id,**kwargs):
        #课程章节
        course=Course.objects.get(id=int(course_id))
        course.click_nums++1
        course.save()
        #用户与课程之间的关联
        user_course=UserCourse.objects.filter(user=request.user,course=course)
        if not user_course:
            user_course=UserCourse(user=request.user,course=course)
            user_course.save()
            course.students+=1
            course.save()

        #学习该课程的所有同学
        user_courses=UserCourse.objects.filter(course=course)
        user_ids=[user_course.user_id for user_course in user_courses]
        all_courses=UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')[:5]
        relate_courses=[user_course.course for user_course in all_courses if user_course.course_id!=course_id]

        #课程资料下载
        course_resourse=CourseResource.objects.filter(course=course)
        context={
            'course':course,
            'course_resource':course_resourse,
            'relate_courses':relate_courses
        }
        return render(request,'course-video.html',context)

class CourseCommentView(LoginRequiredMixin,View):
    # 用户登录验证使用django自带的LoginRequiredMixin类装饰器
    login_url = "/login/"

    def get(self, request, *args, course_id, **kwargs):
        # 课程章节
        course = Course.objects.get(id=int(course_id))
        course.click_nums + +1
        course.save()
        comments=CourseComments.objects.filter(course=course)

        # 用户与课程之间的关联
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        # 学习该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user_id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')[:5]
        relate_courses = [user_course.course for user_course in all_courses if user_course.course_id != course_id]

        # 课程资料下载
        course_resourse = CourseResource.objects.filter(course=course)
        context = {
            'course': course,
            'course_resource': course_resourse,
            'relate_courses': relate_courses,
            'comments':comments
        }
        return render(request,'course-comment.html',context)


class VieoView(LoginRequiredMixin,View):
    # 用户登录验证使用django自带的LoginRequiredMixin类装饰器
    login_url = "/login/"
    def get(self,request,*args,course_id,video_id,**kwargs):
        #课程章节
        course=Course.objects.get(id=int(course_id))
        course.click_nums++1
        course.save()
        #视频
        video=Video.objects.get(id=(int(video_id)))

        #用户与课程之间的关联
        user_course=UserCourse.objects.filter(user=request.user,course=course)
        if not user_course:
            user_course=UserCourse(user=request.user,course=course)
            user_course.save()
            course.students+=1
            course.save()

        #学习该课程的所有同学
        user_courses=UserCourse.objects.filter(course=course)
        user_ids=[user_course.user_id for user_course in user_courses]
        all_courses=UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')[:5]
        relate_courses=[user_course.course for user_course in all_courses if user_course.course_id!=course_id]

        #课程资料下载
        course_resourse=CourseResource.objects.filter(course=course)
        context={
            'course':course,
            'course_resource':course_resourse,
            'relate_courses':relate_courses,
            'video':video
        }
        return render(request,'course-play.html',context)