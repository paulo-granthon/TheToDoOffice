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
    pk = pk-1
    tasks = Task.objects.filter(user=req.user)

    folder = None

    if pk < 0:
        return f_all(req)

    else:
        print("open folder | pk: " + str(pk))
        folder = Folder.objects.all()[pk]
        print("open folder | name: " + folder.name)

        req.session['current_folder'] = pk

        # filter tasks to only include from the selected folder
        tasks = tasks.filter(folder=folder)

    print(folder.name)

    return render(req, 'todo/task_list.html', get_context(req, {'tasks': tasks}))


def add(req):
    name = req.POST.get('name')
    folder = Folder.objects.create(user=req.user, name=name)
    f = Folder.objects.filter(user=req.user)
    return render(req, 'folders/folder_list.html', {'folders': f})

#
# def edit(req):
#     model = Folder
#     fields = ['title', 'description', 'completed']
#     success_url = reverse_lazy('index')
#
#


def f_del(req, pk):
    for i in range(10):
        print(pk)
    folder = Folder.objects.get(pk=pk)
    for i in range(10):
        print(folder)
    req.user.folders.remove(folder)
    return folders
