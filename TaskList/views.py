import datetime
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from TaskList.forms import Task_with_type_ModelForm, Task_with_all_ModelForm, Type_ModelForm, form_Notice,plate_ModelForm
import re
from TaskList.models import Task, Type, Plate


class allList(View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.order_by('-add_time')
        return render(request, 'allList.html', locals())


class TaskListView(View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.order_by('-add_time').filter(status=0)
        form = Task_with_type_ModelForm()
        return render(request, "list.html", locals())

    def post(self, request, *args, **kwargs):
        form = Task_with_type_ModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "任务创建成功!")
            return redirect('list')
        else:
            messages.error(request, "表单验证失败,请检查输入。")
            return render(request, 'list.html', {'form': form})


class TypeListView(View):
    def get(self, request):
        Plates = Plate.objects.all()
        form = Type_ModelForm()
        return render(request, "type.html", locals())

    def post(self, request, *args, **kwargs):
        form = Type_ModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('type')


class edit(View):
    def get(self, request, tid, *args, **kwargs):
        task = Task.objects.get(id=tid)
        form = Task_with_all_ModelForm(instance=task)
        return render(request, "edit.html", locals())

    def post(self, request, tid, *args, **kwargs):
        task = Task.objects.get(id=tid)
        form = Task_with_all_ModelForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "修改成功!")
            return redirect('list')
        else:
            messages.error(request, "表单验证失败,请检查输入。")
            return render(request, 'edit.html', {'form': form})


class delete(View):
    def get(self, request, tid, *args, **kwargs):
        task = Task.objects.get(id=tid)
        task.delete()
        return redirect('list')



class notice(View):
    def get(self, request, *args, **kwargs):
        form = form_Notice()
        return render(request, 'notice.html', locals())

    def post(self, request, *args, **kwargs):
        form = form_Notice(request.POST)
        if form.is_valid():
            # 获取前端填入的数据
            text = form.cleaned_data['text']
            # 填充--类型
            plate = re.findall(r'【(.*?)】', text)[0]
            # 填充--任务名
            task = re.findall(r"】(\w+) {2}", text)[0]
            # 填充时间---re.findall返回的事列表，所以要取第一个
            end_time_str1 = re.findall(r"\d{4}年\d{1,2}月\d{1,2}日", text)[0]  # 2024年7月17日
            end_time_str2 = re.findall(r"\d+", end_time_str1)
            year, month, day = map(int, end_time_str2)
            end_time = datetime.datetime(year, month, day, 17, 30, 0)
            try:
                type = Plate.objects.filter(name=plate)[0].type_set.first()
                task = Task(type=type, name=task, end_time=end_time,wx_notice_from=text)
                task.save()
                return redirect('list')
            except IndexError:
                # 处理 type_set 为空的情况
                return render(request, 'not_found_to_add.html', locals())
            except Plate.DoesNotExist:
                # 处理 Plate 对象不存在的情况
                return render(request, 'not_found_to_add.html', locals())
            except IntegrityError:
                # 处理 Plate 对象不存在的情况
                return render(request, 'not_found_to_add.html', locals())

        else:
            messages.error(request, "操作失败")
            return render(request, 'notice.html', locals())


class add(View):
    def get(self, request, tpid, *args, **kwargs):
        type = Type.objects.get(id=tpid)
        now = datetime.datetime.now()
        one_day_later = now + datetime.timedelta(days=1)
        task = Task(type=type, name=type.name, end_time=one_day_later)
        task.save()
        return redirect('list')


# 点击完成的操作
class finish(View):
    def get(self, request, tid, *args, **kwargs):
        task = Task.objects.get(id=tid)
        task.status = True
        task.save()
        return redirect('list')


class addplate(View):
    def get(self, request, *args, **kwargs):
        plates = Plate.objects.all()
        form = plate_ModelForm()
        return render(request, 'addplate.html', locals())
    def post(self, request, *args, **kwargs):
        form = plate_ModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addplate')
        return redirect('addplate')