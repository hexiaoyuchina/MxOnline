from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from apps.organizations.models import CourseOrg,Teacher,City
from pure_pagination import Paginator, PageNotAnInteger
from apps.organizations.forms import AddForm
from apps.operations.models import UserFavorite
class OrgHomeView(View):
    def get(self,request,org_id,*args,**kwargs):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        has_fav=False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav=True
        context = {
            'all_courses': all_courses,
            'all_teacher': all_teachers,
            'course_org': course_org,
            'current_page':current_page,
            'has_fav':has_fav
        }
        return render(request, 'org-detail-homepage.html', context)

class OrgTeacherView(View):
    def get(self,request,org_id,*args,**kwargs):
        current_page='teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()[:1]
        context = {
            'all_teacher': all_teachers,
            'course_org': course_org,
            'current_page':current_page,
            'has_fav':has_fav
        }
        return render(request, 'org-detail-teachers.html', context)

class OrgCourseView(View):
    def get(self,request,org_id,*args,**kwargs):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        #对课程机构进行分页
        p = Paginator(all_courses, per_page=5,request=request)

        all_courses = p.page(page)

        context = {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        }
        return render(request, 'org-detail-course.html', context)

class OrgDescView(View):
    def get(self,request,org_id,*args,**kwargs):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        context = {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        }
        return render(request, 'org-detail-desc.html', context)

class AddAskView(View):
    def post(self,request,*args,**kwargs):
        userask_form=AddForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'fail','msg':'添加出错'})


# Create your views here.
class OrgView(View):
    def get(self, request, *args, **kwargs):
        #从数据库中获取数据
        org_nums=CourseOrg.objects.count()
        all_orgs=CourseOrg.objects.all()
        all_cities=City.objects.all()
        hot_orgs=all_orgs.order_by('-click_nums')[:3]
        #对课程机构筛选
        category=request.GET.get('ct','')
        if category:
            all_orgs=all_orgs.filter(category=category)
        #通过城市筛选
        city_id=request.GET.get('city','')
        if city_id:
            #存储外键是存储的city_id(定义的字段+外键的主键)
            if city_id.isdigit():
                all_orgs=all_orgs.filter(city_id=int(city_id))
        #对机构进行排序
        sort=request.GET.get('sort','')
        if sort=='students':
            all_orgs=all_orgs.order_by('-students')
        elif sort=='courses':
            all_orgs=all_orgs.order_by('-course_nums')

        org_nums =all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        #对课程机构进行分页
        p = Paginator(all_orgs, per_page=5,request=request)

        orgs = p.page(page)
        context={
            'all_orgs':orgs,
            'org_nums':org_nums,
            'all_cities':all_cities,
            'category':category,
            'cityid':city_id,
            'sort':sort,
            'hot_orgs':hot_orgs,
        }
        return render(request, 'org-list.html',context)

class TeacherListView(View):
    def get(self, request, *args, **kwargs):
        # 从数据库中获取数据


        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()
        hot_teachers=Teacher.objects.all().order_by('-click_nums')[:3]
        # 对机构进行排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对课程机构进行分页
        p = Paginator(all_teachers, per_page=1, request=request)

        all_teachers = p.page(page)
        context = {
            'all_teachers':all_teachers,
            'teacher_nums':teacher_nums,
            'sort':sort,
            'hot_teachers':hot_teachers
        }

        return render(request, 'teachers-list.html', context)

class TeacherDetailView(View):
    def get(self, request,teacher_id, *args, **kwargs):
        teacher=Teacher.objects.get(id=int(teacher_id))
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        teacher_has_fav=False
        org_has_fav=False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
                teacher_has_fav=True
            if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=teacher.org.id):
                org_has_fav=True
        context={
            'teacher':teacher,
            'teacher_has_fav':teacher_has_fav,
            'org_has_fav':org_has_fav,
            'hot_teachers':hot_teachers
        }

        return render(request,'teacher-detail.html',context)