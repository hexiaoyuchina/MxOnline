from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from apps.operations.models import UserFavorite,CourseComments,Banner
from apps.operations.forms import UserFavForm,CommentForm
from apps.courses.models import Course
from apps.organizations.models import CourseOrg,Teacher
# Create your views here.
class IndexView(View):
    def get(self,request,*args,**kwargs):
        # from django.core.exceptions import PermissionDenied
        # raise PermissionDenied
        banners=Banner.objects.all().order_by('index')
        courses=Course.objects.filter(is_banner=False)[:6]
        banner_courses=Course.objects.filter(is_banner=True)
        course_orgs=CourseOrg.objects.all()[:15]
        context={
            'banners':banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs
        }

        return render(request,'index.html',context)

class AddFavView(View):
    def post(self, request, *args, **kwargs):
        """
        用户收藏，取消收藏
        """
        #先判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status":"fail",
                "msg":"用户未登录"
            })

        user_fav_form = UserFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]

            #是否已经收藏
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if existed_records:
                existed_records.delete()

                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "收藏"
                })
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })

class  CommentView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            context = {'status': 'fail', 'msg': '用户未登录'}
            return JsonResponse(context)

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            course = comment_form.cleaned_data['course']
            comments = comment_form.cleaned_data['comments']

            comment=CourseComments()
            comment.user=request.user
            comment.comments=comments



            comment.course=course
            comment.save()


            context = {'status': 'success'}
            return JsonResponse(context)

        else:
            context = {'status': 'fail', 'msg': '参数错误'}
            return JsonResponse(context)