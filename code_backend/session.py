from sql import models
from overall import *
from datetime import datetime, timedelta
from config import Config


def query_session(cookie):
    assert cookie is not None and len(cookie) != 0, 'Assert error'
    result = models.Cookie.objects.filter(cookie=cookie)[0]
    if not result.exists():
        return None
    if result.TTL - datetime.now() < 0:
        return None
    return result.uid


def set_session(uid):
    result = models.Cookie.objects.filter(uid=uid).order_by("TTL")
    if result.count() > Config.max_session:
        result[0].delete()
    cookie = create_random_string(Config.session_length)
    while models.Cookie.objects.filter(cookie=cookie).count() != 0:
        cookie = create_random_string(Config.session_length)
    try:
        models.Cookie.objects.create(uid=uid, cookie=cookie, TTL=datetime.now() + timedelta(seconds=Config.TTL))
    except:
        return None
    return cookie
