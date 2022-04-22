import datetime

from django.db import models

# Create your models here.
from users.models import User


class VoteOffice(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    enabled = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = 'vote_office'
        ordering = ['-created']


class Elector(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    surname = models.CharField(max_length=200, blank=True, null=True)
    birthDate = models.DateField(db_column="birth_date")
    birthPlace = models.CharField(max_length=255, db_column="birth_place")
    gender = models.CharField(max_length=8, blank=True)
    phone = models.CharField(max_length=14, null=True, blank=False, db_column='phone')
    matricule = models.CharField(max_length=255, unique=True, blank=True)
    localisation = models.CharField(max_length=255, blank=True, null=True)
    voteOffice = models.ForeignKey(VoteOffice, models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.matricule:
            self.matricule = datetime.datetime.now().strftime("%Y%H%M%S%f")
        super(Elector, self).save(*args, **kwargs)

    class Meta:
        db_table = 'elector'
        ordering = ['-created']


class Campaign(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    enabled = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if self.enabled:
            Campaign.objects.filter(enabled=True).update(enabled=False)
        super(Campaign, self).save(*args, **kwargs)

    class Meta:
        db_table = 'campaign'
        ordering = ['-created']


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    voted = models.BooleanField(default=True)
    campaign = models.ForeignKey(Campaign, models.SET_NULL, blank=True, null=True)
    elector = models.ForeignKey(Elector, models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 'vote'
        ordering = ['-created']
