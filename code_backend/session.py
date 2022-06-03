from datetime import datetime, timedelta

from pytz import UTC as utc

from .config import Config
from .orms import models
from .overall import *


def query_user_by_token(cookie):
    if isinstance(cookie, HttpResponse):
        return cookie
    if not isinstance(cookie, str):
        return response_json(status='TokenInvalid', message='Token is invalid.')
    result = models.Cookie.objects.filter(cookie=cookie)
    if not result.exists():
        return response_json(status='TokenInvalid', message='Token is not found.')
    if result[0].TTL < utc.localize(datetime.now()):
        return response_json(status='TokenInvalid', message='Token is outdated.')
    return result[0].user


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


def del_session(cookie):
    assert cookie is not None and len(cookie) != 0, 'Assert error'
    try:
        result = models.Cookie.objects.filter(cookie=cookie)
        if result.exists():
            result[0].delete()
            result[0].save()
    except:
        return False
    return True


def get_user_by_request(request):
    token = get_token_by_request(request)
    user = query_user_by_token(token)
    return user


def get_token_by_request(request):
    token = None
    if request.method == 'GET':
        if 'token' in request.GET:
            token = request.GET['token']
    else:
        try:
            text = json.loads(request.body)
        except:
            return response_json(status='InvalidInput', message='Input invalid.')
        if 'token' in text:
            token = text['token']
    if token is None and 'token' in request.COOKIES:
        token = request.COOKIES.get('token')
    if token is None or len(token) == 0:
        return response_json(status='RequireToken', message='Cannot find token.')
    return token
