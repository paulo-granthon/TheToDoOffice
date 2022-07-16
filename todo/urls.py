from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete
from .views import TaskCreateFast

urlpatterns = [

    # task list
    path('', TaskList.as_view(), name='tasks'),

    # url that sends a new task with title only to the database
    path('new-task-fast/', TaskCreateFast, name='new-task-fast'),

    # creates a view to add a new task with title and description
    path('new/', TaskCreate.as_view(), name='new'),

    # c(RUD) - request, update and delete views
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('edit/<int:pk>/', TaskUpdate.as_view(), name='edit'),
    path('del/<int:pk>/', TaskDelete.as_view(), name='del'),

    # path('', views.index, name='index'),
    # path('add', views.add_todo, name='add'),
    # path('complete/<todo_id>', views.complete_todo, name='complete'),
    # path('delete_completed', views.delete_completed, name='delete_completed'),
    # path('delete_all', views.delete_all, name='delete_all')
]
