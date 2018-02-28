# Generated by Django 2.0.2 on 2018-02-22 14:36

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import othello.apps.users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1000)])),
                ('service', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=32, unique=True)),
                ('full_name', models.CharField(max_length=60)),
                ('email', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('github_token', models.CharField(blank=True, max_length=40)),
                ('access_token', models.CharField(blank=True, max_length=64, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', othello.apps.users.models.UserManager()),
            ],
        ),
    ]