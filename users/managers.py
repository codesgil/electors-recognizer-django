from django.db import models
from django.contrib.auth.base_user import BaseUserManager


class ProfileManager(models.Manager):
    pass


class UserManager(BaseUserManager):
    pass
