from libs.http import render_json
from .logic import send_verify_code, gen_verify_code
from django.http import HttpResponse


def get_verify_code(request):
    """手机注册"""
    phonenum = request.GET.get('phonenum')
    # send_verify_code(phonenum,gen_verify_code())
    return render_json(phonenum, 0)


def login(request):
    """短信验证码登录"""
    pass


def get_profile(request):
    """获取个人资料"""
    pass


def modify_profile(request):
    """修改个人资料"""
    pass


def upload_avatar(request):
    """头像上传"""
    pass
