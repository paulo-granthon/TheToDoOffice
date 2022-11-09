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


def f_new(req):
    folder_name = req.POST.get('folder_name')
    folder_color = req.POST.get('folder_color')
    if len(folder_name) < 1: return f_reload(req)
    folder:Folder = Folder.objects.create(user=req.user, folder_name=folder_name, color=folder_color)
    return f_open(req, folder.pk)

COLORS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

def f_new_modal(req):
    next_folder_id = 0
    folders:list[Folder] = Folder.objects.filter(user=req.user)
    folder = None
    for folder in folders:
        if 'Nova Pasta' in folder.folder_name: next_folder_id += 1
    next_folder_color = 0 if folder is None else folder.color + 1 % len(COLORS)
    return render(req, 'folders/modals/new-folder-modal.html', {
        'folder_colors':COLORS,
        'next_folder_id':str(next_folder_id),
        'new_folder_current_color':next_folder_color
    })

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

