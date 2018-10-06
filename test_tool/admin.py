from django.contrib import admin
# Register your models here.
from test_tool.models import GoodsInfo


class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id']

admin.site.register(GoodsInfo, GoodsInfoAdmin)