# general app imports
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse_lazy

# todo app imports
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

# todo classes imports
from .models import Task
from .forms import TaskFormFast

# folders imports
from folders.models import Folder


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return get_context(self.request, context)


def get_context(request, context):

    # if context already contains 'tasks', update the list
    # otherwise, create the list
    if 'tasks' in context:
        context['tasks'] = context['tasks'].filter(user=request.user)
    else:
        context.update({'tasks': Task.objects.filter(user=request.user)})

    # get the user's folders
    context.update({'folders': Folder.objects.filter(user=request.user)})

    # initialize folder variable
    folder = None

    # if session contains a folder pk, get the folder object as 'folder'
    # otherwise, there is no current folder, just leave 'folder' as None
    if 'current_folder' in request.session:
        session_folder = request.session['current_folder']
        try:
            folder = Folder.objects.all().get(pk=session_folder)
        except Folder.DoesNotExist:
            folder = None
            request.session['current_folder'] = -1

    # if there's a current folder parameter in context, set its value
    # otherwise, add the parameter to context and set its value
    if 'current_folder' in context:
        context['current_folder'] = folder
    else:
        context.update({'current_folder': folder})

    # finally, if the folder is not None, set 'tasks' in the context as the folder's tasks only
    if folder is not None:
        context['tasks'] = context['tasks'].filter(folder=folder)

    # get the search input if any
    search_input = request.GET.get('search-area') or ''
    # if search input is present, filter the tasks by its text
    if search_input:
        context['tasks'] = context['tasks'].filter(title__icontains=search_input)

    print(context['current_folder'])
    print(folder)

    # update the search input context
    context['search_input'] = search_input

    # pass the TaskForm as context
    context['fast_form'] = TaskFormFast()

    return context


def tasks(req):
    return render(req, 'todo/task_list.html', get_context(req, {}))


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'


def t_new(req):
    folder = None
    if 'current_folder' in req.session and req.session['current_folder'] >= 0:
        try:
            folder = Folder.objects.get(pk=req.session['current_folder'])
        except Folder.DoesNotExist:
            pass
        print("new task in folder: " + folder.folder_name)
    else:
        print("new uncategorized task")
    Task.objects.create(user=req.user, title=req.POST.get('title'), folder=folder)
    return render(req, 'todo/task_list.html', get_context(req, {'tasks': Task.objects.filter(user=req.user)}))


class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('index')


def t_del(req, pk):
    Task.objects.get(pk=pk).delete()
    return tasks(req)


def t_sel(req, pk):

    # try to get task from pk
    try:
        sel_task = Task.objects.get(pk=pk)

    # no task found
    except Task.DoesNotExist:
        return HttpResponse(status=404)

    # initialize session 'sel_tasks' with sel_task if list is not in session yet
    if 'sel_tasks' not in req.session or pk not in req.session['sel_tasks']:
        req.session['sel_tasks'] = list({pk})
        return HttpResponse(status=201)

    req.session['sel_tasks'] = list()

    return HttpResponse(status=201)


def t_sel_multi(req, pk):

    # try to get task from pk
    try:
        sel_task = Task.objects.get(pk=pk)

    # no task found
    except Task.DoesNotExist:
        return HttpResponse(status=404)

    # initialize session 'sel_tasks' with sel_task if list is not in session yet
    if 'sel_tasks' not in req.session:
        req.session['sel_tasks'] = list({pk})
        return HttpResponse(status=201)

    # reference the list locally
    session_tasks = req.session['sel_tasks']

    # select sel_task if not selected yet
    if pk not in session_tasks:
        session_tasks.append(pk)

    # otherwise, deselect it
    else:
        session_tasks.remove(pk)

    # replace the list
    req.session['sel_tasks'] = list(session_tasks)

    for task in session_tasks:
        print(task)

    return HttpResponse(status=201)
