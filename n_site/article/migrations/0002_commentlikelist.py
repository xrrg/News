# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentLikeList',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('user_nick', models.CharField(max_length=50, blank=True)),
                ('related_article', models.ForeignKey(to='article.Article')),
                ('related_comment', models.ForeignKey(to='article.Comment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
