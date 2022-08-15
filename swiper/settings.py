"""
Django settings for swiper project.

Generated by 'django-admin startproject' using Django 1.11.15.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*!3y9m(n58bjtadt&$cu!-6e7gx$k9x0*v)@!$t#1au5i#1ly1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions.backends.cached_db',
    'django.contrib.staticfiles',
    'user',
    'social',
    'vip',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 安全中间件
    # 'common.middleware.CorsMiddleware' # 有问题
    'django.contrib.sessions.middleware.SessionMiddleware',  # session中间件
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # 目前可有可无
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.AuthMiddleware',  # 认证中间件，放到后面
]

ROOT_URLCONF = 'swiper.urls'

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

WSGI_APPLICATION = 'swiper.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

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

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = 'medias'

# 使用 redis 做缓存
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://82.157.36.220:6379/4',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PICKLE_VERSION': -1,
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://82.157.36.220:6379/2",  # 将session设置在1号库中
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",
        }
    }
}
# session的存储配置
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'session'  # 上面 CACHES 中设置的名称
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 设置session失效时间为30天后, 单位为秒S

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
