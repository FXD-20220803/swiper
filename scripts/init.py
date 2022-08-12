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


# 创建初始用户
for i in range(100):
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
