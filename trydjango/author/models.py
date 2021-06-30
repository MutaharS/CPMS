from django.db import models

# Create your models here.
class Author(models.Model):
    authorid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=100)