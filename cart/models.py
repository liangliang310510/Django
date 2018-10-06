from django.db import models

# Create your models here.
from product_display.models import GoodsInfo
from user_center.models import UserInfo


class CartInfo(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    goods = models.ForeignKey(GoodsInfo)
    user = models.ForeignKey(UserInfo)
    count = models.IntegerField(default=1)

