from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your views here.

class UserManager(BaseUserManager):
    pass

class User(AbstractBaseUser):
    objects = UserManager()
    id = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
