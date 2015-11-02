# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article_text', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='article was published')),
                ('author_nickname', models.CharField(max_length=50)),
                ('article_title', models.CharField(max_length=50)),
                ('was_liked', models.BooleanField(default=False)),
                ('likes_number', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('categoty_name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('com_nickname', models.CharField(max_length=50)),
                ('comment_text', models.TextField()),
                ('comment_pub_date', models.DateTimeField(verbose_name='comment was published')),
                ('c_likes_number', models.IntegerField(default=0)),
                ('c_was_liked', models.BooleanField(default=False)),
                ('article', models.ForeignKey(to='article.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(to='article.Category'),
            preserve_default=True,
        ),
    ]
