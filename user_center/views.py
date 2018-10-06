import datetime
import hashlib

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from redis import StrictRedis

from order.models import OrderMain
from product_display.models import GoodsInfo
from user_center import task
from user_center.models import UserInfo, AddressInfo, AreaInfo
from user_center.utils import user_login


def register(request):
    context = {'title': '注册'}
    return render(request, 'user_center/register.html', context)


def register_handle(request):
    username = request.POST.get('user_name')
    password = sha1(request.POST.get('pwd'))
    email = request.POST.get('email')

    is_username_exist = UserInfo.objects.filter(username=username).count() > 0
    # is_email_exist = UserInfo.objects.filter(mail=email).count() > 0
    is_email_exist = False  # 暂时不校验邮箱

    if not is_email_exist and not is_username_exist:  # 如果两者都不存在再重新创建一个新UserInfo对象用来存储数据
        user = UserInfo()
        user.username = username
        user.password = password
        user.mail = email
        user.save()
        # 发送验证邮件
        # send(user.id, user.mail)
        task.send.delay(user.id, user.mail)  # 将任务加入到队列中
        context = {'info': '请登录邮箱进行激活'}
        return render(request, 'tips.html', context)
    else:
        context = {'title': '注册', 'error': '用户名或邮箱已存在'}
        return render(request, 'user_center/register.html', context)


def register_username_check(request):
    username = request.GET.get('username')

    # if UserInfo.objects.filter(username=username):
    #     result = False
    # else:
    #     result = True
    # 以上代码表示如果数据库中已经存在注册用户，返回False，否则返回True，也可以写成如下格式
    result = UserInfo.objects.filter(username=username).count() == 0

    return JsonResponse({'result': result})


def sha1(password):
    s1 = hashlib.sha1()
    s1.update(password.encode('utf-8'))

    return s1.hexdigest()


# 这个函数是send函数通过url过来调用的，html_message中的超链接指向这个函数
def activate_mailbox(request):
    get = request.GET  # token和id是通过url传过来的！！！
    token = get.get('token')
    id = get.get('id')

    # 比对用户的token
    sr = StrictRedis()
    redis_token = sr.get(id)  # 默认是存储在redis的数据库0 中
    redis_token = bytes.decode(redis_token)  # 因为上面从数据库中获取的数据是二进制数据，所以需要解码(这一步bytes有问题，容易事别不出来对象！！)
    result = False
    if redis_token == token:
        user = UserInfo.objects.filter(id=id)[0]
        if user is not None and user.verification == False:
            user.verification = True
            user.save()
            result = True

    if result:
        context = {'title': '登录'}
        return render(request, 'user_center/login.html', context)
    else:
        return HttpResponse('激活失败')


def test_celery(request):
    task.work_task.delay()  # 把任务放到队列中
    return HttpResponse('OK celery')


def login_handle(request):
    post = request.POST
    username = post.get('username')
    password = post.get('pwd')

    is_login = False  # 记录登录状态
    users = UserInfo.objects.filter(username=username)  # 返回值是一个列表,列表内部都是对象

    if len(users) == 1:  # 查到用户
        password_sha1 = sha1(password)
        if users[0].password == password_sha1:
            # 登录成功
            is_login = True

    if is_login:
        # 做用户邮箱是否激活的验证
        if users[0].verification:
            # 记录用户名到cookie中
            remember = post.get('remember', '0')  # 记住密码的对勾

            # response = redirect('/user/')
            target = request.session.get('target', default='/user/')
            response = redirect(target)

            if remember == '1':
                # 记录时长为2周
                now = datetime.datetime.now()
                date = now + datetime.timedelta(days=14)
                response.set_cookie('username', username, expires=date)  # 默认记住用户名，在登录的时候传入的是COOKIE中的username

            request.session.set_expiry(0)
            request.session['uid'] = users[0].id
            request.session['username'] = users[0].username

            return response
        else:
            context = {'info': '请登录邮箱进行激活操作'}
            return render(request, 'tips.html', context)

            # return HttpResponse('ok')
    else:
        context = {'title': '登录', 'error': '用户名或者密码输入错误'}
        return render(request, 'user_center/login.html', context)


def tips(request):
    context = {'info': '密码重置邮件已经发送'}
    return render(request, 'tips.html', context)


def login(request):
    # 跳转界面:  目的：从那个界面跳转过来，推出登陆时就返回那个界面
    referer = request.META.get('HTTP_REFERER')
    if referer != None:
        index = referer.find('/', 7)
        target = referer[index:]

        request.session['target'] = target   # target是一个字典类型数据

    username = request.COOKIES.get('username', '')  # 用于记住用户名

    context = {'title': '登录', 'username': username, 'hide_top': True}  # 如果登录成功，设置hide_top为True
    return render(request, 'user_center/login.html', context)


# @user_login
def center(request):
    "用户中心入口"
    history = request.COOKIES.get('history')  # 从数据库中获取的元素应该是: {'history': 'id1,id2,id3,id4,id5'}
    list = []
    if history != None:
        history = history.split(',')
        for gid in history:
            # gid = int(gid)
            goods = GoodsInfo.objects.get(id=gid)
            list.append(goods)

    user = UserInfo.objects.get(id=request.session['uid'])

    context = {'title': '用户中心', 'list':list, 'user':user}
    return render(request, 'user_center/user_center_info.html', context)


@user_login
def login_out(request):
    request.session.flush()  # 将缓存中的数据与数据库同步
    return redirect('/user/login/')


@user_login
def address(request):
    """收货地址入口"""
    msg = request.GET.get('msg', '')  # 从address_delete中获取，若没获取就返回‘’

    id = request.session.get('uid')
    list = AddressInfo.objects.filter(user_id=id)

    if list.count() > 0:
        context = {'title': '用户中心', 'list': list, 'msg':msg}
        return render(request, 'user_center/user_center_site.html', context)
    else:
        return redirect('/user/address_edit')


def area(request):
    """省市区的列表获取"""
    area_id = request.GET.get('area_id')  # 如果选择的是省份的话，由于没有上级信息，所以返回值是None
    area_list = AreaInfo.objects.filter(parent_id=area_id)

    list = []
    for item in area_list:
        list.append({'id': item.id, 'name': item.name})

    return JsonResponse({'list': list})


@user_login
def address_edit_handle(request):
    post = request.POST
    realname = post.get('realname')
    province = post.get('province')
    city = post.get('city')
    area = post.get('area')
    detail = post.get('detail')
    phone = post.get('phone')

    # 获取地址编号
    address_id = post.get('address_id')  # 通过user_center_site_edit中的隐藏域获取address_id ，值为value值

    if address_id != '':
        # 获取地址
        address = AddressInfo.objects.get(id=address_id)
    else:
        # 设置地址
        address = AddressInfo()

    areas = AreaInfo.objects.filter(id__in=(province, city, area))

    address.realname = realname
    address.address = '%s %s %s' % (areas[0].name, areas[1].name, areas[2].name)
    address.detail = detail
    address.phone = phone
    address.user_id = request.session.get('uid')  # 用户登录的前提下
    address.save()

    return redirect('/user/address/')


def address_edit(request):
    """编辑地址的入口
        新增和编辑地址
    """
    address_id = int(request.GET.get('id', 0))  # 存在的话获取id，否则就为0
    context = {'title': '用户中心'}
    if not address_id == 0:
        address = AddressInfo.objects.get(id=address_id)
        context['address'] = address  # address是一个字典

    return render(request, 'user_center/user_center_site_edit.html', context)


# @user_login
# def address_delete(request, address_id):
#     try:
#         AddressInfo.objects.filter(id=address_id).delete()
#         msg = '删除成功'
#     except:
#         msg = '删除失败'
#
#     return redirect('/user/address/?msg=%s' % msg)   # 通过request.GET.get('msg)获取


@user_login
def address_delete(request):
    try:
        # 通过user_center_site中的delete函数来传參
        # html中： /?address_id=XXX    url中不用额外添加参数     view函数中通过request.GET.get('address_id')来获取参数
        address_id = request.GET.get('address_id')
        AddressInfo.objects.filter(id=address_id).delete()
    except Exception:
        pass

    return redirect('/user/address')


def address_default(request, address_id):
    try:
        address = AddressInfo.objects.get(id=address_id)

        # 如果当前地址是默认地址就取消
        if address.def_address:
            address.def_address = False
            address.save()
        # 如果不是默认地址，现将所有地址的默认取消掉，再将当前选中的设置为默认
        else:
            address_list = AddressInfo.objects.filter(user_id=request.session.get('uid'))  # 这里相当于获取了所有的地址对象
            # address_list = AddressInfo.objects.all()  # 这种方法和上面的效果一样
            for item in address_list:
                item.def_address = False
                item.save()
            address.def_address = True
            address.save()

        msg = '设置成功'
    except Exception:
        msg = '设置失败'

    return redirect('/user/address/?msg=%s' % msg)


def is_login(request):
    login = False
    if request.session.has_key('uid'):
        login = True
    return JsonResponse({'isLogin': login})


def order(request):
    uid = request.session['uid']
    current_page = int(request.GET.get('current', '1'))  # 分页显示,注：分页插件到页数只有一页的时候是不显示的

    order_list = OrderMain.objects.filter(user_id=uid).order_by('-order_date')

    paginator = Paginator(order_list, 2)
    page = paginator.page(current_page)

    context = {'title':'用户中心', 'page':page}
    return render(request, 'user_center/user_center_order.html', context)