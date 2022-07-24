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
from .forms import TaskForm, TaskFormFast


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return get_context(self.request, context)


def get_context(request, context):
    if context.__contains__('tasks'):
        context['tasks'] = context['tasks'].filter(user=request.user)
    else:
        context.update({'tasks': Task.objects.filter(user=request.user)})

    search_input = request.GET.get('search-area') or ''
    if search_input:
        context['tasks'] = context['tasks'].filter(title__icontains=search_input)

    context['search_input'] = search_input

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
    title = req.POST.get('title')

    task = Task.objects.create(user=req.user, title=title)

    tasks = Task.objects.filter(user=req.user)
    return render(req, 'todo/task_list.html', {'tasks': tasks})


class TaskCreate(CreateView):
    model = Task
    fields = ['title', 'description']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('index')


class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task_del.html'
    success_url = reverse_lazy('index')
