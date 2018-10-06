from django.db import models

# Create your models here.
from product_display.models import GoodsInfo
from user_center.models import UserInfo, AddressInfo


class OrderMain(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING)
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(AddressInfo, on_delete=models.DO_NOTHING)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.IntegerField(default=0)


class OrderDetail(models.Model):
    order = models.ForeignKey(OrderMain, on_delete=models.DO_NOTHING)
    goods = models.ForeignKey(GoodsInfo, on_delete=models.DO_NOTHING)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)



