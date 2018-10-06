import datetime
import random

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from cart.models import CartInfo
from order.models import OrderMain, OrderDetail
from user_center.models import AddressInfo


def checkout(request):
    """
    结算入口
    :param request:
    :return:
    """
    cart_id_list = request.POST.getlist('cart_id')  # 注：getlist(),cart_id是for循环中的商品id
    context = {'title':'提交订单'}
    uid = request.session['uid']
    address_list = AddressInfo.objects.filter(user_id=uid)
    context['address_list'] = address_list

    # 获取的是CartInfo对象，要获取具体的商品信息还要通过在html中通过外键来获取
    cart_list = CartInfo.objects.filter(id__in=cart_id_list)
    context['cart_list'] = cart_list

    context['cart_id_list'] = ','.join(cart_id_list)

    return render(request, 'order/place_order.html', context)


def random_str(default_len=6):
    str = ''
    chars = '0123456789'
    for i in range(default_len):  # int类型数据不可迭代，需要加上range
        str += chars[random.randint(0, (len(chars) - 1))]

    return str


@transaction.atomic
def order_handle(request):
    # 可以通过request.POST.get来获取名为 xxx 的input标签的value值,前提是所有的元素都在表单内且表单以post或者get方式提交
    """
    对ordermain数据的处理
    :param request:
    :return:
    """
    address_id = request.POST.get('address')  # 默认提交的地址
    cart_id_list = request.POST.get('cart_id_list').split(',')
    sp = transaction.savepoint()

    try:
        order = OrderMain()
        order.address_id = address_id

        now_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        order.id = "%s%s" %(now_str, random_str())

        order.user_id = request.session['uid']
        order.save()

        """
        对orderdetail表数据的处理
        """
        list = CartInfo.objects.filter(id__in=cart_id_list)
        total = 0  # 总价
        for cart in list:
            if cart.count <= cart.goods.inventory:
                detail = OrderDetail()
                detail.goods = cart.goods
                detail.order = order
                detail.count = cart.count
                detail.price = cart.goods.price * detail.count # 一项商品的购物记录难道不要乘上它的数量？？？
                detail.save()

                goods = cart.goods
                goods.inventory -= cart.count
                goods.save()

                cart.delete()  # 订单每样商品处理结束后删除
                total += detail.price + 10
            else:
                raise Exception()
        order.total = total
        order.save()
        transaction.savepoint_commit(sp)
        return redirect('/user/order/')
    except Exception:
        transaction.savepoint_rollback(sp)
        return redirect('/cart/checkout/')



