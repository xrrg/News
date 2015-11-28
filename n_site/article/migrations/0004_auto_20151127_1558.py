# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0003_comment_author_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('header', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('was_send', models.DateTimeField(verbose_name='message was send')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Author', max_length=30, db_column='author', related_name='author')),
                ('reciever', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Reciever', max_length=30, db_column='reciever', related_name='reciever')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='article',
            name='article_title',
            field=models.CharField(max_length=150),
            preserve_default=True,
        ),
    ]
