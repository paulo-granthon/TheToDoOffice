from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate
from .views import TaskCreateFast

urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('new-task/', TaskCreate.as_view(), name='new-task'),
    # path('new-task-fast/', TaskCreateFast.as_view(), name='new-task-fast'),

    # path('', views.index, name='index'),
    # path('add', views.add_todo, name='add'),
    # path('complete/<todo_id>', views.complete_todo, name='complete'),
    # path('delete_completed', views.delete_completed, name='delete_completed'),
    # path('delete_all', views.delete_all, name='delete_all')
]
