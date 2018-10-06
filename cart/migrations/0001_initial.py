# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_display', '0001_initial'),
        ('user_center', '0002_addressinfo_areainfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('count', models.IntegerField(default=1)),
                ('goods', models.ForeignKey(to='product_display.GoodsInfo')),
                ('user', models.ForeignKey(to='user_center.UserInfo')),
            ],
        ),
    ]
