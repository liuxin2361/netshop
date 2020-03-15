from django.db import models

# Create your models here.
from goodsapp.models import Color, Size, Goods
from userapp.models import UserInfo


class CartItem(models.Model):
    goods_id = models.PositiveIntegerField()
    color_id = models.PositiveIntegerField()
    size_id = models.PositiveIntegerField()
    count = models.PositiveIntegerField(default=0)
    is_delete = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def get_color(self):
        return Color.objects.get(id=self.color_id)

    def get_size(self):
        return Size.objects.get(id=self.size_id)

    def get_goods(self):
        return Goods.objects.get(id=self.goods_id)

    def get_total_price(self):
        # 转成int型，避免未登录情况下由于数据类型不一致导致页面总价显示错误
        return int(self.get_goods().price) * int(self.count)
