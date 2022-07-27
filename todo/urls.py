from django.urls import path
from . import views

urlpatterns = [

    # task list
    path('', views.Index.as_view(), name='index'),
    path('tasks/', views.TaskList.as_view(), name='tasks'),

    # c(RUD) - request, update and delete views
    path('task/<int:pk>/', views.TaskDetail.as_view(), name='task'),
    path('edit/<int:pk>/', views.TaskUpdate.as_view(), name='edit'),
    path('del/<int:pk>/', views.TaskDelete.as_view(), name='del'),

]

htmx_urlpatterns = [
    path('new-task-fast/', views.TaskCreateFast, name='new-task-fast'),
]

urlpatterns += htmx_urlpatterns
