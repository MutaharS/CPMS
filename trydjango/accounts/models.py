from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    is_reviewer = models.BooleanField('reviewer status', default=False)
    is_author = models.BooleanField('author status', default=False)