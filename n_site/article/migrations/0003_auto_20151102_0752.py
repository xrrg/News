# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20151101_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='was_liked',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='c_was_liked',
        ),
    ]
