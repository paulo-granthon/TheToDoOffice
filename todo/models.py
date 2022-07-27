from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from folders.models import Folder


class Task(models.Model):

    # fields
    # user = models.ManyToOneRel(User, related_name='tasks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    title = models.CharField(max_length=40)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    # initialize list reference
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('tasks', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['completed']
