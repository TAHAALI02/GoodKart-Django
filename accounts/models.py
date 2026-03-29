from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)  # hashes the password properly
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, password):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=15, unique=False, null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
