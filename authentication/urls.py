# Django imports
from django.urls import path
from django.contrib.auth.views import LogoutView

# app imports
from . import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # old urls
    # path('login_old', views.login_index, name='login_page_old'),
]

htmx_urlpatterns = [
   path('check_username/', views.check_username, name='check_username')
]

urlpatterns += htmx_urlpatterns
