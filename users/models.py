from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from users.managers import CustomUserManager
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token





class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=10,null=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    education = models.CharField(max_length=30)
    bio = models.TextField()
    age = models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to='users/images/')
    otp = models.CharField(max_length=6)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name','last_name','age','bio','education','image']
    objects = CustomUserManager()




    def show_bio(self):
        return self.bio[:10]

    def __str__(self):
        return self.email

    def save(self,*args,**kwargs):
        self.username=(self.first_name)+' user'
        return super().save(*args,**kwargs)







