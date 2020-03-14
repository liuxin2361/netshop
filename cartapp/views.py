from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from cartapp.cartmanager import getCartManger


class CartView(View):
    def post(self, request):
        # 获取用户当前操作类型
        flag = request.POST.get('flag', '')
        if flag == 'add':
            cart_manger = getCartManger(request)
            # request.POST是一个类字典对象，通过 .dict()转换成字典对象
            cart_manger.add(**request.POST.dict())
        elif flag == 'plus':
            cart_manger = getCartManger(request)
            # {'flag':'plus', 'goodsid':1,...}
            cart_manger.update(step=1, **request.POST.dict())
        elif flag == 'minus':
            cart_manger = getCartManger(request)
            cart_manger.update(step=-1, **request.POST.dict())
        return redirect('/cart/queryAll/')


class CartListView(View):
    def get(self, request):
        # 获取cartManager对象
        cart_manger = getCartManger(request)
        cart_item_list = cart_manger.queryAll()
        return render(request, 'cart.html', {'cart_item_list': cart_item_list})
