from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=140)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title