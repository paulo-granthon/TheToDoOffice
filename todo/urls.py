from django.urls import path
from . import views

urlpatterns = [

    # task list
    path('', views.Index.as_view(), name='index'),
    path('tasks/', views.tasks, name='tasks'),

    # c(RUD) - request, update and delete views
    path('task/<int:pk>/', views.TaskDetail.as_view(), name='task'),
    path('edit/<int:pk>/', views.TaskUpdate.as_view(), name='edit'),

]

htmx_urlpatterns = [
    path('new-task-fast/', views.t_new, name='new-task-fast'),
    path('del/<int:pk>/', views.t_del, name='del'),
]

urlpatterns += htmx_urlpatterns
