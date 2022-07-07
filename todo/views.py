from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Todo
from .forms import TodoForm


def index(req):
    todo_list = Todo.objects.order_by('id')
    form = TodoForm()
    context = {'todo_list': todo_list, 'form': form}
    return render(req, 'todo/index.html', context)


@require_POST
def add_todo(req):
    form = TodoForm(req.POST)
    print(req.POST['text'])
    if form.is_valid():
        new_todo = Todo(title=req.POST['text'])
        new_todo.save()
    return redirect('index')


def complete_todo(req, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.completed = True
    todo.save()
    return redirect('index')


def delete_completed(req):
    Todo.objects.filter(completed__exact=True).delete()
    return redirect('index')


def delete_all(req):
    Todo.objects.all().delete()
    return redirect('index')
