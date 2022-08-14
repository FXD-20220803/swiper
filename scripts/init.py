#!/user/bin/env python
# 指导这个脚本怎么执行
import os
import sys
import random

import django

# 设置环境，加载 Django 环境
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper.settings')
django.setup()

# 如果没有上面环境的配置，下面的 User 不会被加载
from user.models import User
from vip.models import Permission, Vip, VipPermRelation

last_names = ('赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨'
              '朱秦尤许何吕施张孔曹严华金魏陶姜'
              '戚谢邹喻柏水窦章云苏潘葛奚范彭郎'
              '鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
              '费廉岑薛雷贺倪汤滕殷罗毕郝邬安常')

first_names = {
    'Male': [
        '昊然', '坤曜', '英达', '木槿', '天钧', '华茂', '高轩', '琪琛',
        '承天', '光辉', '天宇', '兴国', '宸浩', '润玉', '斯辰', '文哲',
        '白草', '欧辰', '承志', '暮词', '俊邈', '阳锦', '黎杉', '鸿畅',
        '俊语', '玉书', '林古', '清嘉', '戕仪', '景曜', '昕晖', '宾鸿',
    ],
    'Female': [
        '宛梦', '沛玲', '紫雯', '婕娇', '冉甯', '淇汐', '嫦曦', '静璇',
        '晓梅', '思涵', '妍玲', '妍青', '莎诗', '淇甄', '瑜菱', '依静',
        '绮芙', '娣童', '鸿碧', '紫霜', '金琳', '陈红', '平墐', '焉雨',
        '中颖', '咪渲', '萱梓', '姝晶', '凡淇', '南媛', '雪华', '婕鸣',
    ]
}


def random_name():
    last_name = random.choice(last_names)
    sex = random.choice(['Male', 'Female'])
    first_name = random.choice(first_names[sex])
    return ''.join([last_name, first_name]), sex


def creat_robots(n):
    # 创建初始用户
    for i in range(n):
        while True:
            name, sex = random_name()
            try:
                User.objects.get(nickname=name)  # 存在重新循环选名字
                continue
            except User.DoesNotExist:  # 不存在使用此名字
                break
        User.objects.create(
            phonenum='%s' % random.randrange(21000000000, 21900000000),
            nickname=name,
            sex=sex,
            birth_year=random.randint(1980, 2000),
            birth_month=random.randint(1, 12),
            birth_day=random.randint(1, 28),
            location=random.choice(['北京', '上海', '深圳', '广州', '西安', '成都', '沈阳', '武汉']),
        )
        print('created: %s %s' % (name, sex))


def init_permission():
    """创建初始权限"""
    permissions = [
        'vipflag',
        'superlike',
        'rewind',
        'anylocation',
        'unlimit_like',
    ]
    for name in permissions:
        perm, _ = Permission.objects.get_or_create(name=name)
        print('created permission %s' % perm.name)


def init_vip():
    for i in range(4):
        vip, _ = Vip.objects.get_or_create(
            name='会员-%d' % i,
            level=i,
            price=i * 5.0
        )
        print('created %s' % vip.name)


def create_vip_perm_relation():
    """创建 Vip 和 Permission 的关系"""
    # 获取VIP
    vip1 = Vip.objects.get(level=1)
    vip2 = Vip.objects.get(level=2)
    vip3 = Vip.objects.get(level=3)

    # 获取权限
    vipflag = Permission.objects.get(name='vipflag')
    superlike = Permission.objects.get(name='superlike')
    rewind = Permission.objects.get(name='rewind')
    anylocation = Permission.objects.get(name='anylocation')
    unlimit_like = Permission.objects.get(name='unlimit_like')

    # 给 VIP 1 分配权限
    VipPermRelation.objects.get_or_create(vip_id=vip1.id, perm_id=rewind.id)
    VipPermRelation.objects.get_or_create(vip_id=vip1.id, perm_id=superlike.id)

    # 给 VIP 2 分配权限
    VipPermRelation.objects.get_or_create(vip_id=vip2.id, perm_id=superlike.id)
    VipPermRelation.objects.get_or_create(vip_id=vip2.id, perm_id=rewind.id)
    VipPermRelation.objects.get_or_create(vip_id=vip2.id, perm_id=unlimit_like.id)

    # 给 VIP 3 分配权限
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=vipflag.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=superlike.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=rewind.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=anylocation.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=unlimit_like.id)


if __name__ == '__main__':
    # creat_robots(100)
    init_permission()
    init_vip()
    create_vip_perm_relation()
