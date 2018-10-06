# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0002_addressinfo_areainfo'),
        ('product_display', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('price', models.DecimalField(default=0, decimal_places=2, max_digits=5)),
                ('goods', models.ForeignKey(to='product_display.GoodsInfo', on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
        ),
        migrations.CreateModel(
            name='OrderMain',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(default=0, decimal_places=2, max_digits=8)),
                ('status', models.IntegerField(default=0)),
                ('address', models.ForeignKey(to='user_center.AddressInfo', on_delete=django.db.models.deletion.DO_NOTHING)),
                ('user', models.ForeignKey(to='user_center.UserInfo', on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(to='order.OrderMain', on_delete=django.db.models.deletion.DO_NOTHING),
        ),
    ]
