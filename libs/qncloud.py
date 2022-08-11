from qiniu import Auth, put_file, etag, BucketManager
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
