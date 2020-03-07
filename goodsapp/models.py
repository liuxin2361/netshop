from django.db import models


# Create your models here.

class Category(models.Model):
    """
    类别表
    """
    cname = models.CharField(max_length=10, verbose_name='类别名称')

    def __str__(self):
        return self.cname


class Goods(models.Model):
    """
    商品表
    """
    gname = models.CharField(max_length=100, verbose_name='商品名称')
    gdesc = models.CharField(max_length=100, verbose_name='商品描述')
    oldprice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='原价')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='现价')
    # CASCADE级联删除，Category表中的数据被删除时，Goods表中关联数据也删除
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='类别ID')

    def __str__(self):
        return self.gname

    def get_img_url(self):
        """
        获取商品图片地址
        :return: 返回对应商品的图片地址
        """
        # 从一的模型查找多的模型
        # 通过'多的模型小写名_set'查找
        return self.inventory_set.first().color.colorurl

    def get_colours(self):
        """
        获取商品的颜色
        :return: 返回商品的颜色列表
        """
        colors = []
        for inventory in self.inventory_set.all():
            color = inventory.color
            if color not in colors:
                colors.append(color)
        return colors

    def get_sizes(self):
        """
        获取商品尺寸
        :return: 返回商品的尺寸列表
        """
        sizes = []
        for inventory in self.inventory_set.all():
            size = inventory.size
            if size not in sizes:
                sizes.append(size)
        return sizes

    # {'参数规格':['url'], '整体款式'：['url'], '模特实拍':['url1','url2',...]}
    def get_detail_info(self):
        datas = {}
        for detail in self.goodsdetail_set.all():
            # 获取详情名称
            detail_name = detail.get_detail_name()
            # 判断detail_name是否在字典中存在
            if detail_name not in datas:
                datas[detail_name] = [detail.gdurl]
            else:
                datas[detail_name].append(detail.gdurl)
        return datas


class GoodsDetailName(models.Model):
    """
    详情名称表
    """
    gdname = models.CharField(max_length=30, verbose_name='详情名称')

    def __str__(self):
        return self.gdname


class GoodsDetail(models.Model):
    """
    商品详情表
    """
    gdurl = models.ImageField(upload_to='', verbose_name='详情图片地址')
    detailname = models.ForeignKey(GoodsDetailName, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)

    def __str__(self):
        # 返回的是表GoodsDetailName中的gdname
        return self.detailname.gdname

    def get_detail_name(self):
        return self.detailname.gdname


class Size(models.Model):
    """
    尺寸表
    """
    sname = models.CharField(max_length=10, verbose_name='尺寸名称')

    def __str__(self):
        return self.sname


class Color(models.Model):
    """
    颜色表
    """
    colorname = models.CharField(max_length=10, verbose_name='颜色名称')
    colorurl = models.ImageField(upload_to='color/', verbose_name='颜色图片地址')

    def __str__(self):
        return self.colorname


class Inventory(models.Model):
    """
    库存表
    """
    count = models.PositiveIntegerField(verbose_name='库存数量')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    def __str__(self):
        return self.count
