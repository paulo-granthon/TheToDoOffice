from django.urls import path
from . import views

urlpatterns = [

    # task list
    path('', views.Index.as_view(), name='index'),
    path('tasks/', views.TaskList.as_view(), name='tasks'),

    # url that sends a new task with title only to the database
    # path('new-task-fast/', TaskCreateFast, name='new-task-fast'),

    # creates a view to add a new task with title and description
    path('new/', views.TaskCreate.as_view(), name='new'),

    # c(RUD) - request, update and delete views
    path('task/<int:pk>/', views.TaskDetail.as_view(), name='task'),
    path('edit/<int:pk>/', views.TaskUpdate.as_view(), name='edit'),
    path('del/<int:pk>/', views.TaskDelete.as_view(), name='del'),

]

htmx_urlpatterns = [
    path('new-task-fast/', views.TaskCreateFast, name='new-task-fast'),
]

urlpatterns += htmx_urlpatterns
