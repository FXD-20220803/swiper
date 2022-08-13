import logging
from libs.http import render_json

from social import logic
from social.models import Friend
from vip.logic import perm_require

log = logging.getLogger('inf')


def get_users(request):
    """获取推荐列表"""
    group_num = int(request.GET.get('group_num', 0))
    start = group_num * 5
    end = start + 5
    users = logic.get_rcmd_users(request.user)[start:end]  # 切片，惰性加载
    result = [user.to_dict() for user in users]
    return render_json(result)


def like(request):
    """喜欢"""
    sid = int(request.POST.get('sid'))
    is_matched = logic.like(request.user, sid)
    log.info(f'{request.user.id} like {sid}')
    return render_json({'is_matched': is_matched})


# perm_require('superlike')(superlike)(request)
@perm_require('superlike')
def superlike(request):
    """超级喜欢"""
    sid = int(request.POST.get('sid'))
    is_matched = logic.superlike(request.user, sid)
    log.info(f'{request.user.id} superlike {sid}')
    return render_json({'is_matched': is_matched})


def dislike(request):
    """不喜欢"""
    sid = int(request.POST.get('sid'))
    logic.dislike(request.user, sid)
    log.info(f'{request.user.id} 不喜欢 {sid}')
    return render_json(None)


@perm_require('rewind')
def rewind(request):
    """反悔"""
    sid = int(request.POST.get('sid'))
    logic.rewind(request.user, sid)
    log.info(f'{request.user.id} rewind {sid}')
    return render_json(None)


def friends(request):
    """查询好友"""
    my_friends = Friend.friends(request.user.id)
    friends_info = [friend.to_dict() for friend in my_friends]
    return render_json({'friends': friends_info})
