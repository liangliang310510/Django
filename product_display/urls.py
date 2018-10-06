from django.conf.urls import url, include

from product_display import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^product_list_(\d+)_(\d+)/$', views.product_list),
    url(r'^detail_(\d+)/$', views.detail),
    # url(r'^search/$', include('haystack.urls')),
    url(r'^search/$', views.MySearchView.as_view()),
]