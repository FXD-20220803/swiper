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
            print('get from cache')
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
    print('add to cache')
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
