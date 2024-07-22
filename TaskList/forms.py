from django import forms
from TaskList.models import *


class Task_with_type_ModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['type', 'name', 'end_time']
        widgets = {
            'end_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'step': '1'}
            )
        }


class Task_with_all_ModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['type', 'name', 'end_time', 'wx_notice_from', 'to_who', 'wx_notice_to', ]
        widgets = {
            'wx_notice_from': forms.TextInput(attrs={
                'class': 'form-control-wide',  # 应用自定义的 CSS 类
            }),
            'wx_notice_to': forms.TextInput(attrs={
                'class': 'form-control-wide',  # 应用自定义的 CSS 类
            }),
        }

class Type_ModelForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name', 'plate', 'doUser']


class form_Notice(forms.Form):
    text = forms.CharField(max_length=1000)


class plate_ModelForm(forms.ModelForm):
    class Meta:
        model = Plate
        fields = ['name', 'dutyUser']