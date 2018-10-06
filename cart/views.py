import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from cart.models import CartInfo
from user_center.utils import user_login


@user_login
def cart(request):
    uid = request.session['uid']
    list = CartInfo.objects.filter(user_id=uid)
    context = {'title': '购物车', 'list': list}
    return render(request, 'cart/cart.html', context)


def add_goods(request):
    is_add = False
    try:
        uid = request.session['uid']
        gid = request.GET.get('gid')

        # 问题：如果数据中的相同用户购买了相同商品，那么就应该只改变商品数据的数量而不新加数据
        # 问题2：界面显示购物项的数量问题
        list = CartInfo.objects.filter(user_id=uid, goods_id=gid)
        gcount = int(request.GET.get('count', '1'))  # gcount是从输入框输入的数字
        if len(list) > 0:
            # 对已经存在的商品数量当点击购物车时 +1
            cart = list[0]
            cart.count += gcount
        else:
            # 添加新的购物项
            cart = CartInfo()
            cart.id = uuid.uuid1()  # id作为主键不能重复，因此用uuid来随机生成
            cart.user_id = uid
            cart.goods_id = gid
            cart.count = gcount

        cart.save()

        # 添加结果、数量（更改界面中购物车的数量）:显示当前用户对应的购物项数量
        is_add = True
        count = CartInfo.objects.filter(user_id=uid).count()

        return JsonResponse({'isAdd': is_add, 'count': count})
    except Exception:
        return JsonResponse({'isAdd': is_add})


def count(request):
    # 检查用户的购物项数量，当未登录时，购物车中数量为0,登录之后直接显示用户的购买商品的数量
    count = 0
    if request.session.has_key('uid'):
        uid = request.session['uid']
        count = CartInfo.objects.filter(user_id=uid).count()
    return JsonResponse({'count': count})


def edit(request):
    id = request.GET.get('id')
    count = request.GET.get('count')
    result = False
    try:
        Cart = CartInfo.objects.get(id=id)
        Cart.count = count
        Cart.save()
        result = True
        return JsonResponse({'result':result})
    except Exception:
        return JsonResponse({'result':result})


def del_goods(request):
    result = False

    id = request.GET.get('id')
    list = CartInfo.objects.filter(id=id)
    if len(list) == 1:
        list[0].delete()
        result = True

    return JsonResponse({'result':result})


