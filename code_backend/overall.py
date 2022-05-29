import json
from random import Random

from django.shortcuts import HttpResponse


def exit_json(*args, **kwargs):
    return HttpResponse(json.dumps(kwargs))


def generate_json(*args, **kwargs):
    return json.dumps(kwargs)


def create_random_string(length):
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    random = Random()
    for i in range(length):
        # 每次从chars中随机取一位
        salt += chars[random.randint(0, len_chars)]
    return salt