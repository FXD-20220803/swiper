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
source .venv/bin/activate （2.激活虚拟环境）或 source activate
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
pip install django redis gunicorn gevent celery ipython pymysql qiniu django_redis
```

```
pip install alibabacloud_dysmsapi20170525
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

## 五. user模块

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

> `property`第一个参数为实例本身`self`，所以类属性和实例属性都可以访问到。

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

#### `@classmethod` 和`@staticmethod` 区别

> 1. 语法区别
>    + 声明时： 
>      + `classmethod`的第一个参数为类本身(`cls`)，正如实例方法的第一个参数为对象本身(self);
>      + `staticmethod`第一个参数不需要传入`cls`或`self`，故`staticmethod`中是无法访问类和对象的数据的。
>    + 调用时：
>      + 都可用类名直接调用
>      + 也可用实例对象调用（不推荐，没必要）

```python
class A:
    z = 789

    def __init__(self):
        self.x = 123
        self.y = 456

    def foo1(self):
        print(self.x,self.y)

    @classmethod
    def foo2(cls):
        return cls.z

    @staticmethod
    def foo3():
        return 123

A.foo2()
Out[3]: 789
A.foo3()
Out[4]: 123
a = A()
a.foo2()
Out[6]: 789
a.foo3()
Out[7]: 123
```

> 2. 使用场景
>    + 两者特点：
>      + `classmethod`可以设置修改类属性；也可以实例化对象；
>      + `staticmethod`无法访问类或对象的数据，所以可把它当作一个辅助功能方法用，里面包含一些与该类有关的逻辑代码。比如`validate(*args)`
> 3. 实例
>    +  需求：从本地文件中`(txt, csv, json等等)`读取数据，生成一个对象。比如，本地有一个`data.json`文件，里面包含了每个学生的姓名及对应的考试成绩。现在要求读取该数据，生成一个class对象。 
>    + 思路
>      + `__init__`方法中，清晰的声明对象的属性
>      + 用一个`classmethod`：`load_json`，专门用于读取data_file，获取数据，实例化对象
>      + 用一个`staticmethod`：`validate`，来对要初始化数据进行有效性检查

```python
class Class:
    def __init__(self, names, grades):
        self._names = names
        self._grades = grades

    @classmethod
    def load_json(cls, data_file):
        # 读取数据,获得names,grades
        cls.validate(names，grades)
        return cls(names, grades)

    @staticmethod
    def validate(names, grades):
        # 检查数据有效性
        pass

data_file = {'names':'fanxinde','grades':11}
obj = Class.load_json(data_file)
obj
Out[14]: <__main__.Class at 0x25319575f70>
obj._names
Out[15]: 'fanxinde'
obj._grades
Out[16]: 11
```

加了一点

```python
class Class:
    def __init__(self, names, grades):
        self._names = names
        self._grades = grades

    def read_names(self):
        return self._names

    @property
    def read_grades(self):
        return self._grades

    @classmethod
    def load_json(cls, data_file):
        # 读取数据,获得names,grades
        names = data_file.get('names')
        grades = data_file.get('grades')
        cls.validate(names, grades)
        return cls(names, grades)

    @staticmethod
    def validate(names, grades):
        # 检查数据有效性
        pass

data_file = {'names':'fanxinde','grades':11}
obj = Class.load_json(data_file)
obj.read_names()
Out[20]: 'fanxinde'
obj.read_grades
Out[21]: 11
```

总结：

1. `property`装饰的方法 继承 `self`，将方法以**对象属性**的方式使用，方法返回一个值，即对象.方法直接得到值，不需要再加括号调用。
2. ` classmethod `装饰的方法继承`cls`，将方法变为**类方法**使用，不需要实例化，类可以直接使用，当然对象也可以使用，但就失去了意义。
3.  `staticmethod `装饰的方法不继承，将方法作为**类方法**使用， 不需要实例化，不访问类和对象的数据，当然对象也可以使用，但就失去了意义。
4. 继承 self 的都是实例化之后才能使用。

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

#### `swiper/config.py`

阿里云短信验证码：

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

```python
request.GET
request.POST
# 都是字典
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

> 缓存和session

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

#### `user/forms.py`

```python
from django import forms

from user.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['dating_sex', 'location', 'min_distance',
                  'max_distance', 'min_dating_age', 'max_dating_age',
                  'vibration', 'only_match', 'only_play']

```

> Form表单可以很方便的将前端传过来的`request.POST`字典数据进行校验，因为其通过Meta与model关联

```
form_obj.is_valid()  # 验证数据是否都正确
form_obj.errors  # 输出错误的字段及原因
form_obj.cleaned_data  # 将清洗后的数据以字典形式输出
form_obj.save()   # 将表单验证后的数据根据根据关联的model保存到数据库
```

> 表单例子👇

```python
class TestForm(Form):
   ...:     TAGS = (
   ...:         ('py', 'python'),
   ...:         ('ln', 'linux'),
   ...:         ('dj', 'django'),
   ...:     )
   ...:     fid = IntegerField()
   ...:     name = CharField(max_length=10)
   ...:     tag = ChoiceField(choices=TAGS)
   ...:     date = DateField()
   ...:     
POST = {'fid':'123','name':'sdfsdfsd','tag':'dj','date':'2017-01-01'}
form = TestForm(POST)
form.is_valid()
Out[14]: True

form.errors
Out[27]: {}

form.cleaned_data
Out[28]: 
{'fid': 123,
 'name': 'sdfsdfsd',
 'tag': 'dj',
 'date': datetime.date(2017, 1, 1)}
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
> 4. Linux的root账号启动不起来，需要 `export C_FORCE_ROOT="true"`

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

### 2. `orm.py`

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

### 3. `qncloud.py`

```python
from qiniu import Auth, put_file, etag
from swiper import config
from worker import call_by_worker

# 构建鉴权对象
qn = Auth(config.QN_ACCESSKEY, config.QN_SECRETKEY)


def upload_to_qiniu(localfile, key):
    """
    将本地文件上传到七牛云
    Args:
        localfile: 要上传文件的本地路径
        key: 上传到七牛后保存的文件名
    """
    bucket_name = config.QN_BUCKET_NAME  # 要上传的空间
    token = qn.upload_token(bucket_name, key, 3600)  # 生成上传 Token，可以指定过期时间等

    ret, info = put_file(token, key, localfile, version='v2')
    print(info)
    return ret, info


# 手动装饰一次，定义出异步上传到七牛云，为了不影响原来的方法，便于调试
async_upload_to_qiniu = call_by_worker(upload_to_qiniu)

```

### 4. `db.py`

> 对Django的models进行打补丁处理，来实现自动缓存的目的（暂时没使用）

```python
from django.core.cache import cache
from django.db import models


def get(cls, *args, **kwargs):
    """数据优先从缓存中获取，缓存中取不到再从数据库中获取"""
    # 创建 key
    pk = kwargs.get('pk') or kwargs.get('id')

    # 从缓存中获取
    if pk is not None:
        key = 'Model-%s-%s' % (cls.__name__, pk)
        model_pbj = cache.get(key)
        if isinstance(model_pbj, cls):
            return model_pbj

    # 缓存里面没有，直接从数据库获取，同时写入缓存
    model_pbj = cls.objects.get(*args, **kwargs)
    key = 'Model-%s-%s' % (cls.__name__, model_pbj.pk)
    cache.set(key, model_pbj)
    return model_pbj


def get_or_create(cls, *args, **kwargs):
    # 创建 key
    pk = kwargs.get('pk') or kwargs.get('id')

    # 从缓存中获取
    if pk is not None:
        key = 'Model-%s-%s' % (cls.__name__, pk)
        model_pbj = cache.get(key)
        if isinstance(model_pbj, cls):
            return model_pbj, False

    # 执行原生方法，并添加缓存
    model_pbj, created = cls.objects.save(*args, **kwargs)
    key = 'Model-%s-%s' % (cls.__name__, model_pbj.pk)
    cache.set(key, model_pbj)
    return model_pbj, created


def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    """存入数据库后，同时写入缓存"""
    # 原生的 save 以及被修改为了 _origin_save，所以实际上还是先用原生的save保存一下
    self._origin_save(force_insert=False, force_update=False, using=None, update_fields=None)
    key = 'Model-%s-%s' % (self.__class__.__name__, self.pk)
    cache.set(key, self)


def patch_model():
    """
    动态更新 Model 方法

    Model 在 Django 中是一个特殊的类，如果通过继承的方法来增加或修改原有方法，Django 会将
    继承的类识别为一个普通的 app.model，所以只能通过 monkey patch（猴子补丁） 的方式动态修改
    """
    # 动态添加一个类方法 get
    models.Model.get = classmethod(get)
    models.Model.get_or_create = classmethod(get_or_create)

    # 修改save，需要改一下原生的，不理解
    models.Model._origin_save = models.Model.save
    models.Model.save = save

```

需要在`swiper/_init_.py`文件导入

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
> VCODE_ERROR = 1000  # 验证码错误
> LOGIN_ERROR = 1001  # 登录错误
> PROFILE_ERROR = 1002  # 前端传入profile数据没有通过验证
> FILE_NOT_FOUND = 1003  # 上传的文件不存在
> NOT_HAS_PERM = 1004  # 用户没有该权限
> ```

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

## 九. 静态文件处理

> 1. 用户图片上传服务器
> 2. 服务器将图片上传到七牛云
> 3. 将七牛云返回的图片URL存入数据库

## 十. social模块

```
manage.py startapp social
or
python manage.py startapp social
```

**random包**

```python
random.randrange(1, 10)  # 左闭右开区间，不包含10
random.randint(1, 10)  # 左右闭区间，包含10
random.random()
random.choice(['a', 'b'])  # 从一个序列里面选择一个,可以是字符串
random.sample('123456789', 3)   # 采样，从里面随机三个，可以是字符串
l = ['4', '2', '6', '5', '1', '9', '7', '3', '8']
random.shuffle(l)  # 将l打乱，不能是字符串
```

### 1. `social/api.py`

```python
from libs.http import render_json

from social import logic
from social.models import Friend
from vip.logic import perm_require


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
    return render_json({'is_matched': is_matched})


# perm_require('superlike')(superlike)(request)
@perm_require('superlike')
def superlike(request):
    """超级喜欢"""
    sid = int(request.POST.get('sid'))
    is_matched = logic.superlike(request.user, sid)
    return render_json({'is_matched': is_matched})


def dislike(request):
    """不喜欢"""
    sid = int(request.POST.get('sid'))
    logic.dislike(request.user, sid)
    return render_json(None)


@perm_require('rewind')
def rewind(request):
    """反悔"""
    sid = int(request.POST.get('sid'))
    logic.rewind(request.user, sid)
    return render_json(None)


def friends(request):
    """查询好友"""
    my_friends = Friend.friends(request.user.id)
    friends_info = [friend.to_dict() for friend in my_friends]
    return render_json({'friends':friends_info})

```

### 2. `social/logic.py`

```python
import datetime

from social.models import Swiperd, Friend
from user.models import User


def get_rcmd_users(user):
    """获取推荐用户"""
    sex = user.profile.dating_sex
    location = user.profile.location
    min_age = user.profile.min_dating_age
    max_age = user.profile.max_dating_age

    current_year = datetime.date.today().year
    min_year = current_year - min_age
    max_year = current_year - max_age

    users = User.objects.filter(sex=sex, location=location,
                                birth_year__gte=max_year, birth_year__lte=min_year)
    return users


def like(user, sid):
    """喜欢一个用户"""
    Swiperd.mark(user.id, sid, 'like')
    # 检查被滑动的用户是否喜欢过自己
    if Swiperd.is_liked(uid=sid, sid=user.id):
        Friend.be_friends(uid1=user.id, uid2=sid)
        return True
    else:
        return False


def superlike(user, sid):
    """超级喜欢一个用户"""
    Swiperd.mark(user.id, sid, 'superlike')
    # 检查被滑动的用户是否喜欢过自己
    if Swiperd.is_liked(uid=sid, sid=user.id):
        Friend.be_friends(uid1=user.id, uid2=sid)
        return True
    else:
        return False


def dislike(user, sid):
    """不喜欢一个用户"""
    Swiperd.mark(user.id, sid, 'dislike')


def rewind(user, sid):
    """反悔"""
    try:
        # 取消滑动记录
        Swiperd.objects.get(uid=user.id, sid=sid).delete()
    except Swiperd.DoesNotExist:
        pass
    # 撤销好友关系
    Friend.break_off(user.id, sid)

```

### 3. `social/models.py`

```python
from django.db import models
from django.db.models import Q

from user.models import User


class Swiperd(models.Model):
    STATUS = (
        ('superlike', '超级喜欢'),
        ('like', '喜欢'),
        ('dislike', '不喜欢'),
    )
    uid = models.IntegerField(verbose_name='滑动者的 UID')
    sid = models.IntegerField(verbose_name='被滑动者的 UID')
    status = models.CharField(max_length=32, choices=STATUS)
    time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def mark(cls, uid, sid, status):
        """标记一次滑动"""
        if status in ['superlike', 'like', 'dislike']:
            defaults = {'status': status}
            cls.objects.update_or_create(uid=uid, sid=sid, defaults=defaults)

    @classmethod
    def is_liked(cls, uid, sid):
        """检查uid是否喜欢sid"""
        return cls.objects.filter(uid=uid, sid=sid,
                                  status__in=['superlike', 'like']).exists()


class Friend(models.Model):
    uid1 = models.IntegerField(verbose_name='用户1的 UID')
    uid2 = models.IntegerField(verbose_name='用户2的 UID')

    @classmethod
    def be_friends(cls, uid1, uid2):
        """成为好友"""
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        cls.objects.get_or_create(uid1=uid1, uid2=uid2)  # 如果有的话就会忽略掉

    @classmethod
    def is_friend(cls, uid1, uid2):
        """检查是否是好友"""
        condition = Q(uid1=uid1, uid2=uid2) | Q(uid1=uid2, uid2=uid1)
        return cls.objects.filter(condition).exists()

    @classmethod
    def break_off(cls, uid1, uid2):
        """断交"""
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        try:
            cls.objects.get(uid1=uid1, uid2=uid2).delete()
        except cls.DoesNotExist:
            pass

    @classmethod
    def friends(cls,uid):
        condition = Q(uid1=uid) | Q(uid2=uid)
        relations = cls.objects.filter(condition)  # 过滤出我的好友关系
        friend_id_list = []
        for r in relations:
            friend_id = r.uid2 if r.uid1 == uid else r.uid1
            friend_id_list.append(friend_id)
        return User.objects.filter(id__in=friend_id_list)

```

### 4. `swiper/settings.py`

```python
INSTALLED_APPS = [
	...
    'user',
    'social',
]
```

### 5. `swiper/urls.py`

```python
from social import api as social_api
urlpatterns = [
	...

    url('^api/social/users$', social_api.get_users),
    url('^api/social/like$', social_api.like),
    url('^api/social/superlike$', social_api.superlike),
    url('^api/social/dislike$', social_api.dislike),
    url('^api/social/rewind$', social_api.rewind),
]
```

## 十一. scripts模块

> 脚本文件
>
> 1. `init.py `：初始化一些数据和一些机器人数据。

### 1. `init.py `

```python
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
    VipPermRelation.objects.get_or_create(vip_id=vip1.id, perm_id=vipflag.id)
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
    # creat_robots(1000)
    init_permission()
    init_vip()
    create_vip_perm_relation()

```

## 十二. `vip`模块

### 1. `vip/logic.py`

```python
from common import error
from libs.http import render_json


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
                return render_json(None, error.NOT_HAS_PERM)
        return wrap
    return deco

```

### 2. `vip/models.py`

> 多对多需要三张表

```python
"""
Vip - User: 一对多
Vip - Permission: 一对多
"""

from django.db import models


class Vip(models.Model):
    """
    会员1
    会员2
    会员3
    """
    name = models.CharField(max_length=32, unique=True)
    level = models.IntegerField()
    price = models.FloatField()

    def perms(self):
        """当前 VIP 具有的所有权限"""
        relations = VipPermRelation.objects.filter(vip_id=self.id)
        perm_id_list = [r.perm_id for r in relations]
        return Permission.objects.filter(id__in=perm_id_list)

    def has_perm(self, perm_name):
        """检查这个会员等级是否有某种权限"""
        perm = Permission.objects.get(name=perm_name)
        return VipPermRelation.objects.filter(vip_id=self.id,perm_id=perm.id).exists()


class Permission(models.Model):
    """
    权限表
        vipflag 会员身份标识
        superlike 超级喜欢
        rewind 返回功能
        anylocation 任意更改定位
        unlimit_like 无限喜欢次数
    """

    name = models.CharField(max_length=32, unique=True)


class VipPermRelation(models.Model):
    """"
    会员权限关系表
    vip_id       perm_id
    会员身份标识  1      3
    超级喜欢      1  2   3
    返回功能         2   3
    任意更改定位         3
    无限喜欢次数     2   3
    """
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()

```

### 3. `swiper/settings.py`

```python
INSTALLED_APPS = [
	...
    'user',
    'social',
    'vip',
]
```

## 十三. logging配置

[Django配置](https://blog.csdn.net/zhouzhiwengang/article/details/119606262)

[logging模块使用](https://blog.csdn.net/weixin_41010198/article/details/89356417)

### `swiper/settings.py`

> simple：比较**简单**的日志信息格式，info Handler使用。
>
> verbose：比较**详细**的日志信息格式，error Handler使用。

```python
# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    # 格式配置
    'formatters': {
        'simple': {
            "format": '%(asctime)s %(module)s.%(funcName)s:%(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        'verbose': {
            "format": '%(asctime)s %(levelname)s [%(process)d-%(threadName)s] '
                      '%(module)s:%(funcName)s line %(lineno)d:%(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    # Handler 配置
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'class': 'logging.StreamHandler',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            ''
            'filename': os.path.join(BASE_DIR, 'logs/info.log'),  # 日志保存路径
            'when': "D",  # 每日切割日志
            'backupCount': 30,  # 日志保留30天
            'formatter': 'simple',
            'encoding': 'utf-8',  # 中文不乱码
        },
        "error": {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/error.log'),  # 日志保存路径
            'when': "W0",  # 每周切割日志
            'backupCount': 4,  # 日志保留4周
            'formatter': 'verbose',
            'encoding': 'utf-8',  # 中文不乱码
        }
    },
    # Logger 配置
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        "inf": {
            "level": "INFO",
            "handlers": ["info"],
            'propagate': True,
        },
        "err": {
            "level": "WARNING",
            "handlers": ["error"],
            'propagate': True,
        }
    }
}
```

## 十四. 缓存处理

> memcached
>
> + 操作
>   + set
>   + get
>   + incr
>   + decr
>   + watch
> + 优点：性能好
> + 缺点：无法做到数据持久化保存，只用到了内存，一旦宕机数据会全部消失。
>
> redis

[django cache](https://docs.djangoproject.com/en/4.1/topics/cache/)

[django session 配置](https://blog.csdn.net/weixin_42194215/article/details/111414823)

```
pip install django-redis
```

### `swiper/settings.py`

```python
# 使用 redis 做缓存
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/4',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PICKLE_VERSION': -1,
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",		# 将session设置在1号库中
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",
        }
    }
}
# session的存储配置
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'session'		# 上面 CACHES 中设置的名称
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 设置session失效时间为30天后, 单位为秒S
```

### 一般缓存处理流程

```python
from django.core.cache import cache

user_profile = cache.get(key)  # 首先从缓存中获取数据
if not user_profile:
    user_profile = user.profile.to_dict()  # 缓存中没有，从数据库中获取
    cache.set(key, user_profile)  # 将数据添加到缓存，方便下次获取
return render_json(user_profile)
```

### `swiper/_init_.py`

```python
from libs.db import patch_model

# 动态给原生的 Model 打补丁，需要抢在models代码加载之前加载，所以写在settings前面
patch_model()
```

## 十五. 分布式数据库

> 数据总量： 5000w
>
> 单台能力上限：500w
>
> 数据分片：sharding
>
> User表：
>
> user_0	  		1	-	500 w
>
> user_1	  500 w	-	1000 w
>
> user_2	1000 w	-	1500 w
>
> user_3	1500 w	-	2000 w
>
> user_4	2000 w	-	3500 w
>
> user_5	2500 w	-	3000 w
>
> user_6	3000 w	-	3500 w
>
> user_7	3500 w	-	4000 w
>
> user_8	4000 w	-	4500 w
>
> user_9	4500 w	-	5000 w



> user_0	  1		11		...
>
> user_1	  2		12		...
>
> user_2	  3		13		...
>
> user_3	  4	    14		...
>
> user_4	  5		15		...
>
> user_5	  6		16		...
>
> user_6	  7		17		...
>
> user_7	  8		18		...
>
> user_8	  9		19		...
>
> user_9	10		20		...
>
> ​	master	<-	写入
>
> ​	slave		->	读取
>
> ​	slave		->	读取
>
> ​	slave		->	读取
>
> 读写分离
>
> zookeeper

Django 配置mysql

```
pip install pymysql
```

### `swiper/settings`

```python
DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
            'NAME': 'swiper',  # 数据库名称
            'HOST': '82.157.36.220',  # 数据库地址
            'PORT': 3306,  # mysql端口
            'USER': 'root',  # 数据库用户名
            'PASSWORD': '123456',  # 数据库密码
        }
}
```

### `swiper/_init_.py`

```python
import pymysql
pymysql.install_as_MySQLdb()
```

## 十六. 压力测试与TCP

### ab (apache benchmark)

工具：[文档](https://httpd.apache.org/docs/2.4/)

### `centos` 安装

[ab 资料](https://www.136.la/nginx/show-99885.html)

[Apache Benchmark测试结果数据解析](https://blog.csdn.net/weixin_43180484/article/details/110048945)

```shell
sudo yum install httpd
sudo systemctl enable httpd
sudo systemctl start httpd
```

### 测试命令

```shell
curl http://127.0.0.1:8000/api/user/profile  # 检查链接是否
ab -n 1000 -c 100 http://127.0.0.1:8000/api/user/profile  # -n 请求1000次，-c 并发100次
```

```shell
[root@VM-20-5-centos ~]#ab -n 1000 -c 100 http://127.0.0.1:8000/api/user/profile
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        WSGIServer/0.2
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /api/user/profile
Document Length:        38 bytes

Concurrency Level:      100
Time taken for tests:   27.438 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      292000 bytes
HTML transferred:       38000 bytes
Requests per second:    36.45 [#/sec] (mean)	# 最重要：每秒的请求数，RPS
Time per request:       2743.766 [ms] (mean)
Time per request:       27.438 [ms] (mean, across all concurrent requests)
Transfer rate:          10.39 [Kbytes/sec] received

Connection Times (ms)
			  最小  平均  误差    中位	   最大	 # 中位数比较准确
              min  mean[+/-sd] median   max
Connect:        0   91 297.0      0    1060		# 网络连接环节占据时长
Processing:     5  464 2547.9     18   26377	# 网络处理环节占据时长
Waiting:        1  454 2548.8      8   26374	# 网络之间发生阻塞等待的时间
Total:          6  555 2728.3     18   27436	# 总的时间

Percentage of the requests served within a certain time (ms)
  50%     18
  66%     20
  75%     22
  80%     24
  90%     36
  95%   2730
  98%   7671
  99%  14133
 100%  27436 (longest request)
```

> HTTP 超文本传输协议：建立在TCP基础之上的，短连接协议，通信完一次以后就会断开，需要频繁的建立TCP连接。
>
> 
>
> TCP（缺点：慢）：
>
> + 三次握手（全双工）：
>
>   1. client	->	SYN			   ->	server
>   2. client	<-	ACK + SYN	<-	server
>   3. client	->	           ACK    ->	server
>
>   + SYN：请求建立联系
>   + ACK：应答

 SYN：同步序列编号（**Synchronize Sequence Numbers**）。是TCP/IP建立连接时使用的握手信号。在客户机和[服务器](https://baike.baidu.com/item/服务器/100571)之间建立正常的TCP网络连接时，客户机首先发出一个SYN消息，服务器使用SYN+ACK应答表示接收到了这个消息，最后客户机再以[ACK](https://baike.baidu.com/item/ACK/3692629)消息响应。这样在[客户机](https://baike.baidu.com/item/客户机/5168153)和服务器之间才能建立起可靠的TCP连接，数据才可以在客户机和服务器之间传递。 

ACK (**Acknowledge character**）即是确认字符，在数据通信中，接收站发给发送站的一种传输类[控制字符](https://baike.baidu.com/item/控制字符/6913704)。表示发来的数据已确认接收无误。在[TCP/IP协议](https://baike.baidu.com/item/TCP%2FIP协议)中，如果接收方成功的接收到数据，那么会回复一个ACK数据。通常ACK信号有自己固定的格式,长度大小,由接收方回复给发送方。

全双工 / 半双工

全双工：我和你发送数据，与你和我发送数据互不干扰的。比如有时候打电话，信号不好，你能听到我说话，我听不到你说话。

半双工：我和你发送数据时，你不能和我发送数据，因为他俩共用一个信道。

![1660561781370](python项目开发.assets/1660561781370.png)

## 十七. 多任务和高并发处理

### 多任务

+ 多进程：操作系统
  + 多线程
    + 多协程

|      | 资源占用                 | 通信方式                                                    | 上下文切换性能                                               |
| ---- | ------------------------ | ----------------------------------------------------------- | ------------------------------------------------------------ |
| 进程 | 大，一般以Mb为单位       | 需要一种媒介来进行通信socket，如：管道，文件，共享内存，UDS | 稍慢，需要保存大量的变量，不够灵活，由操作系统控制，被迫的切换 |
| 线程 | 很小，一般为2k左右       | 直接通信，非常方便                                          | 稍快，不够灵活，由Python解释器控制切换                       |
| 协程 | 资源占用更小，一般不到1k | 直接通信，非常方便                                          | 非常好，非常灵活，切换方式由开发者掌控                       |

上下文切换：

单核电脑

时间片

time --------------------------------------------------------------------------------------------------

x+=1

A  ----->			  ----------> 			  ----------> 			  ----------> 			  ---------->   

​			|			^ 			|			^ 			|			^ 			|			^  					频繁的进行 

​			v			|			 v			|			  v			|			 v			|					 上下文切换

B		  --------->		  	--------->		  		--------->		  		--------->

​			y-=3

寄存器 / 一级、二级、三级缓存 / 内存 / 硬盘 ：容量越来越大，速度越来越慢。



高效上下文切换：

x+=1

A  ----->			  ----------> ---------> ----------> ---------> ----------> --------->  

​			|			^ 																					 |	通知机制 I/O event			 

​			v			|			 																		 v				

B		  --------->		  																				--------->

​			s.recv()阻塞

多路复用：select / poll / epoll（event poll）

Input	   ：write()

Output	：read()

Unix：一切皆文件

设备 / 文件 / 网络 的操作都是 IO 操作

事件驱动

nginx		4万以上

redis		11万次操作/秒

tornado	5000 ~ 8000 rps



阻塞：多任务异步处理

上下文切换：使用尽可能快的处理单元

### 协程

Python 协程发展

+ stackless / greenlet / gevent：第三方
+ tornado：通过纯 Python 代码实现了协程处理（底层使用 yield）
+ asyncio：Python 官方实现的协程

协程关键字：async / await

asyncio 实现协程：

```python
import asyncio


async def foo(n):
    for i in range(n):
        print(f'我是{i}')
        await asyncio.sleep(i)
    return i


t1 = foo(10)

t2 = foo(7)

tasks = [asyncio.ensure_future(t1),
         asyncio.ensure_future(t2),
         ]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
```

### 全局解释器锁（GIL）

![1660580958521](python项目开发.assets/1660580958521.png)

+ 它确保任何时候一个进程中都只有一个 Python 线程能进入 CPU 执行。
+ 全局解释器锁造成单个进程无法使用多个 CPU 核心。
+ 通过多线程利用多个 CPU 核心，一般进程数与CPU核心数相等，或者CPU核心数两倍。

### 结论

>  通常使⽤多进程 + 多协程达到最⼤并发性能

+ 因为 GIL 的原因, Python 需要通过多进程来利⽤多个核⼼ 

+ 线程切换效率低, ⽽且应对 I/O 不够灵活 

+ 协程更轻量级，完全没有协程切换的消耗，⽽且可以由程序⾃身统⼀调度和切换 

+ HTTP Server 中，每⼀个请求都由独⽴的协程来处理

## 十八. Gunicorn

> g-green，unicorn-独角兽

```
pip install gunicorn gevent
```

### 使用 Gunicorn 驱动 Django

+ [Gunicorn文档](https://docs.gunicorn.org/en/stable/index.html)

+ Gunicorn 扮演 HTTPServer 的⻆⾊ 

+ HTTPServer: 只负责⽹络连接 (TCP握⼿、数据收/发)

|      ip       |                          内网                          |
| :-----------: | :----------------------------------------------------: |
|  `127.0.0.1`  |                        本地回环                        |
|  `10.x.x.x`   | 内部组织的一些网络，网段、ip地址范围更多一些，适合公司 |
| `172.16.x.x`  |               内部子网，比10少，比192多                |
| `192.168.x.x` |                          最少                          |

###  `swiper/gunicorn.conf.py `

```python
from multiprocessing import cpu_count

bind = ["127.0.0.1:9000"]  # 线上环境不会开启在公网 IP 下，一般使用内网 IP
daemon = True  # 是否开启守护进程模式
pidfile = 'logs/gunicorn.pid'

workers = cpu_count()*2
worker_class = "gevent"  # 指定一个异步处理的库
worker_connections = 65535

keepalive = 60  # 服务器保持连接的时间，能够避免频繁的三次握手过程
timeout = 30
graceful_timeout = 10
forwarded_allow_ips = '*'

# 日志处理
capture_output = True
loglevel = 'info'
errorlog = 'logs/gunicorn_error.log'
```

### 在Centos运行时遇到的坑

> 问题：gunicorn 将环境加载到虚拟环境之外
>
> 解决方案：
>
> 1.  首先退出虚拟环境： `deactivate `
> 2.  再次进入虚拟环境： `source .venv/bin/activate`
> 3. `gunicorn -c swiper/gunicorn.conf.py swiper.wsgi`，可以了
>
> ```shell
> kill `logs/gunicorn.pid` # 杀死进程，进程已经保存在了 logs/gunicorn.pid 文件
> ```

```shell
(.venv) [root@VM-20-5-centos swiper]# curl http://127.0.0.1:9000/api/user/profile
{
    "code": 1001,
    "data": null
}
(.venv) [root@VM-20-5-centos swiper]# ps aux|grep gunicorn
root     1005885  0.0  0.2 132432 22644 ?        S    01:39   0:00 /root/swiper_test/swiper/.venv/bin/python3.7 /root/swiper_test/swiper/.venv/bin/gunicorn -c swiper/gunicorn.conf.py swiper.wsgi
```

### 进行压力测试

```shell
(.venv) [root@VM-20-5-centos swiper]# ab -n 1000 -c 100 http://127.0.0.1:9000/api/user/profile
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            9000

Document Path:          /api/user/profile
Document Length:        25 bytes

Concurrency Level:      100
Time taken for tests:   1.194 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      278000 bytes
HTML transferred:       25000 bytes
Requests per second:    837.71 [#/sec] (mean)
Time per request:       119.374 [ms] (mean)
Time per request:       1.194 [ms] (mean, across all concurrent requests)
Transfer rate:          227.42 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.5      0       3
Processing:    40   92 123.2     65     997
Waiting:       40   91 123.1     63     996
Total:         40   93 123.5     65     999

Percentage of the requests served within a certain time (ms)
  50%     65
  66%     74
  75%     76
  80%     79
  90%    144
  95%    185
  98%    783
  99%    808
 100%    999 (longest request)
```

+ RPS 每秒的请求数比较（优了二三十倍）

|                                           | Django                                             | Gunicorn                                          |
| ----------------------------------------- | -------------------------------------------------- | ------------------------------------------------- |
| Concurrency Level                         | 100                                                | 100                                               |
| Time taken for tests                      | 27.438 seconds                                     | 1.194 seconds                                     |
| Complete requests                         | 1000                                               | 1000                                              |
| Total transferred                         | 292000 bytes                                       | 278000 bytes                                      |
| HTML transferred                          | 38000 bytes                                        | 25000 bytes                                       |
| **Requests per second 每秒的请求数，RPS** | **36.45 [#/sec] (mean)**                           | **837.71 [#/sec] (mean)**                         |
| Time per request                          | 2743.766 [ms] (mean)                               | 119.374 [ms] (mean)                               |
| Time per request                          | 27.438 [ms] (mean, across all concurrent requests) | 1.194 [ms] (mean, across all concurrent requests) |
| Transfer rate                             | 10.39 [Kbytes/sec] received                        | 227.42 [Kbytes/sec] received                      |

+ Connection Times 耗时比较（优了二三十倍）

| Connection Times (ms) | min      | mean     | [+/-sd]   | median   | max      |                            |
| --------------------- | -------- | -------- | --------- | -------- | -------- | -------------------------- |
| Connect               | 0        | 91       | 297.0     | 0        | 1060     | 网络连接环节占据时长       |
| Processing            | 5        | 464      | 2547.9    | 18       | 26377    | 网络处理环节占据时长       |
| Waiting               | 1        | 454      | 2548.8    | 8        | 26374    | 网络之间发生阻塞等待的时间 |
| Total                 | 6        | 555      | 2728.3    | 18       | 27436    | 总的时间                   |
| ↑Django **Gunicorn↓** | **最小** | **平均** | **误差**  | **中位** | **最大** |                            |
| **Connect**           | **0**    | **0**    | **0.5**   | **0**    | **3**    |                            |
| **Processing**        | **40**   | **92**   | **123.2** | **65**   | **997**  |                            |
| **Waiting**           | **40**   | **91**   | **123.1** | **63**   | **996**  |                            |
| **Total**             | **40**   | **93**   | **123.5** | **65**   | **999**  |                            |

### 单台服务器最⼤连接数 

> `ulimit -n` 查看

+ ⽂件描述符: 限制⽂件打开数量 (⼀切皆⽂件) 
+ 内核限制: `net.core.somaxconn`
+ 内存限制 
+ 修改⽂件描述符: `ulimit -n 65535`

## 十九. WSGI与Nginx配置

### Gunicorn 扮演的角色

|         | HTTP Server | WSGI | WebAPP |
| ------- | ----------- | ---- | ------ |
| Request | Gunicorn    | WSGI | Django |

```
HTTP Server => 负责 
| ^				1. 建立与客户端的连接，接收客服端的⽹络数据; 
| |				2. 发送客服端的⽹络数据，断开与客户端的连接。
v |
WSGI => 负责 在 HTTPServer 和 WebApp 之间进⾏数据转换
| ^			1. 将用户的 “请求报文” 转化成 HTTPRequest 对象 
| |			2. 将 WebApp 返回的 HTTPResponse 对象转换成 “响应报文”
v |
Web App => 负责 Web 应⽤的业务逻辑、数据存储等等

1. HTTP Server 从网络上接收到大段的二进制字符串，就和socket之间传输的数据一样，bytes 类型的文本，自己不进行处理；
2. HTTP Server把这些数据交给WSGI，WSGI将这些数据翻译成WebAPP可以使用的request对象；
3. 然后WSGI将这些数据交给WebAPP。
```

### 分清几个概念 

> + **WSGI**: 全称是 `WebServerGatewayInterface`, 它是 Python 官⽅定义的⼀种描述 HTTP 服务器 (如nginx)与 Web 应⽤程序 (如 Django、Flask) 通信的规范。全⽂定义在 `PEP333 `
> + **uwsgi**: 与 WSGI 类似, 是 uWSGI 服务器⾃定义的通信协议, ⽤于定义传输信息的类型(type of information)。每⼀个 uwsgi packet 前 `4byte` 为传输信息类型的描述, 与 WSGI 协议是两种东⻄, 该协议性能远好于早期的 `Fast-CGI` 协议。 和WSGI是两种完全不同的东西。
> + **uWSGI**: uWSGI 是⼀个全功能的 HTTP 服务器, 实现了WSGI协议、uwsgi 协议、http 协议 等。它要做的就是把 HTTP协议转化成语⾔⽀持的⽹络协议。⽐如把 HTTP 协议转化成 WSGI 协议, 让 Python 可以直接使⽤。**即支持WSGI协议，也支持uWSGI协议。**

### 服务器的登陆与维护

```
/opt 放自己的东西
/project 在根目录额外独立的创建一个项目文件夹
这两个选一个，把项目放在一个不常用的地方，防止误操作
```

1. SSH 登陆服务器: ssh root@xxx.xxx.xxx.xxx 

2. 密钥 
   1. 产⽣: ssh-keygen 
   2. 公钥: ~/.ssh/id_rsa.pub 
   3. 私钥: ~/.ssh/id_rsa 
   4. 免密登陆服务器 
      1. 复制公钥内容 
      2. 将公钥内容粘贴到服务器的 ~/.ssh/authorized_keys 

3. 代码上传 
   1. rsync —— remote sync 远程同步（windows安装麻烦，直接用Tremius的SFTP也行）

   2. [rsync 资料](https://www.cnblogs.com/f-ck-need-u/p/7220009.html)

   3. ```
      rsync -crvP --exclude={.git,.venv,__pycache__} ./ root@82.157.36.220:/opt/swiper/
      """
      -c check		检查本地和远程文件有哪些不同，如果不同的话才会上传，如果相同的话会跳过这些文件
      -r --recursive	递归到目录中去
      -v 				显示rsync过程中详细信息。可以使用"-vvvv"获取更详细信息。
      -P				显示文件传输的进度信息。(实际上"-P"="--partial --progress"，其中的"--progress"才是显示进度信息的)。
      --exclude		指定排除规则来排除不需要传输的文件。
      ./				当前文件夹
      root@xxx:		账号@ip:端口默认22
      /opt/swiper/	远程路径
      """
      ```

### Gunicorn 进程模型

+ master：主进程，负责管理子进程，不干活
+ worker：子进程，接受用户请求并处理
+ worker：子进程，接受用户请求并处理
+ worker：子进程，接受用户请求并处理
+ worker：子进程，接受用户请求并处理

> 查看进程里的cpu信息：`cat /proc/cpuinfo`
>
> 查看内存：
>
> + free -m	以Mb为单位
> + free -k 	以Kb为单位
> + free -g	 以Gb为单位
>
> 在 vim 下，/搜索的词，按Shift+上/下，可以跳到词的位置。

### Nginx

[Nginx下载稳定版 Stable version](http://nginx.org/en/download.html)

```
cd download		# 1.在根目录的download文件夹下载安装包，没有的话mkdir一下
wget http://nginx.org/download/nginx-1.22.0.tar.gz		# 2.下载压缩包
tar -xzf nginx-1.22.0.tar.gz		# 3.解压
cd nginx-1.22.0/		# 4.进入文件夹
./configure		# 5.通过configure自动完成配置，生成一个Makefile编译的指导文件
make		# 6.阅读Makefile，根据这个文件完成二进制源代码的编译，编译的文件在	/objs 目录下
make install		# 7.安装，会安装到 /usr/local/nginx 目录下
/usr/local/nginx/conf/nginx.conf		 8.配置文件
```

1.  在 Nginx 根目录下，通过执行以下命令验证配置文件问题：`./sbin/nginx -t`
2.  在 Nginx 根目录下，通过执行以下命令重启 Nginx：`./sbin/nginx -s reload`

```nginx
#user  nobody;
worker_processes  4;

error_log  logs/error.log;
error_log  logs/error.log  notice;
error_log  logs/error.log  info;
#pid        logs/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  logs/access.log  main;
    sendfile        on;
    tcp_nopush     on;
    keepalive_timeout  65;
    gzip  on;
    upstream app_server {
        server 127.0.0.1:9000 weight=10;
    }
    server {
        listen       80;
        server_name  localhost;
        access_log  logs/host.access.log  main;
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
        location / {
                proxy_pass http://app_server;  # 反向代理
                proxy_set_header Host $http_host;
        }
    }
}
```

### Nginx 服务器 SSL 证书安装部署

[Nginx 服务器 SSL 证书安装部署](https://cloud.tencent.com/document/product/400/35244)

## 二十. Nginx 与不间断重启

+ 反向代理 

+ 负载均衡 

  + 轮询: rr (默认) 
  + 权重: weight 
  + IP哈希: ip_hash 

  + 最⼩连接数: least_conn 

+ 其他负载均衡 
  + LVS 
  + HAProxy 
  + F5 

+ 可以不使⽤ Nginx, 直接⽤ gunicorn 吗？ 
  + Nginx 相对于 Gunicorn 来说更安全 
  + Nginx 可以⽤作负载均衡

## 二十一. 脚本开发

+ 系统部署脚本 

+ 代码发布脚本 

+ 程序启动脚本 

+ 程序停⽌脚本 

+ 程序重启脚本 

+ 不间断重启: `kill -HUP [进程 ID]`

```
/tmp	临时的文件夹，下载完以后安装包就没用了
```

