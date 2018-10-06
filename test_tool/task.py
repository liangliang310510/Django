import uuid

from celery.task import task
from django.core.mail import send_mail
from redis import StrictRedis

from ttsx import settings

@task
def send(id, mail):
    uuid_str = uuid.uuid1()
    sr = StrictRedis()
    result = sr.set(id, uuid_str)  # 把id:token_str设置到redis数据库中
    html_message = '<a href="http://127.0.0.1:8000/user/activate_mailbox/?id=%d&token=%s">激活邮箱</a>' %(id,uuid.uuid1())
    """
    subject:主题，
    from_email:发送者，
    recipient——list :接受者;
    html_message:带超链接的邮件正文
    """
    send_mail('激活邮件', '', settings.EMAIL_FROM, [mail], html_message=html_message)