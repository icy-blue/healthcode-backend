from datetime import datetime, timedelta

from .config import Config
from .orms import models
from .overall import *


def query_session(cookie):
    assert cookie is not None and len(cookie) != 0, 'Assert error'
    result = models.Cookie.objects.filter(cookie=cookie)
    print(result, type(result))
    if not result.exists():
        return None
    if result[0].TTL - datetime.now() < 0:
        return None
    return result[0].user.uid


def set_session(uid):
    try:
        user = models.User.objects.get(uid=uid)
    except:
        return None
    result = models.Cookie.objects.filter(user=user).order_by("TTL")
    if result.count() > Config.max_session:
        result[0].delete()
        result[0].save()
    cookie = create_random_string(Config.session_length)
    while models.Cookie.objects.filter(cookie=cookie).count() != 0:
        cookie = create_random_string(Config.session_length)
    try:
        models.Cookie.objects.create(user=user, cookie=cookie, TTL=datetime.now() + timedelta(seconds=Config.TTL))
    except:
        return None
    return cookie


def del_session(uid, cookie):
    assert cookie is not None and len(cookie) != 0, 'Assert error'
    try:
        user = models.User.objects.get(uid=uid)
        result = models.Cookie.objects.filter(cookie=cookie, user=user)
        if result.exists():
            result[0].delete()
            result[0].save()
    except:
        return False
    return True
