from django.db import models

class Test(models.Model):
    dateOnly = models.DateField()
    datetime = models.DateTimeField()

