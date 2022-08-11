from libs.http import render_json
from .logic import send_verify_code, check_vcode
from common import error
from user.models import User


def get_verify_code(request):
    """手机注册"""
    phonenum = request.GET.get('phonenum')
    send_verify_code(phonenum)
    return render_json(phonenum, 0)


def login(request):
    """短信验证码登录"""
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vode')
    if check_vcode(phonenum, vcode):
        # 获取用户
        user, created = User.objects.get_or_create(phonenum=phonenum)

        # 记录登陆状态
        request.session['uid'] = user.id
        return render_json(user.to_dict(), 0)
    else:
        return render_json(phonenum, error.VCODE_ERROR)


def get_profile(request):
    """获取个人资料"""
    pass


def modify_profile(request):
    """修改个人资料"""
    pass


def upload_avatar(request):
    """头像上传"""
    pass
