import jsonpickle
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from cartapp.cartmanager import SessionCartManager
from userapp.models import UserInfo, Area, Address
from utils.code import gene_code


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 获取请求参数
        uname = request.POST.get('account', '')
        pwd = request.POST.get('password', '')
        # 注册用户信息
        try:
            user = UserInfo.objects.get(uname=uname, pwd=pwd)
            return render(request, 'register.html')
        except UserInfo.DoesNotExist:
            user = UserInfo.objects.create(uname=uname, pwd=pwd)
            # 将注册的用户对象存入session中,session中无法直接存入对象，使用jsonpickle序列化成json格式
            request.session['user'] = jsonpickle.dumps(user)
        return redirect('/user/center/')


def center_view(request):
    return render(request, 'center.html')


class LoginView(View):
    def get(self, request):
        # 标识登录的来源页面，方便登录后跳转到购物车页面
        reflag = request.GET.get('reflag', '')
        return render(request, 'login.html', {'reflag': reflag})

    def post(self, request):
        # 获取请求参数
        uname = request.POST.get('account', '')
        pwd = request.POST.get('password', '')

        # 获取登录后跳转页面标识，是否来自于购物车页面的登录
        reflag = request.POST.get('reflag', '')

        # 判断是否登录成功
        user = UserInfo.objects.filter(uname=uname, pwd=pwd)
        if user:
            request.session['user'] = jsonpickle.dumps(user[0])

            # 将session中的购物项目存放到数据库
            SessionCartManager(request.session).migrateSession2DB()

            if reflag == 'cart':
                return redirect('/cart/queryAll/')

            return redirect('/user/center/')

        return redirect('/user/login/')


class LoadCodeView(View):
    def get(self, request):
        # 获取图片验证码
        img, code = gene_code()
        request.session['session_code'] = code
        return HttpResponse(img, content_type='image/png')  # content_type指定图片的渲染格式


class CheckCodeView(View):
    def get(self, request):
        # 获取请求参数
        code = request.GET.get('code', -1)
        # 获取session中生成的验证码
        session_code = request.session.get('session_code', '')
        # 判断是否相等
        vflag = False
        if code == session_code:
            vflag = True
        # 返回响应
        return JsonResponse({'vflag': vflag})


class LogoutView(View):
    def post(self, request):
        # 清空session中所有数据
        request.session.flush()
        # 返回响应
        return JsonResponse({'logout': True})


class AddressView(View):
    def get(self, request):
        # 获取当前登录用户下的收货地址信息
        # 获取当前登录用户对象
        user_str = request.session.get('user', '')
        if user_str:
            # 将session数据转换成对象
            user = jsonpickle.loads(user_str)
        addr_list = user.address_set.all()
        return render(request, 'address.html', {'addr_list': addr_list})

    def post(self, request):
        # 获取请求参数
        aname = request.POST.get('aname', '')
        aphone = request.POST.get('aphone', '')
        addr = request.POST.get('addr', '')
        # 获取当前登录用户对象
        user_str = request.session.get('user', '')
        if user_str:
            # 将session数据转换成对象
            user = jsonpickle.loads(user_str)

        # 插入数据库表
        # 从 一的模型 查找 多的模型通过 '多的模型小写名_set' 查找
        # lambda参考onenote笔记
        Address.objects.create(aname=aname, aphone=aphone, addr=addr, userinfo=user,
                               isdefault=(lambda count: True if count == 0 else False)(user.address_set.count()))
        return redirect('/user/address/')


def load_area_view(request):
    # 获取请求参数
    pid = request.GET.get('pid', -1)
    pid = int(pid)
    area_list = Area.objects.filter(parentid=pid)
    # 序列化数据
    jarea_list = serialize('json', area_list)
    return JsonResponse({'jarea_list': jarea_list})


def update_default_addr_view(request):
    # 获取请求参数
    addr_id = request.GET.get('addrid', -1)
    addr_id = int(addr_id)
    # 修改数据
    Address.objects.filter(id=addr_id).update(isdefault=True)
    Address.objects.exclude(id=addr_id).update(isdefault=False)
    return redirect('/user/address/')


def del_addr_view(request):
    # 获取请求参数
    addr_id = request.GET.get('addrid', -1)
    addr_id = int(addr_id)
    # 删除数据
    Address.objects.get(id=addr_id).delete()
    return redirect('/user/address/')
