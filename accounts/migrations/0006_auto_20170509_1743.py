# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-09 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20170509_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(default='img/default-profile.png', upload_to='profiles', verbose_name='Profile picture'),
        ),
    ]
