# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=40)),
                ('mail', models.CharField(max_length=20)),
                ('verification', models.BooleanField(default=False)),
            ],
        ),
    ]
