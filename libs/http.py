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
