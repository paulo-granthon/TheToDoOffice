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

# Those will return partial renders for the htmx to swap
htmx_urlpatterns = [

    # create
    path('new-task-fast/', views.t_new, name='new-task-fast'),

    # task actions
    path('complete/<int:pk>/', views.t_complete, name='complete'),
    path('move/<int:pk>/to/<int:pk2>', views.t_move, name='move'),
    path('move/<int:pk>/to/-1', views.t_move, name='move'),
    path('del/<int:pk>/', views.t_del, name='del'),

    # selects
    path('sel/<int:pk>/', views.t_sel, name='sel'),
    path('sel_multi/<int:pk>/', views.t_sel_multi, name='sel-multi'),

    # selected actions
    path('sel_actions_update/', views.t_sel_actions, name="sel-actions-update"),
    path('sel_complete/<int:pk>/', views.sel_complete, name='sel-complete'),
    path('sel_move_to/<int:pk>', views.sel_move, name='sel-move'),          
    path('sel_move_to/-1', views.sel_move, name='sel-move'),          
    path('sel_del/<int:pk>/', views.sel_del, name='sel-del'),

    # modals
    path('move/<int:pk>', views.move_modal, name="move-modal"),
    path('sel_move/', views.sel_move_modal, name="sel-move-modal"),
]

urlpatterns += htmx_urlpatterns
