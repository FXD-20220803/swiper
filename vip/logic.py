import logging

from common import error
from libs.http import render_json

log = logging.getLogger('err')


def perm_require(perm_name):
    """权限检查装饰器"""

    def deco(view_func):
        def wrap(request):
            user = request.user
            # 判断用户是否有perm_name这个权限，如果有权限正常执行函数并返回值，如果没有权限则返回错误
            if user.vip.has_perm(perm_name):
                response = view_func(request)
                return response
            else:
                log.error(f'{request.user.nickname} not has {perm_name}')
                return render_json(None, error.NOT_HAS_PERM)

        return wrap

    return deco
