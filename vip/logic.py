from common import error
from libs.http import render_json


def perm_require(perm_name):
    """权限检查装饰器"""
    def deco(view_func):
        def wrap(request):
            user = request.user
            if user.vip.has_perm(perm_name):
                response = view_func(request)
                return response
            else:
                return render_json(None, error.NOT_HAS_PERM)
        return wrap
    return deco


