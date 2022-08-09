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

```
models.py
```

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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
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

> /user/admin.py 也可以删掉

#### 表迁移

```
manage.py makemigrations
manage.py migrate
```

#### __ dict __（类字典）

> 包含了这个对象中的所有属性和属性值：{key:value,key:value,key:value}

#### hasattr(obj,attr)

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

+ 可以将 **views.py** 改为 **api.py**，更直观，这些文件可以随便命名。

+ 新增一个写逻辑代码的文件 **logic.py**。

+ 新建一个**config.py**文件，来放与Django本身无关的配置，不影响Django。

#### 短信验证码

阿里云短信验证码：

```python
config.py
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
import random

from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

from swiper.config import ALI_SMS_PARAMS


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
    ) -> None:
        client = Sample.create_client(args.get('AccessKeyId'), args.get('AccessKeySecret'))
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name=args.get('sign_name'),
            template_code=args.get('template_code'),
            phone_numbers=args.get('phone_numbers'),
            template_param=args.get('template_param')
        )
        runtime = util_models.RuntimeOptions()
        # 复制代码运行请自行打印 API 的返回值
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.send_sms_with_options(send_sms_request, runtime)
            return response.body
        except Exception as error:
            # 如有需要，请打印 error
            raise str(error)


def gen_verify_code(length=6):
    return random.randrange(10 ** (length - 1), 10 ** length)


def send_verify_code(phone_numbers, code):
    sms_cfg = ALI_SMS_PARAMS.copy()
    sms_cfg['phone_numbers'] = phone_numbers
    sms_cfg['template_param'] = '{"code":"%s"}' % code
    Sample.main(sms_cfg)


if __name__ == '__main__':
    sms_params = ALI_SMS_PARAMS.copy()
    sms_params['phone_numbers'] = '17835699470'
    sms_params['template_param'] = '{"code":"%s"}' % gen_verify_code()
    print(Sample.main(sms_params))
```

