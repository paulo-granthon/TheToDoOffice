# general app imports
from django.http import HttpResponse
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


class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)

        # only return the current user's tasks
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(completed=False).count()

        # add the fast_form as context
        context['fast_form'] = TaskFormFast()

        # search related logic
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input

        # return the context
        return context


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'


@require_POST
def TaskCreateFast(req):
    form = TaskFormFast(req.POST)
    print(req.POST['text'])
    if form.is_valid():
        Task(user=req.user, title=req.POST['text']).save()
    return redirect('tasks')


class TaskCreate(CreateView):
    model = Task
    fields = ['title', 'description']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks')


class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task_del.html'
    success_url = reverse_lazy('tasks')
