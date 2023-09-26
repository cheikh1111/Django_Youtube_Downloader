from django.db import models
from datetime import datetime


# Create your models here.
class Download(models.Model):
    url = models.CharField(max_length=250)
    time = models.DateTimeField(default=datetime.now)
    ip = models.CharField(max_length=250)
