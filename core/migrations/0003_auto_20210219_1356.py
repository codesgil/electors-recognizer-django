# Generated by Django 3.1.6 on 2021-02-19 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210213_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elector',
            name='matricule',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]