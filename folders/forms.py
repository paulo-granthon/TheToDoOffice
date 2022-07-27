from django import forms
from .models import Folder


class TaskFormFast(forms.Form):
    model = Folder
    template_name = "folders/new-folder.html"
    text = forms.CharField(max_length=40)
