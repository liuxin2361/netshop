from django.db import models

# Create your models here.
from userapp.models import Address, UserInfo


class Order(models.Model):
    out_trade_num = models.UUIDField()  # 交易凭证
    order_num = models.CharField(max_length=50)  # 订单号
    trade_no = models.CharField(max_length=20, default='')  # 验证凭证
    status = models.CharField(max_length=20, default='待支付')
    payway = models.CharField(max_length=20, default='alipay')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_num


class OrderItem(models.Model):
    goods_id = models.PositiveIntegerField()
    color_id = models.PositiveIntegerField()
    size_id = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
