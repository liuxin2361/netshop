"""
全局上下文
"""
import jsonpickle


def get_login_user_info(request):
    """
    获取登录用户对象信息
    :param request: 请求
    :return:
    """
    user = request.session.get('user', '')
    if user:
        # json数据转成字典
        user = jsonpickle.loads(user)

    return {'login_user': user}
