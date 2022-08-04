from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your views here.

class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, email, password):
        if not email:
            raise ValueError('must have user email')
        if not password:
            raise ValueError('must have user password')

        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
