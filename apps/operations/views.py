from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from apps.operations.models import UserFavorite
from apps.operations.forms import UserFavForm
from apps.courses.models import Course
from apps.organizations.models import CourseOrg,Teacher
# Create your views here.
class AddFavView(View):
    def post(self,request,*args,**kwargs):
        #用户收藏用户取消手收藏
        #用户登录
        if not request.user.is_authenticated:
            context = {'status': 'fail','msg':'用户未登录'}
            return JsonResponse(context)

        user_fav_form=UserFavForm(request.POST)

        if user_fav_form.is_valid():
            fav_id=user_fav_form.cleaned_data['fav_id']
            fav_type=user_fav_form.cleaned_data['fav_type']
            #是否已经收藏
            existed_records=UserFavorite.objects.filter(user=request.user,fav_id=fav_id,fav_type=fav_type)
            if existed_records:
                existed_records.delete()
                #相应选项收藏数减1
                if fav_type==1:
                    course=Course.objects.get(id=fav_id)
                    course.fav_nums-=1
                    course.save()
                elif fav_type==2:
                    course_org=CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums-=1
                    course_org.save()
                elif fav_type==3:
                    teacher=Teacher.objects.get(id=fav_id)
                    teacher.fav_nums-=1
                    teacher.save()

                context = {'status': 'success', 'msg': '收藏'}
                return JsonResponse(context)
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()
                context = {'status': 'success', 'msg': '已收藏'}
                return JsonResponse(context)
        else:
            context = {'status': 'fail', 'msg': '参数错误'}
            return JsonResponse(context)

