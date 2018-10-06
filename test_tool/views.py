import uuid

import time
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail


# Create your views here.
from django.views.generic import TemplateView
from redis import StrictRedis

from test_tool.models import GoodsInfo
from ttsx import settings


def send(request):
    html_message = '<a href="http://127.0.0.1:8000/user/activate_mailbox/?token=%s">激活邮箱</a>' %uuid.uuid1()

    send_mail('激活邮件', '', settings.EMAIL_FROM, ['1974737340@qq.com'], html_message=html_message)
    return HttpResponse('ok')


def redis(request):
    sr = StrictRedis()
    result = sr.set('itcast','888888')
    if result:
        msg = 'ok'
    else:
        msg = 'error'
    return HttpResponse(msg)


def test_thread(request):
    _task()
    return HttpResponse('OK Thread')


def _task():
    print('hello')
    time.sleep(2)
    print('world')


def editor(request):
    goods= GoodsInfo.objects.get(id=1)
    context = {'details':goods.detail}

    return render(request, 'test_tool/editor.html', context)


def query(request):
    return render(request, 'test_tool/query.html')


class QueryView(TemplateView):
    template_name = 'test_tool/query.html'  # template_name用于指定要渲染的模板文件
    def get_context_data(self, **kwargs):
        context = super(QueryView, self).get_context_data(**kwargs)
        context['data'] = 'itcast'
        return context