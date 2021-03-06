# Generated by Django 3.0.3 on 2020-03-08 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('areaid', models.IntegerField(primary_key=True, serialize=False)),
                ('areaname', models.CharField(max_length=50)),
                ('parentid', models.IntegerField()),
                ('arealevel', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
            options={
                'db_table': 'area',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=100)),
                ('pwd', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aname', models.CharField(max_length=30, verbose_name='收货人')),
                ('aphone', models.CharField(max_length=11, verbose_name='收货人手机号')),
                ('addr', models.CharField(max_length=100, verbose_name='收货人地址')),
                ('isdefault', models.BooleanField(default=False, verbose_name='是否是默认收货地址')),
                ('userinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.UserInfo')),
            ],
        ),
    ]
