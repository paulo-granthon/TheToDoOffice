from django.shortcuts import render

from todo.views import Task, get_context
from .models import Folder


def folders(req):

    return render(req, 'folders/folder_list.html', get_context(req, {}))


def f_all(req):
    print("open folder| all")
    req.session['current_folder'] = -1
    tasks = Task.objects.filter(user=req.user)
    return render(req, 'todo/task_list.html', get_context(req, {'tasks': tasks}))


def f_open(req, pk=-1):
    tasks = Task.objects.filter(user=req.user)

    if pk < 0:
        return f_all(req)

    try:
        folder = Folder.objects.get(pk=pk)
        req.session['current_folder'] = pk

        # filter tasks to only include from the selected folder
        tasks = tasks.filter(folder=folder)

    except Folder.DoesNotExist:
        return f_all(req)

    print("open folder | folder_name: " + folder.folder_name)

    return render(req, 'todo/task_list.html', get_context(req, {'tasks': tasks}))


def f_reload(req):
    if 'current_folder' not in req.session or req.session['current_folder'] > 0:
        return f_all(req)

    try:
        folder = Folder.objects.get(pk=req.session['current_folder'])
    except Folder.DoesNotExist:
        return f_all(req)

    tasks = Task.objects.filter(user=req.user).filter(folder=folder)
    return render(req, 'todo/task_list.html', get_context(req, {'tasks': tasks}))


def new_folder(req):
    folder_name = req.POST.get('folder_name')
    folder = Folder.objects.create(user=req.user, folder_name=folder_name)
    for _ in range(20):
        print(folder.pk)
    return f_open(req, folder.pk)


def new_folder_modal(req):
    return render(req, 'folders/new-folder.html', {})

#
# def edit(req):
#     model = Folder
#     fields = ['title', 'description', 'completed']
#     success_url = reverse_lazy('index')
#
#


def f_del(req, pk):
    Folder.objects.filter(pk=pk).delete()
    if 'current_folder' not in req.session or pk is req.session['current_folder']:
        return f_all(req)
    else:
        return f_reload(req)

