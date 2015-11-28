# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_commentlikelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author_id',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
