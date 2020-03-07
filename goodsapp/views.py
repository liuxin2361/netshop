from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.views import View

from goodsapp.models import Category, Goods


class IndexView(View):

    def get(self, request, category_id=16, page=1):
        """
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
