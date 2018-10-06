from django.conf.urls import include, url
from order import views

urlpatterns = [
    url(r'^checkout/$', views.checkout),
    url(r'^order_handle/$', views.order_handle),
]
