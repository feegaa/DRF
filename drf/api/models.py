from django.db import models

# Create your models here.

class PostModel(models.Model):
    title   = models.CharField(max_length=10)
    content = models.CharField(max_length=10)
    date    = models.DateField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.title
