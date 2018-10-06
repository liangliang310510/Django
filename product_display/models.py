from django.db import models

# Create your models here.
from tinymce.models import HTMLField


class TypeInfo(models.Model):
    title = models.CharField(max_length=20)
    delete = models.BooleanField(default=False)

class GoodsInfo(models.Model):
    name = models.CharField(max_length=50)
    pic = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    click = models.IntegerField()
    unit = models.CharField(max_length=10)
    delete = models.BooleanField(default=False)
    subtitle = models.CharField(max_length=200)
    inventory = models.IntegerField(default=100)
    details = HTMLField()
    type = models.ForeignKey(TypeInfo)
