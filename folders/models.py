from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Folder (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='folders')
    name = models.CharField(max_length=32)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('folders', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
