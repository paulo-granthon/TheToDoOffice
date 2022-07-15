from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):

    # fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=40)
    description = models.TextField(null=True, blank=True)
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
