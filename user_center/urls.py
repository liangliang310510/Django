from django.conf.urls import url
from user_center import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),
    url(r'^register_username_check/$', views.register_username_check),
    url(r'^activate_mailbox/$', views.activate_mailbox),
    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^tips/$', views.tips),
    url(r'^$', views.center),
    url(r'^login_out/$', views.login_out),
    url(r'^address/$', views.address),
    url(r'^area/$', views.area),
    url(r'^address_edit_handle/$', views.address_edit_handle),
    url(r'^address_edit/$', views.address_edit),
    # url(r'^address_delete_(\d+)/$', views.address_delete),
    url(r'^address_delete/$', views.address_delete),
    url(r'^address_default(\d+)/$', views.address_default),
    url(r'^is_login/$', views.is_login),
    url(r'^order/$', views.order),
]

