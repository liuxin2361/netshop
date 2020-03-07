from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.views import View

from goodsapp.models import Category, Goods


class IndexView(View):

    def get(self, request, category_id=16, page=1):
        """
        首页信息的get请求
        :param page: 页码
        :param category_id: 默认页面显示的类别
        :param request:
        :return:
        """
        # 1.获取所有商品的类型信息
        category_list = Category.objects.all().order_by('id')
        # 2.获取某个类别下的所有商品信息
        goods_list = Goods.objects.filter(category_id=category_id).order_by('id')
        # 3.对商品添加分页功能
        paginator = Paginator(goods_list, settings.PER_PAGE_NUMBER)
        # 获取指定page的商品对象
        page_goods = paginator.get_page(page)
        # 4.添加页码数,显示10个页码
        start = page - int(10 / 2)
        start = start if start > 1 else 1
        end = start + (10 - 1)
        end = end if end < paginator.num_pages else paginator.num_pages
        page_list = range(start, end + 1)

        return render(request, 'index.html',
                      {'category_list': category_list, 'goods_list': page_goods, 'current_category': category_id,
                       'page_list': page_list})


def recommend(func):
    """
    recommend装饰器，实现猜你喜欢功能
    :param func: 被装饰函数名称
    :return:
    """
    def _wrapper(detail_view, request, goods_id, *args, **kwargs):
        # 将goods_id转成string型，方便后续存入cookie
        goods_id_str = str(goods_id)
        # 获取cookie中的goods_id_list
        c_goods_id = request.COOKIES.get('c_goods_id', '')
        # 存放用户访问过的商品ID列表
        goods_id_list = [id for id in c_goods_id.split() if id.strip()]
        # 存放用户访问过的商品对象列表,取前4个;
        goods_list = [Goods.objects.get(id=g_id) for g_id in goods_id_list if
                      g_id != goods_id_str and Goods.objects.get(id=g_id).category_id == Goods.objects.get(
                          id=goods_id).category_id][:4]
        # 将当前商品ID放入访问过的商品ID列表中的第一位
        if goods_id_str in goods_id_list:
            goods_id_list.remove(goods_id_str)
        goods_id_list.insert(0, goods_id_str)
        # 调用视图方法，视图方法返回一个response对象
        response = func(detail_view, request, goods_id, recommend_list=goods_list, *args, **kwargs)
        # 将用户访问过的商品ID列表转成字符串存放至cookie中,['1','2','3'] -> '1 2 3',有效期3天
        response.set_cookie('c_goods_id', ' '.join(goods_id_list), max_age=3 * 24 * 60 * 60)
        return response

    return _wrapper


class DetailView(View):

    # 使用装饰器对get方法添加新功能
    @recommend
    def get(self, request, goods_id, recommend_list=[]):
        """
        商品详情的get请求
        :param recommend_list: 猜你喜欢中推荐的商品列表
        :param request:
        :param goods_id: 商品id
        :return:
        """
        # 根据商品id获取商品详细信息
        try:
            goods = Goods.objects.get(id=goods_id)
        except Goods.DoesNotExist:
            raise Http404
        return render(request, 'detail.html', {'goods': goods, 'recommend_list': recommend_list})
