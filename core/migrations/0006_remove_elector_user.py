# Generated by Django 3.1.6 on 2021-03-31 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_elector_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elector',
            name='user',
        ),
    ]
