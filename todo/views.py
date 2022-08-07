# general app imports
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse  # to redirect back to the previous page after creating a task

# todo app imports
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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


class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        return get_context(self.request, context)


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'


def TaskCreateFast(req):
    folder = None
    if 'current_folder' in req.session and req.session['current_folder'] >= 0:
        try:
            folder = Folder.objects.get(pk=req.session['current_folder'])
        except Folder.DoesNotExist:
            pass
        print("new task in folder: " + folder.name)
    else:
        print("new uncategorized task")
    Task.objects.create(user=req.user, title=req.POST.get('title'), folder=folder)
    tasks = Task.objects.filter(user=req.user)
    return render(req, 'todo/task_list.html', get_context(req, {'tasks': tasks}))


class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('index')


class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task_del.html'
    success_url = reverse_lazy('index')
