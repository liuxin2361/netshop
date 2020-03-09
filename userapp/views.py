import jsonpickle
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from userapp.models import UserInfo
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
        return render(request, 'login.html')

    def post(self, request):
        # 获取请求参数
        uname = request.POST.get('account', '')
        pwd = request.POST.get('password', '')

        # 判断是否登录成功
        user = UserInfo.objects.filter(uname=uname, pwd=pwd)
        if user:
            request.session['user'] = jsonpickle.dumps(user[0])
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
