import os
from django.core.cache import cache
from libs.http import render_json
from .forms import ProfileForm
from .logic import send_verify_code, check_vcode, save_upload_file
from common import error
from user.models import User
from django.conf import settings


def get_verify_code(request):
    """手机注册"""
    phonenum = request.GET.get('phonenum')
    send_verify_code(phonenum)
    return render_json(phonenum)


def login(request):
    """短信验证码登录"""
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vode')
    if check_vcode(phonenum, vcode):
        # 获取用户
        user, created = User.objects.get_or_create(phonenum=phonenum)
        # 记录登陆状态
        request.session['uid'] = user.id
        request.session.set_expiry(settings.SESSION_COOKIE_AGE)  # 设置过期时间
        return render_json(user.to_dict())
    else:
        return render_json(phonenum, error.VCODE_ERROR)


def get_profile(request):
    """获取个人资料"""
    user = request.user
    key = 'Profile-%s' % user.id
    # 从缓存获取
    user_profile = cache.get(key)
    if not user_profile:
        user_profile = user.profile.to_dict()
        cache.set(key, user_profile, settings.SESSION_COOKIE_AGE)
    return render_json(user_profile)


def modify_profile(request):
    """修改个人资料"""
    form = ProfileForm(request.POST)
    if form.is_valid():
        user = request.user
        user.profile.__dict__.update(form.cleaned_data)
        user.profile.save()  # 保存到数据库
        # 修改缓存
        key = 'Profile-%s' % user.id
        user_profile = user.profile.to_dict()
        cache.set(key, user_profile, settings.SESSION_COOKIE_AGE)
        return render_json(user_profile)
    else:
        return render_json(form.errors, error.PROFILE_ERROR)


def upload_avatar(request):
    """头像上传"""
    # 1. 接受用户上传的头像
    # 2. 定义用户头像名称
    # 3. 异步 将头像上传七牛
    # 4. 将URL保存入数据库
    file = request.FILES.get('avatar')
    if file:
        save_upload_file(request.user, file)
        return render_json(file.name)
    else:
        return render_json(None, error.FILE_NOT_FOUND)
