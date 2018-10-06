# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('realname', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('detail', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=11)),
                ('def_address', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to='user_center.UserInfo')),
            ],
        ),
        migrations.CreateModel(
            name='AreaInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('parent', models.ForeignKey(to='user_center.AreaInfo', blank=True, null=True)),
            ],
        ),
    ]
