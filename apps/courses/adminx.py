import xadmin
from apps.courses.models import Course,Lesson,Video,CourseResource
class GlobalSettings(object):
    site_title='后台管理系统'#系统标题
    site_footer='何笑语创建'#页面最后@的内容
    # menu_style='accordion'#后台样式

class CourseAdmin(object):
    list_display = ['name', 'desc','detail','degree','learn_time','students']
    search_fields = ['name', 'desc','detail','degree','students']
    list_filter = ['name', 'desc','detail','degree','learn_time','students']
    list_editable = ['degree', 'desc']

class LessonAdmin(object):
    list_display=['course','name','add_time']
    search_fields=['course','name']
    list_filter=['course__name','name','add_time']

class VideoAdmin(object):
    list_display=['lesson','name','add_time']
    search_fields=['lesson','name']
    list_filter=['lesson','name','add_time']

class CourseResourceAdmin(object):
    list_display=['course','name','download','add_time']
    search_fields=['course','name','download']
xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
xadmin.site.register(xadmin.views.CommAdminView,GlobalSettings)