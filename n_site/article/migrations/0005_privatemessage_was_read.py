# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20151127_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatemessage',
            name='was_read',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
