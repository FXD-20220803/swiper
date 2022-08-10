import json
from django.http import HttpResponse


def render_json(data, code):
    result = {
        'code': code,
        'data': data
    }
    json_str = json.dumps(result, separators=[',', ':'])
    return HttpResponse(json_str)
