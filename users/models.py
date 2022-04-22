from django.db import models
from .managers import ProfileManager, UserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .constants import Form, TOKEN


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=250, null=False, blank=False, db_column='first_name')
    last_name = models.CharField(max_length=250, null=True, blank=True, db_column='last_name')
    phone = models.CharField(max_length=14, null=False, blank=False, db_column='phone')
    email = models.EmailField(max_length=150, blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True, db_column='update_at')

    objects = ProfileManager()

    class Meta:
        db_table = 'profile'
        ordering = ['id']


class User(AbstractUser):
    username = models.CharField(db_index=True, max_length=150, unique=True, null=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=30, null=False, choices=Form.ROLES)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    voteOffice = models.ForeignKey('core.VoteOffice', models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, db_column='created_at')
    update_at = models.DateTimeField(auto_now=True, db_column='update_at')
    deleted = models.BooleanField(default=False, blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        db_table = 'user'
        ordering = ['-id']


class BlackListedToken(models.Model):
    token = models.TextField()
    jti = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, related_name="token_user", on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=14, null=False, choices=Form.TOKEN_TYPE, default=TOKEN)
    created_at = models.DateTimeField(default=timezone.now)
    expired_at = models.DateTimeField(null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'blacklisted_token'
        unique_together = ("token", "user")
        ordering = ['id']
