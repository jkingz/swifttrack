# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-16 06:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='date_of_leave',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
