# Django imports
from django.urls import path

# app imports
from . import views


urlpatterns = [
    # path('edit/<int:pk>', views.edit, name='edit'),
    # path('delete/<int:pk>', views.delete, name='delete'),

]

htmx_urlpatterns = [

    # list
    path('folders', views.folders, name="folders"),

    # open
    path('all/', views.f_all, name="all"),
    path('open/<int:pk>/', views.f_open, name="open"),
    path('f5/', views.f_reload, name="f5"),

    # delete
    path('f_del/<int:pk>/', views.f_del, name="f_del"),

    # create
    path('new_folder', views.f_new, name='new_folder'),

    # create modal
    path('new-folder/', views.f_new_modal, name="new-folder-modal"),
    path('new-folder/colors', views.f_new_modal_colors, name="new-folder-modal-colors"),

    # create modal utils
    path('new-folder/sel-col/<int:color>', views.f_new_select_color, name="new-folder-modal-select-color"),
    path('new-folder/sel-col-rand', views.f_new_rand_col, name='f_new_rand_col'),
    path('new-folder/sel-col-update', views.f_new_update_selected, name='f_new_update_selected'),

    path('edit-folder/<int:pk>', views.f_edit_color, name="edit-folder-color"),
    path('edit-folder/<int:pk>/color/<int:color>', views.f_set_color, name="set-folder-color"),

]

urlpatterns += htmx_urlpatterns
