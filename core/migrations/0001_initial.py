# Generated by Django 3.1.6 on 2021-02-13 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('enabled', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'campaign',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Elector',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(blank=True, max_length=200, null=True)),
                ('birth_date', models.DateField()),
                ('birth_place', models.CharField(max_length=255)),
                ('matricule', models.CharField(max_length=255, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'elector',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('voted', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.campaign')),
                ('elector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.elector')),
            ],
            options={
                'db_table': 'vote',
                'ordering': ['-created'],
            },
        ),
    ]