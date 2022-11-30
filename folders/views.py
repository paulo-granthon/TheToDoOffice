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

    # print("open folder | folder_name: " + folder.folder_name)
    if 'sel_tasks' not in req.session: req.session.update({'sel_tasks': []})
    else: req.session['sel_tasks'] = []

    return render(req, 'todo/task_list.html', get_context(req, {'tasks': tasks}))


def f_reload(req):
    if 'current_folder' not in req.session or req.session['current_folder'] < 0:
        return f_all(req)
    return f_open(req, req.session['current_folder'])


def f_new(req):
    folder_name = req.POST.get('folder_name')
    folder_color = req.session['new_folder_current_color'] if 'new_folder_current_color' in req.session else 0
    if len(folder_name) < 1: return f_reload(req)
    folder:Folder = Folder.objects.create(user=req.user, folder_name=folder_name, color=folder_color)
    return f_open(req, folder.pk)

COLORS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

def f_new_modal(req):
    next_folder_id = 1
    folders:list[Folder] = Folder.objects.filter(user=req.user)
    
    folder = None
    
    for folder in folders:
        if 'Nova Pasta' in folder.folder_name: next_folder_id += 1
    next_folder_color = (req.session['new_folder_current_color'] if 'new_folder_current_color' in req.session else 0) if folder is None else folder.color + 1 % len(COLORS)
    
    if 'new_folder_current_color' in req.session: req.session['new_folder_current_color'] = next_folder_color
    else: req.session.update({'new_folder_current_color':next_folder_color})

    if 'folder_colors' not in req.session: req.session.update({'folder_colors':COLORS})
    
    return render(req, 'folders/modals/new-folder-modal.html', {
        'folder_colors':COLORS,
        'next_folder_id':'' if next_folder_id == 1 else str(next_folder_id),
        'new_folder_current_color':next_folder_color
    })

def f_new_modal_colors(req):
    return render(req, 'folders/modals/new-folder-modal-colors.html', {})

def f_new_select_color(req, color):
    if 'new_folder_current_color' in req.session: req.session['new_folder_current_color'] = color
    else: req.session.update({'new_folder_current_color':color})
    return render(req, 'folders/modals/new-folder-modal-colors.html', {
        'folder_colors':COLORS,
        'new_folder_current_color':color
    })

def f_new_rand_col(req):
    from random import randint
    return f_new_select_color(req, randint(0, 12))

def f_new_update_selected(req):
    return render(req, 'folders/modals/new-folder-modal-color-selected.html', {'new_folder_current_color':req.session['new_folder_current_color']})
#
# def edit(req):
#     model = Folder
#     fields = ['title', 'description', 'completed']
#     success_url = reverse_lazy('index')
#
#

def f_edit_color (req, pk):
    return f_set_color(req, pk, (Folder.objects.get(pk=pk).color + 1) % len(COLORS))
    return render(req, 'folders/modals/edit-folder-modal.html', {
        'folder_colors':COLORS,
        'folder':Folder.objects.get(pk=pk)
    })


def f_set_color (req, pk, color):
    folder = Folder.objects.get(pk=pk)
    prevcol = folder.color
    folder.color = color
    folder.save()
    print(f'{folder.folder_name} color is now {color} instead of {prevcol}')
    return folders(req)

def f_del(req, pk):
    Folder.objects.filter(pk=pk).delete()
    if 'current_folder' not in req.session or pk is req.session['current_folder']:
        return f_all(req)
    else:
        return f_reload(req)

