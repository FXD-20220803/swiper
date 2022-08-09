import random

from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

from swiper.config import ALI_SMS_PARAMS
from worker import call_by_worker


def gen_verify_code(length=6):
    return random.randrange(10 ** (length - 1), 10 ** length)


@call_by_worker
def send_verify_code(phone_numbers, code):
    sms_cfg = ALI_SMS_PARAMS.copy()
    sms_cfg['phone_numbers'] = phone_numbers
    sms_cfg['template_param'] = '{"code":"%s"}' % code
    Sample.main(sms_cfg)


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


if __name__ == '__main__':
    send_verify_code('17835699470', gen_verify_code())
