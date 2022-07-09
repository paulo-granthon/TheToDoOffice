from django.urls import path
from . import views
urlpatterns = [
    # path('', views.index, name='index'),
    path('login', views.login_index, name='login_index'),
    path('login', views.login_index, name='login_page'),
]
