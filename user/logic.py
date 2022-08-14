import logging
import random
import os
from urllib.parse import urljoin

from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from django.core.cache import cache
from swiper import config

from libs.qncloud import async_upload_to_qiniu

from worker import call_by_worker
from django.conf import settings

log = logging.getLogger('inf')


def gen_verify_code(length=6):
    return random.randrange(10 ** (length - 1), 10 ** length)


@call_by_worker
def send_verify_code(phonenum):
    """异步发送验证码"""
    vcode = gen_verify_code()
    key = 'VerifyCode-%s' % phonenum
    cache.set(key, vcode)
    sms_cfg = config.ALI_SMS_PARAMS.copy()
    sms_cfg['phone_numbers'] = phonenum
    sms_cfg['template_param'] = '{"code":"%s"}' % vcode
    response = Sample.main(sms_cfg)
    return response


def check_vcode(phonenum, vcode):
    """检查验证码是否正确"""
    key = 'VerifyCode-%s' % phonenum
    saved_vcode = cache.get(key)
    log.info(f'check code is {str(saved_vcode) == str(vcode)}')
    return str(saved_vcode) == str(vcode)


def save_upload_file(user, upload_file):
    """保存上传文件，并上传到七牛云"""
    # 获取文件并保存到本地
    ext_name = os.path.splitext(upload_file.name)[-1]
    filename = 'Avatar-%s%s' % (user.id, ext_name)
    filepath = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, filename)
    with open(filepath, 'wb') as newfile:
        for chunk in upload_file.chunks():
            newfile.write(chunk)
    # 异步将头像上传七牛
    async_upload_to_qiniu(filepath, filename)
    # 将URL保存入数据库
    url = urljoin(config.QN_BASE_URL, filename)
    user.avatar = url
    user.save()
    # 修改缓存
    key = 'Profile-%s' % user.id
    user_profile = user.profile.to_dict()
    cache.set(key, user_profile, settings.SESSION_COOKIE_AGE)
    log.info(f'{user.id} upload file {url} successful')


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
