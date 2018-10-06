from django.conf.urls import include, url
from django.contrib import admin
from cart import views

urlpatterns = [
    url(r'^$', views.cart),
    url(r'^add_goods/$', views.add_goods),
    url(r'^count/$', views.count),
    url(r'^edit/$', views.edit),
    url(r'^del_goods/$', views.del_goods),
]
