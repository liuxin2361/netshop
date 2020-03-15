import jsonpickle
from django.shortcuts import render

# Create your views here.
from cartapp.cartmanager import DBCartManger


def to_order_view(request):
    cartitems = request.GET.get('cartitems', '')
    user = request.session.get('user', '')

    # 获取支付总金额
    total_price = request.GET.get('totalPrice', '')

    # 判断当前用户是否登录
    if not user:
        return render(request, 'login.html', {'reflag': 'order', 'cartitems': cartitems, 'total_price': total_price})
        # return redirect('/user/login/?reflag=order&cartitems=' + cartitems)

    # 反序列化cartitems
    # [{'goodsid':'1', 'sizeid':'2','colorid':'3'},{'goodsid':'1', 'sizeid':'3','colorid':'2'}]
    cartitem_list = jsonpickle.loads(cartitems)

    # 获取默认收货地址
    user = jsonpickle.loads(user)
    addr = user.address_set.get(isdefault=True)

    # 获取订单商品内容
    # [CartItem(), CartItem()]
    cartItemObj_list = [DBCartManger(user).get_cartitems(**item) for item in cartitem_list if item]

    return render(request, 'order.html',
                  {'cartItemObj_list': cartItemObj_list, 'total_price': total_price, 'addr': addr})
