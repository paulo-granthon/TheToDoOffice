from django import forms
from .models import Task


class TaskFormFast(forms.Form):
    model = Task
    template_name = "todo/fast_task_form.html"
    text = forms.CharField(max_length=40, widget=forms.TextInput(
        # attrs={
        #     'class': 'form-control',
        #     'placeholder': 'Enter todo e.g. Delete junk files',
        #     'aria-label': 'Todo',
        #     'aria-describedby': 'add-btn'
        # }
    ))


class TaskForm(forms.Form):
    model = Task
    text = forms.CharField(max_length=40, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter todo e.g. Delete junk files',
            'aria-label': 'Todo',
            'aria-describedby': 'add-btn'
        }
    ))
