from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy  # to redirect back to the previous page after creating a task

from .models import Task
from .forms import TaskForm, TaskFormFast


class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['fast_form'] = TaskFormFast()
        return context


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'


class TaskCreateFast(CreateView):
    model = Task
    fields = ['title']


class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')

