# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('pic', models.CharField(max_length=100)),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('click', models.IntegerField()),
                ('unit', models.CharField(max_length=10)),
                ('delete', models.BooleanField(default=False)),
                ('subtitle', models.CharField(max_length=200)),
                ('inventory', models.IntegerField(default=100)),
                ('details', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=20)),
                ('delete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='type',
            field=models.ForeignKey(to='product_display.TypeInfo'),
        ),
    ]
