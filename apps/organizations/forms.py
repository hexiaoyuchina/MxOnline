from django import forms
from apps.operations.models import UserAsk

class AddForm(forms.ModelForm):
    #model中只有max_length，无min_length,通过自定义来限制
    mobile=forms.CharField(max_length=11,min_length=11,required=True)
    class Meta:
        model=UserAsk
        fields=['name','mobile','course_name']
    def clean_mobile(self):
        mobile=self.cleaned_data['mobile']
        regex_mobile="^(13[0-9]|14[5|7]|15[0|1|2|3|4|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$"
        import re
        p=re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号非法',code='mobile_invalid')


