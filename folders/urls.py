# Django imports
from django.urls import path

# app imports
from . import views


urlpatterns = [
    path('add', views.add, name='add'),
    # path('edit/<int:pk>', views.edit, name='edit'),
    # path('delete/<int:pk>', views.delete, name='delete'),

]

htmx_urlpatterns = [
    path('all/', views.f_all, name="all"),
    path('open/<int:pk>/', views.f_open, name="open")
]

urlpatterns += htmx_urlpatterns
