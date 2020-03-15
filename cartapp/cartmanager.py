# coding=utf-8

from collections import OrderedDict

import jsonpickle
from django.db.models import F

from cartapp.models import CartItem


class CartManager(object):
    def add(self, goodsid, colorid, sizeid, count, *args, **kwargs):
        """添加商品，如果商品已经存在就更新商品的数量(self.update())，否则直接放到购物车"""
        pass

    def delete(self, goodsid, colorid, sizeid, *args, **kwargs):
        """删除一个购物项"""
        pass

    def update(self, goodsid, colorid, sizeid, count, step, *args, **kwargs):
        """更新购物项的数据,添加减少购物项数据"""
        pass

    def queryAll(self, *args, **kwargs):
        """:return CartItem  多个购物项"""
        pass


# 当前用户未登录
class SessionCartManager(CartManager):
    cart_name = 'cart'

    def __init__(self, session):
        self.session = session
        # 创建购物车 #  {cart:{key1:cartitem,key2:cartitem}}
        # request.session['cart']['key1']
        if self.cart_name not in self.session:
            self.session[self.cart_name] = OrderedDict()

    def __get_key(self, goodsid, colorid, sizeid):
        # 1,1,1
        return goodsid + ',' + colorid + ',' + sizeid

    def add(self, goodsid, colorid, sizeid, count, *args, **kwargs):

        # 获取购物项的唯一标示
        key = self.__get_key(goodsid, colorid, sizeid)

        # session   {'cart':{key1:item}}
        # session('cart',[{key1:cartitem,key2:cartitem}])
        if key in self.session[self.cart_name]:
            self.update(goodsid, colorid, sizeid, count, *args, **kwargs)
        else:
            self.session[self.cart_name][key] = jsonpickle.dumps(
                CartItem(goods_id=goodsid, color_id=colorid, size_id=sizeid,
                         count=count))

    def delete(self, goodsid, colorid, sizeid, *args, **kwargs):

        key = self.__get_key(goodsid, colorid, sizeid)
        if key in self.session[self.cart_name]:
            del self.session[self.cart_name][key]

    def update(self, goodsid, colorid, sizeid, step, *args, **kwargs):

        key = self.__get_key(goodsid, colorid, sizeid)
        if key in self.session[self.cart_name]:
            # 反序列化成CartItem对象
            cartitem = jsonpickle.loads(self.session[self.cart_name][key])
            cartitem.count = int(str(cartitem.count)) + int(step)
        else:
            raise Exception('SessionManager中的update出错了')

    def queryAll(self, *args, **kwargs):
        cartitem_list = []
        # 反序列化
        for c in self.session[self.cart_name].values():
            cartitem_list.append(jsonpickle.loads(c))
        return cartitem_list

    def migrateSession2DB(self):
        if 'user' in self.session:
            user = jsonpickle.loads(self.session.get('user'))
            # 此时cartitem为self.add()序列化CartItem后的数据，所以cartitem中为goods_id，color_id，size_id
            for cartitem in self.queryAll():
                # 如果数据库中没有session中的数据
                if CartItem.objects.filter(goods_id=cartitem.goods_id, color_id=cartitem.color_id,
                                           size_id=cartitem.size_id).count() == 0:
                    cartitem.user = user
                    cartitem.save()
                # 数据库中存在session中的商品，则在数据库中商品数量的基础上在加上session中商品的数量
                else:
                    item = CartItem.objects.get(goods_id=cartitem.goodsid, color_id=cartitem.colorid,
                                                size_id=cartitem.sizeid)
                    item.count = int(item.count) + int(cartitem.count)
                    item.save()

            del self.session[self.cart_name]


# 用户已登录
class DBCartManger(CartManager):
    def __init__(self, user):
        self.user = user

    def add(self, goodsid, colorid, sizeid, count, *args, **kwargs):

        if self.user.cartitem_set.filter(goods_id=goodsid, color_id=colorid, size_id=sizeid).count() == 1:
            self.update(goodsid, colorid, sizeid, count, *args, **kwargs)
        else:
            CartItem.objects.create(goods_id=goodsid, color_id=colorid, size_id=sizeid, count=count, user=self.user)

    def delete(self, goodsid, colorid, sizeid, *args, **kwargs):
        self.user.cartitem_set.filter(goods_id=goodsid, color_id=colorid, size_id=sizeid).update(count=0, isdelete=True)

    def update(self, goodsid, colorid, sizeid, step, *args, **kwargs):
        self.user.cartitem_set.filter(goods_id=goodsid, color_id=colorid, size_id=sizeid).update(
            count=F('count') + int(step), is_delete=False)

    def queryAll(self, *args, **kwargs):
        return self.user.cartitem_set.order_by('id').filter(is_delete=False).all()

    def get_cartitems(self, goodsid, sizeid, colorid, *args, **kwargs):
        """获取当前用户下的所有购物项"""
        return self.user.cartitem_set.get(goods_id=goodsid, size_id=sizeid, color_id=colorid)


# 工厂方法
# 根据当前用户是否登录返回相应的CartManger对象
def getCartManger(request):
    if request.session.get('user'):
        # 当前用户已登录
        return DBCartManger(jsonpickle.loads(request.session.get('user')))
    return SessionCartManager(request.session)
