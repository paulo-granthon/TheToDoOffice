from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add_todo, name='add'),
    path('complete/<todo_id>', views.complete_todo, name='complete'),
    path('delete_completed', views.delete_completed, name='delete_completed'),
    path('delete_all', views.delete_all, name='delete_all')
]
