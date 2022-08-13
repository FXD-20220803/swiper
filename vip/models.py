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
