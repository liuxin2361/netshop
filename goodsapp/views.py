from django.shortcuts import render

# Create your views here.
from django.views import View

from goodsapp.models import Category, Goods


class IndexView(View):

    def get(self, request, category_id=16):
        """
        :param category_id: 默认页面显示的类别
        :param request:
        :return:
        """
        # 1.获取所有商品的类型信息
        category_list = Category.objects.all().order_by('id')
        # 2.获取某个类别下的所有商品信息
        goods_list = Goods.objects.filter(category_id=category_id)
        return render(request, 'index.html',
                      {'category_list': category_list, 'goods_list': goods_list, 'current_category': category_id})
