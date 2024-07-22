from django.contrib import admin
from django.urls import path
from TaskList.views import TaskListView, TypeListView, edit, delete, notice,add,finish,allList,addplate


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TaskListView.as_view(), name='list'),
    path('allList/', allList.as_view(), name='allList'),
    path('type/', TypeListView.as_view(), name='type'),
    path('edit/<int:tid>/', edit.as_view(), name='edit'),
    path('delete/<int:tid>/', delete.as_view(), name='delete'),
    path('notice/', notice.as_view(), name='notice'),
    path('add/<int:tpid>', add.as_view(), name='add'),
    path('finish/<int:tid>', finish.as_view(), name='finish'),
    path('addplate/', addplate.as_view(), name='addplate'),

]
