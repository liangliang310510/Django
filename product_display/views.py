from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from haystack.generic_views import SearchView

from product_display.models import TypeInfo, GoodsInfo


def index(request):
    types = TypeInfo.objects.filter(delete=False)

    # 方式一：用sql语句查询
    # for type in types:
    #     # 点击量排名前三
    #     hot_goods = GoodsInfo.objects.raw('select * from product_display_goodsinfo whrer type_id=%d order by click desc limit 3;' %type.id)
    #     # 最新商品排名前四
    #     new_goods = GoodsInfo.objects.raw('select * from product_display_goodsinfo whrer type_id=%d order by id desc limit 4;' %type.id)

    type_goods = []
    # 方式二：
    for type in types:
        hot_goods = type.goodsinfo_set.order_by('-click')[0:3]
        new_goods = type.goodsinfo_set.order_by('-id')[0:4]
        type_goods.append({'type':type, 'hot_goods':hot_goods,'new_goods':new_goods})

    context = {'title':'首页', 'product':True, 'types':types, 'type_goods':type_goods}
    return render(request, 'product_display/index.html', context)


def product_list(request, type_id, current_page):  # 通过形參(形參名字可以随便起，但位置和类型要与html中的顺序对应)来传递参数， html中： product_list_{{ item.type.id }}    urls中：  /^product_list_(\d+)$/      views函数中：product_list(request, type_id)
    current_type = TypeInfo.objects.get(id=type_id)  # 获取从index.html中选中的id对应的种类
    types = TypeInfo.objects.filter(delete=False)

    new_goods = current_type.goodsinfo_set.order_by('-id')[0:2]
    order_by = request.GET.get('order_by', '-id')
    goods_list = current_type.goodsinfo_set.order_by(order_by)

    paginator = Paginator(goods_list, 10)
    page = paginator.page(current_page)

    context = {'title':'商品列表','product':True, 'current_type':current_type, 'types':types, 'new_goods':new_goods, 'order_by':order_by, 'page':page}
    return render(request, 'product_display/list.html', context)


def detail(request, product_id):

    # 获取网页所需要的变量
    goods = GoodsInfo.objects.get(id=product_id)
    types = TypeInfo.objects.filter(delete=False)
    new_goods = GoodsInfo.objects.filter(type_id=goods.type_id).order_by('-id')[0:2]

    # 浏览历史记录

    context = {'title':'商品详情', 'product':True, 'types':types, 'details':True, 'current_type':goods.type, 'goods':goods, 'new_goods':new_goods}
    response = render(request, 'product_display/detail.html', context)

    '''
        需求分析：
        需要记录用户的浏览历史（点击量的更新）（记录一周）
        记录——存储记录：cookie（为什么？）
        获取记录：用户中心

        存储什么内容，使用什么格式
        key：value：：：key='history'  value='pid,pid,pid....' id数量5个
        id需要按顺序排列：最近浏览数据排在第一位，到5个id后，如果有新加入的，需要删除最后一个

        操作步骤：
        1、获取cookie中history信息，并对值进行处理（按,分割数据）
        2、将最新的浏览商品id插入到id的容器中，位置要求第一位
        3、判断插入数据后的容器长度，超过5，删除最后一个
        4、将最新的浏览记录信息设置到cookie中（需要将数据转换成','分割字符串，cookie中设置存储时间）
        
        注意：
        每点击一次就会触发下列时间以此，所以goods的点击量就要增加一次
    '''
    if request.COOKIES.get('history', '') == '':
        history = []
    else:
        history = request.COOKIES.get('history', '').split(',')

    # 如果id重复了，从列表中删除
    if product_id in history:
        history.remove(product_id)

    history.insert(0, product_id)

    if len(history) > 5:
        history.pop()

    response.set_cookie('history', ','.join(history), max_age=60*60*24*7)

    # 点击量更新
    goods.click += 1
    goods.save()

    return response


# 怎么指向模板文件的？？？  url会根据urls.py中的路径中查找指定的网页的路径，如果没有设置template_name的话，就回去haystack.urls中找，默认路径就是/search/search.html
class MySearchView(SearchView):  # 这里是对TemplateVieW中方法的重写,目的是为了设置context让html能够显示购物车模块
    # template_name = 'search/search_templates_view.html'
    def get_context_data(self, **kwargs):
        context = super(MySearchView, self).get_context_data(**kwargs)
        context['product'] = True
        return context
