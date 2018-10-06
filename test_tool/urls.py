from django.conf.urls import url, include
from django.views.generic import TemplateView

from test_tool import views

urlpatterns = [
    url(r'^send$', views.send),
    url(r'^redis$', views.redis),
    url(r'^test_thread/$', views.test_thread),
    url(r'^editor/$', views.editor),
    # url(r'^query/$', views.query),
    # 基于类的视图,可以传递用于渲染的html文件
    url(r'^query/$', views.QueryView.as_view(template_name='test_tool/query.html')),
    url(r'^search/$', include('haystack.urls')),
]