import xadmin
from apps.courses.models import Course,Lesson,Video,CourseResource,CourseTag
from apps.operations.models import Banner
from xadmin.layout import Fieldset, Side, Row, FormHelper, Main


class GlobalSettings(object):
    site_title='后台管理系统'#系统标题
    site_footer='何笑语创建'#页面最后@的内容
    # menu_style='accordion'#后台样式

class CourseAdmin(object):
    list_display = ['name', 'desc','detail','degree','learn_time','students']
    search_fields = ['name', 'desc','detail','degree','students']
    list_filter = ['name', 'desc','detail','degree','learn_time','students']
    list_editable = ['degree', 'desc']

class NewCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students']
    list_editable = ['degree', 'desc']
    ordering=['click_nums']#排序
    readonly_fields=['students','add_time']#只读
    #富文本设置  
    style_fields = {
        "detail": "ueditor"
    }
    # def queryset(self):
    #     qs=super.queryset()
    #     if not self.request.user.is_supperuser:
    #         qs=qs.filter(teacher=self.request.user)
    #     return qs

    #页面布局设置，mian,side,fielset,row,return super
    def get_form_layout(self):
        if self.org_obj:#判断语句，只有编辑界面，布局设置才生效

            self.form_layout=(
                Main(
                    Fieldset('讲师信息',
                             'teacher','course_org',
                             css_class='unsort no_title'

                             ),
                    Fieldset('基本信息',
                             'name', 'desc',
                             Row('learn_time','degree'),
                             Row('category','tag'),
                             'youneed_know','teacher_tell','detail',

                             ),
                ),
                Side(
                Fieldset("访问信息",
                         'fav_nums','click_nums','students','add_time'
                         )
            ),
                Side(
                    Fieldset("选择信息",
                             'is_banner','is_classic'
                             )
                )

            )
        return super(NewCourseAdmin, self).get_form_layout()


class LessonAdmin(object):
    list_display=['course','name','add_time']
    search_fields=['course','name']
    list_filter=['course__name','name','add_time']

class VideoAdmin(object):
    list_display=['lesson','name','add_time']
    search_fields=['lesson','name']
    list_filter=['lesson','name','add_time']

class CourseResourceAdmin(object):
    list_display=['course','name','file','add_time']
    search_fields=['course','name','file']
    list_filter=['course', 'name', 'file', 'add_time']

class CourseTagAdmin(object):
    list_display = ['course', 'tag','add_time']
    search_fields = ['course', 'tag']
    list_filter =['course', 'tag','add_time']



#xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Course,NewCourseAdmin)

xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
xadmin.site.register(xadmin.views.CommAdminView,GlobalSettings)
xadmin.site.register(CourseTag,CourseTagAdmin)