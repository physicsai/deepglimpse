# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-23 02:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newscontent', '0011_auto_20180122_2113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zipcodes',
            old_name='rec_no',
            new_name='id',
        ),
    ]
