# Django imports
from django.urls import path

# app imports
from . import views


urlpatterns = [
    # path('edit/<int:pk>', views.edit, name='edit'),
    # path('delete/<int:pk>', views.delete, name='delete'),

]

htmx_urlpatterns = [

    path('folders', views.folders, name="folders"),

    path('all/', views.f_all, name="all"),
    path('open/<int:pk>/', views.f_open, name="open"),

    path('f_del/<int:pk>/', views.f_del, name="f_del"),

    path('new_folder', views.f_new, name='new_folder'),
    path('new-folder/', views.f_new_modal, name="new-folder-modal")
]

urlpatterns += htmx_urlpatterns
