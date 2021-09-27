
from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    startdate=models.DateTimeField()
    enddate=models.DateTimeField()

    def __str__(self):
        return self.name