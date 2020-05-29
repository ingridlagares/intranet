# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models




class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    title = models.CharField(max_length=100, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return (self.first_name or "") + (self.last_name or "")

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, projectsApp_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
