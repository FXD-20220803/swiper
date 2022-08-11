# Django项目开发

## 一. git 创建项目

**添加ssh密钥**

```
swiper
 |- .gitignore (创建的python项目忽略文件)
 |- LICENSE
 |- README.md (项目的入门手册)
```

> README.md文件是一个项目的入门手册，里面介绍了整个项目的使用、功能等等。所以README文件写得好不好，关系到这个项目能不能更容易的被其他人了解和使用。
> README至少要写明项目的功能和使用，这是最基本的，当然，一个好的README想要的不仅仅是功能和使用方法。好的项目都会有README，这已经是一个约定了。
> md是Markdown的缩写，其实READEME就是使用Markdown编写的。README既然是为了让别人了解你这个项目，那么应该如何编写？
> 国际化：
> 我们都知道GitHub一般都是使用英语，所以可以的话最好写两个版本，一个是英文，为了所有人能看懂，另一个是中文，为了我们更好的理解。
> 项目名及简介：
> 简单介绍一下这个项目是做什么的。有的话最好加上demo地址。
> 功能：
> 你这个项目可以实现的功能。
> 用法：
> 这可以说是最重要的，一定要让别人看得懂你这项目是怎么使用的。
> 其他：
> 作者或者是维护人列表、版权、鸣谢、贡献、logo、联系方式等等，这些有的话当然会更加高大上。 

## 二. 创建虚拟环境

+ 在项目路径下用命令行创建（**使用麻烦**）

```
windows：
python -m venv .venv （1.创建虚拟环境）
.venv/Scripts/activate （2.激活虚拟环境）
--------------------------------------------
mac/linux：
python -m venv .venv （1.创建虚拟环境）
source .venv/Scripts/activate （2.激活虚拟环境）
```

+ 直接用Pycharm创建（**使用方便**）

> 勾选下面这个选项（这样每次打开项目不用激活虚拟环境）
>
> - [x] Make available to all projects
>
> ```
> where python/where pip 查找python和pip的位置
> 如果pip使用的还是全局变量的，使用下面的方法
> .venv\Scripts\python.exe -m pip list
> .venv\Scripts\python.exe -m pip install -r requirement.txt
> ```

## 三. 安装Python包

```
pip install django redis gunicorn gevent celery ipython
```

将环境的包导入**requirements.txt**文件

```
pip freeze > requirements.txt
```

## 四. 创建Django项目

```
在下一级创建项目：
django-admin startproject swiper
在当前目录创建项目：
django-admin startproject swiper ./
```

项目结构：

```
swiper
 |- .venv/
 |- swiper/
 |- .gitignore
 |- LICENSE
 |- manage.py
 |- README.md
 |- requirement.txt
```

## 五. 创建user应用

```
manage.py startapp user
```

项目结构：

```
swiper
 |- .venv/
 |- swiper/
 |- user/
 |- .gitignore
 |- LICENSE
 |- manage.py
 |- README.md
 |- requirement.txt
```

```
进入ipython调试环境：
manage.py shell
```

#### user模块结构：

```
user
 |- migrations/
 |- __init__.py
 |- api.py
 |- apps.py
 |- logic.py
 |- models.py
 |- tests.py
```

###  1. models创建

#### @property(描述符) 的使用

```python
class Box:
    def __init__(self):
        self.length = 123
        self.width = 10
        self.height = 80

    def volume(self):
        return self.length * self.width * self.height


b = Box()
v = b.volume()
print("体积为：", v)

"""修改:@property将类方法属性化，并且为只读"""


class Box:
    def __init__(self):
        self.length = 123
        self.width = 10
        self.height = 80

    @property
    def volume(self):
        return self.length * self.width * self.height


b = Box()
print("体积为：", b.volume)
```

#### 构建User模型

`models.py`

```python
from django.db import models
import datetime
from django.utils.functional import cached_property


class User(models.Model):
    """用户数据模型"""
    SEX = (
        ('男', '男'),
        ('女', '女'),
    )
    nickname = models.CharField(max_length=32, unique=True)
    phone = models.CharField(max_length=16, unique=True)

    sex = models.CharField(max_length=8, choices=SEX)
    avatar = models.CharField(max_length=256)
    location = models.CharField(max_length=32)
    birth_year = models.IntegerField(default=2000)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)

    # @property
    @cached_property  # django提供的缓存装饰器，相比于property的优势是，如果对象相同，类方法只执行一次。
    def age(self):
        today = datetime.date.today()
        birth_date = datetime.date(self.birth_year, self.birth_month, self.birth_day)
        times = today - birth_date
        return times.days // 365

    @property
    def profile(self):
        """用户的配置项"""
        # if '_profile' not in self.__dict__:
        # 这样的话查询只需要执行一次，用类属性记住，只要self还在就不会消失
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(id=self.id)  # 如果没有，则创建
        return self._profile


class Profile(models.Model):
    """用户配置项"""

    SEX = (
        ('男', '男'),
        ('女', '女'),
    )
    dating_sex = models.CharField(default="女", max_length=8, choices=SEX, verbose_name='匹配的性别')
    location = models.CharField(max_length=32, verbose_name='目标城市')

    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最大查找范围')

    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=45, verbose_name='最大交友年龄')

    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_match = models.BooleanField(default=True, verbose_name='不让未匹配的人看我的相册')
    only_play = models.BooleanField(default=True, verbose_name='是否自动播放视频')
```

#### settings设置

`settings.py`

```python
ALLOWED_HOSTS = ['*']

# 不需要的就删掉
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'common.middleware.CorsMiddleware' # 有问题
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # 目前可有可无
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
```

> `/user/admin.py` 也可以删掉

#### 表迁移

```
manage.py makemigrations
manage.py migrate
```

#### `__dict__`（类字典）

> 包含了这个对象中的所有属性和属性值：`{key:value,key:value,key:value}`

#### `hasattr(obj,attr)`

> 检查obj对象中是否有attr属性，相当于 
>
> ```python
> value = hasattr(obj,attr)
> value = True if attr not in obj.__dict__ else False
> ```

#### 使用shell来进行models的调试

> 这样做的好处是不用等所有代码都写完再进行调试，这样比较高效

#### cached_property

```python
from django.utils.functional import cached_property
@cached_property  # django提供的缓存装饰器，相比于property的优势是，如果对象相同，类方法只执行一次。
```

### 2. api (views)编写

+ 可以将 `views.py` 改为 `api.py`，更直观，这些文件可以随便命名。

+ 新增一个写逻辑代码的文件 `logic.py`。

+ 新建一个`config.py`文件，来放与Django本身无关的配置，不影响Django。

#### 短信验证码

阿里云短信验证码：

##### `swiper/config.py`

```python
"""
第三方配置
"""

# 阿里云短信配置
ALI_SMS_PARAMS = {'AccessKeyId': 'LTAI5tN3SSefoMm8fGwnZzni',
                  'AccessKeySecret': 'rJCzRj0K8V8nck0OjVlxAgWv5juFWO',
                  'sign_name': '阿里云短信测试',
                  'template_code': 'SMS_154950909',
                  'phone_numbers': '',
                  'template_param': '',  # '{"code":"1234"}'
                  }
```

#### `user/api.py`

```python
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
```

#### 缓存和session

```python
cache.set(key, vcode, 1800)  # 设置缓存
saved_vcode = cache.get(key)  # get缓存

request.session['uid'] = user.id  # 设置session
```

#### `user/logic.py`

```python
import random

from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from django.core.cache import cache

from swiper.config import ALI_SMS_PARAMS
from worker import call_by_worker


def gen_verify_code(length=6):
    return random.randrange(10 ** (length - 1), 10 ** length)


@call_by_worker
def send_verify_code(phonenum):
    """异步发送验证码"""
    vcode = gen_verify_code()
    key = 'VerifyCode-%s' % phonenum
    cache.set(key, vcode, 1800)
    sms_cfg = ALI_SMS_PARAMS.copy()
    sms_cfg['phone_numbers'] = phonenum
    sms_cfg['template_param'] = '{"code":"%s"}' % vcode
    response = Sample.main(sms_cfg)
    return response


def check_vcode(phonenum, vcode):
    """检查验证码是否正确"""
    key = 'VerifyCode-%s' % phonenum
    saved_vcode = cache.get(key)
    return str(saved_vcode) == str(vcode)


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的 AccessKey ID,
            access_key_id=access_key_id,
            # 您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def main(
            args: dict,
    ):
        client = Sample.create_client(args.get('AccessKeyId'), args.get('AccessKeySecret'))
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name=args.get('sign_name'),
            template_code=args.get('template_code'),
            phone_numbers=args.get('phone_numbers'),
            template_param=args.get('template_param')
        )
        runtime = util_models.RuntimeOptions()
        # 复制代码运行请自行打印 API 的返回值
        response = client.send_sms_with_options(send_sms_request, runtime)
        return response.body.code


if __name__ == '__main__':
    send_verify_code('17835699470')
```

## 六. celery

#### celery模块结构：

```
worker
 |- __init__.py
 |- config.py
```

`__init__.py`

```python
import os
from celery import Celery

# 1. 设置环境变量，加载 Django 的 settings
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper.settings')


# 2. 创建 Celery Application
celery_app = Celery('swiper')
celery_app.config_from_object('worker.config')  # 3. 加载celery配置文件
celery_app.autodiscover_tasks()  # 4. 自动发现通过装饰器定义的所有任务


def call_by_worker(func):
    """将任务在 Celery 中异步执行, 只需要将此函数作为装饰器使用，就可以免去一些频繁的操作"""
    task = celery_app.task(func)
    # task.delay 将task加到异步任务里面
    return task.delay
```

`config.py`

```
# 配置代理人，指定代理人将任务存到哪里,这里是redis的0号库
broker_url = 'redis://127.0.0.1:6379/0'
broker_pool_limit = 1000

# 设置时区，默认UTC
timezone = 'Asia/Shanghai'
# using serializer name
accept_content = ['pickle', 'json']

task_serializer = 'pickle'

result_backend = 'redis://127.0.0.1:6379/1'
result_serializer = 'pickle'
result_cache_max = 10000  # 任务结果最大缓存数量
result_expires = 3600  # 任务结果的过期时间

worker_redirect_stdouts_level = 'INFO'
```

```
windows：
celery -A task worker --loglevel=info -P eventlet
linux/mac
celery -A task worker --loglevel=info
task：celery任务模块名
```

> 会遇到的问题：
>
> 1. 启动celery没有 tasks 列表没有任务，Celery没有扫描到Django里的所有函数，解决方法：将任务所在模块的路由添加上。
> 2. Windows系统celery启动任务不执行，解决方法：将celery启动命令行加上 -P eventlet。
> 3. 调试celery时，使用Shell，方便快捷。

https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#using-celery-with-django

#### 装饰器

```python
@celery_app.task
def add(x, y):
	return x + y
--装饰器就是函数，将装饰的函数作为参数执行以后的返回值赋值给相同的函数名--
add = celery_app.task(add)
```

```python
def deco(func):
    def wrap(*args, **kwargs):
        r = func(*args, **kwargs)
        return r

    return wrap


def bar(x, y):
    return x * y


@deco
def par(x, y):
    return x * y


@deco
def par1(x, y):
    return x * y
------------------------
bar
Out[5]: <function __main__.bar(x, y)>
par
Out[6]: <function __main__.deco.<locals>.wrap(*args, **kwargs)>
par1
Out[7]: <function __main__.deco.<locals>.wrap(*args, **kwargs)>
bar = deco(bar)
bar
Out[9]: <function __main__.deco.<locals>.wrap(*args, **kwargs)>
```

## 七. libs模块

> 新建一个library包，用来存放偏底层的一些方法

### 1. `http.py`

+ `render_json` ：将接口返回进行包装

```python
import json

from django.conf import settings
from django.http import HttpResponse


def render_json(data, code=0):
    result = {
        'code': code,
        'data': data
    }
    if settings.DEBUG:
        # 如果为DEBUG模式，正常输出json格式，如果不是DEBUG，压缩后输出
        json_str = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)  # indent 缩进，sort_keys 排序
    else:
        json_str = json.dumps(result, ensure_ascii=False, separators=[',', ':'])
    return HttpResponse(json_str)

```

## 八. common模块添加

> 通常用的一些文件

### 1. `middleware.py`

+ `CorsMiddleware`：不重要，一般是前端解决（这里处理的有问题）。
+ `AuthMiddleware`：认证中间件，省去每次调用接口的认证操作。

```python
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
            if request.path.startwith(path):  # path在request.path的开头或等于
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

```

> `settings.py` 添加

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 安全中间件
    # 'common.middleware.CorsMiddleware' # 有问题
    'django.contrib.sessions.middleware.SessionMiddleware',  # session中间件
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # 目前可有可无
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.AuthMiddleware',  # 认证中间件，放到后面
]
```

### 2. `error.py`

> 一些错误的值
>
> ```python
> VCODE_ERROR = 1000
> ```

### 3. `orm.py`

> `orm`相关的方法: 

+ `ModelMixin`
  + `to_dict`：将 model 对象转化为 dict

#### 多态

```shell
  ...: class Animal:
  ...:     def run(self):
  ...:         print('Animal running')
  ...: 
  ...: class Lion:
  ...:     def run(self):
  ...:         print('Lion running')
  ...: 
  ...: class Tiger:
  ...:     def run(self):
  ...:         print('Tiger running')
  ...: 
  ...: class LeoTiger(Lion, Tiger):
  ...:     pass
  ...: cub = LeoTiger()
isinstance(cub,Lion)
Out[3]: True
isinstance(cub,Tiger)
Out[4]: True
LeoTiger.mro()
Out[5]: [__main__.LeoTiger, __main__.Lion, __main__.Tiger, object]
```

#### 多继承

+ 方法和属性的继承顺序：`cls.mro()`

+ 菱形继承问题：

```
继承关系示意
菱形继承
	A.foo()
  /   \
 B     C.foo()
  \   /
	D.foo()  # 方法的继承顺序，由 C3 算法得到
```

+ `Mixin`：通过单纯的mixin类完成功能组合，所有继承的类的功能不会有任何的交叉
  + 继承的所有的父类之间没有任何的方法和属性有重合
  + 继承的所有的父类仅用来继承使用，父类自身不会创建任何实例

> `self._meta.fields`，将对象的类属性列出来（不包括之后设置的对象属性）
>
> `field.attname`，循环上面的属性，用attname展示出来
>
> `obj.__dict__`，将obj的属性和属性值以字典形式列出来
>
> `getattr(obj, attr)`，获取obj对象的attr属性的值
>
> `setattr(obj, attr, value)`，设置obj对象的attr属性值为value
>
> `hasattr(obj, attr)`，判断obj对象有没有attr属性，如果有为True，否则为Flase

`ModelMixin`

```python
class ModelMixin:
    def to_dict(self):
        """将 model 对象转化为 dict"""
        data = {}
        for field in self._meta.fields:
            name = field.attname
            # value = self.__dict__[name]  # 这个方法偏底层
            value = getattr(self,name)
            data[name] = value
        return data
```

`models.py`

```python
from libs.orm import ModelMixin
class Profile(models.Model, ModelMixin):
    """用户配置项"""
	...
---------shell---------
profile = Profile.objects.last()
profile.to_dict()
Out[10]: 
{'id': 2,
 'dating_sex': '女',
 'location': '',
 'min_distance': 1,
 'max_distance': 10,
 'min_dating_age': 18,
 'max_dating_age': 45,
 'vibration': True,
 'only_match': True,
 'only_play': True}
```
