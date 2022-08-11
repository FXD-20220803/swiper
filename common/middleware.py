from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

from common import error
from libs.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    """用户登录认证"""
    WHITE_LIST = [
        'api/user/verify',
        'api/user/login',
    ]

    def process_request(self, request):
        # 如果请求的url开头在白名单内，直接跳过检查
        for path in self.WHITE_LIST:
            if request.path.startswith(path):  # path在request.path的开头或等于
                return
        # 进行登陆检查
        uid = request.session.get('uid')
        if uid:
            try:
                request.user = User.objects.get(id=uid)
                return
            except User.DoesNotExist:
                request.session.flush()  # 清空session
        return render_json(None, code=error.LOGIN_ERROR)


class CorsMiddleware(MiddlewareMixin):
    """处理客户端 JS 的跨域"""

    def process_request(self, request):
        if request.method == 'OPTIONS' and 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = HttpResponse()
            response['Content-Length'] = '0'
            response['Access-Control-Allow-Headers'] = request.META
            ['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']
            response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000'
            return response

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
