from django.contrib import admin
from TaskList.models import Plate, Type, Task


class PlateAdmin(admin.ModelAdmin):
    list_display = ('name', 'dutyUser')
    fields = ('name', 'dutyUser')


class TypeAdmin(admin.ModelAdmin):
    list_display = ('plate', 'name', 'doUser')


class TaskAdmin(admin.ModelAdmin):
    fields = ['type', 'name', 'end_time', ]
    list_display = ('type', 'name', 'end_time', 'finish_time', 'status')


admin.site.register(Task, TaskAdmin)
admin.site.register(Plate, PlateAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.site_header = '任务管理系统'
admin.site.index_title = '任务后台管理'
admin.site.site_title = '任务管理'