import uuid
from datetime import datetime

import jsonpickle
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from cartapp.cartmanager import DBCartManger
from goodsapp.models import Inventory
from orderapp.models import Order, OrderItem
from userapp.models import Address
from utils.alipay_p3 import AliPay


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


alipayObj = AliPay(appid='', app_notify_url='http://127.0.0.1:8000/order/checkPay/',
                   app_private_key_path='orderapp/keys/my_private_key.txt',
                   alipay_public_key_path='orderapp/keys/my_public_key.txt',
                   return_url='http://127.0.0.1:8000/order/checkPay/', debug=True)


def to_pay_view(request):
    # 获取请求参数
    addr_id = request.GET.get('address', -1)
    payway = request.GET.get('payway', 'alipay')
    cartitems = request.GET.get('cartitems', '')
    out_trade_num = uuid.uuid4().hex
    order_num = datetime.now().strftime("%Y%m%d%H%M%S")
    address = Address.objects.get(id=addr_id)
    user = jsonpickle.loads(request.session.get('user', ''))

    order = Order.objects.create(out_trade_num=out_trade_num, order_num=order_num, payway=payway, address=address,
                                 user=user)

    # '[{'':'','':'',},{},...]
    if cartitems:
        # [{'':'','':'',},{},...]
        cartitems = jsonpickle.loads(cartitems)
        orderitem_list = [OrderItem.objects.create(order=order, goods_id=cartitem.goodsid, color_id=cartitem.colorid,
                                                   size_id=cartitem.sizeid, count=cartitem.count) for cartitem in
                          cartitems if cartitem]

    url_param = alipayObj.direct_pay(subject='购物商城', out_trade_no=order.out_trade_num,
                                     total_amount=request.GET.get('totalPrice', 0))

    url = alipayObj.gateway + '?' + url_param
    return redirect(url)


def check_pay_view(request):
    # 获取当前用户登录对象
    user = jsonpickle.loads(request.session.get('user', ''))

    # 获取请求参数
    params = request.GET.dict()

    # 获取sign的值
    sign = params.pop('sign')

    # 校验是否支付成功
    if alipayObj.verify(params, sign):
        # 修改订单状态
        order = Order.objects.get(out_trade_num=params.get('out_trade_no', ''))
        order.trade_no = params.get('trade_no', '')
        order.status = '代发货'
        order.save()

        # 修改库存
        orderitem_list = order.orderitem_set.all()
        [Inventory.objects.filter(goods_id=orderitem.goods_id, size_id=orderitem.size_id,
                                  color_id=orderitem.color_id).update(count=F('count') - orderitem.count) for orderitem
         in orderitem_list if orderitem]

        # 更新购物车表中数据
        [user.cartitem_set.filter(goods_id=orderitem.goods_id, color_id=orderitem.color_id,
                                  size_id=orderitem.size_id).delete()
         for orderitem in orderitem_list if orderitem]

        return HttpResponse('支付成功')

    return HttpResponse('支付失败')
