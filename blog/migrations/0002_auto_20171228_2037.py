# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='created_time',
            new_name='time',
        ),
        migrations.RemoveField(
            model_name='post',
            name='excerpt',
        ),
        migrations.RemoveField(
            model_name='post',
            name='modified_time',
        ),
        migrations.AddField(
            model_name='post',
            name='file',
            field=models.CharField(default='null', max_length=50),
        ),
    ]