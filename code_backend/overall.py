import json
from random import Random

from django.shortcuts import HttpResponse


def response_json(*args, **kwargs):
    return HttpResponse(json.dumps(kwargs), content_type='application/json')


def generate_json(*args, **kwargs):
    return json.dumps(kwargs)


def generate_dict(*args, **kwargs):
    return kwargs


def create_random_string(length):
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    random = Random()
    for i in range(length):
        # 每次从chars中随机取一位
        salt += chars[random.randint(0, len_chars)]
    return salt


def get_dict_from_request(request):
    if request.method == "POST":
        try:
            text = json.loads(request.body)
        except:
            return response_json(status='InvalidInput', message='Input invalid.')
        return text
    else:
        return request.GET
