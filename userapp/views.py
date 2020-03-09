import jsonpickle
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from userapp.models import UserInfo


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
