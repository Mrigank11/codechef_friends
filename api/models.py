from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CCUser(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False)
    tokens = models.TextField()
