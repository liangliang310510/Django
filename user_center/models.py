from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=20)

    password = models.CharField(max_length=40)

    mail = models.CharField(max_length=20)

    verification = models.BooleanField(default=False)


# 地址信息表(省市区地址模型)
class AreaInfo(models.Model):
    name = models.CharField(max_length=20)

    parent = models.ForeignKey('self', null=True, blank=True)


# 添加个人地址
class AddressInfo(models.Model):
    realname = models.CharField(max_length=10)
    address = models.CharField(max_length=100)  # 省市区使用空格进行分割
    detail = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    def_address = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo)