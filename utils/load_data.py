import json

from django.db.transaction import atomic

from goodsapp.models import *


# 使用事务注解
@atomic
def load_data():
    """
    读取json文件中的数据导入到数据库中
    :return:
    """
    with open('utils/jiukuaijiu.json') as fr:
        datas = json.loads(fr.read())
        for data in datas:
            # 向商品类别表中插入数据
            cate = Category.objects.create(cname=data['category'])
            _goods = data['goods']
            for goods in _goods:
                good = Goods.objects.create(gname=goods['goodsname'], gdesc=goods['goods_desc'],
                                            oldprice=goods['goods_oldprice'], price=goods['goods_price'],
                                            category=cate)

                sizes = []
                for _size in goods['sizes']:
                    if Size.objects.filter(sname=_size[0]).count() == 1:
                        size = Size.objects.get(sname=_size[0])
                    else:
                        size = Size.objects.create(sname=_size[0])
                    sizes.append(size)

                colors = []
                for _color in goods['colors']:
                    color = Color.objects.create(colorname=_color[0], colorurl=_color[1])
                    colors.append(color)

                for _spec in goods['specs']:
                    try:
                        goods_details = GoodsDetailName.objects.get(gdname=_spec[0])
                    except GoodsDetailName.DoesNotExist:
                        goods_details = GoodsDetailName.objects.create(gdname=_spec[0])
                    for img in _spec[1]:
                        GoodsDetail.objects.create(gdurl=img, detailname=goods_details, goods=good)

                for c in colors:
                    for s in sizes:
                        Inventory.objects.create(count=100, color=c, size=s, goods=good)


def delete_all():
    """
    删除数据库表中所有数据
    :return:
    """
    Category.objects.filter().delete()
    Color.objects.filter().delete()
    Size.objects.filter().delete()
