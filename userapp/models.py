# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Area(models.Model):
    areaid = models.IntegerField(primary_key=True)
    areaname = models.CharField(max_length=50)
    parentid = models.IntegerField()
    arealevel = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'area'


class UserInfo(models.Model):
    uname = models.CharField(max_length=100)
    pwd = models.CharField(max_length=100)

    def __str__(self):
        return self.uname


class Address(models.Model):
    aname = models.CharField(max_length=30, verbose_name='收货人')
    aphone = models.CharField(max_length=11, verbose_name='收货人手机号')
    addr = models.CharField(max_length=100, verbose_name='收货人地址')
    isdefault = models.BooleanField(default=False, verbose_name='是否是默认收货地址')
    userinfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.aname
