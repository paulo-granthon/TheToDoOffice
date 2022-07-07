from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=40)
    completed = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['completed']
