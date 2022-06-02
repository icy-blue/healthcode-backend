import hashlib

from django.db import IntegrityError
from django.views.decorators.http import require_POST

from . import session
from .config import Config
from .orms import models
from .overall import *


def hash_password(password, salt):
    data = hashlib.sha256(password.encode('utf-8')).hexdigest()
    data = data + salt
    data = hashlib.sha256(data.encode('utf-8')).hexdigest()
    front = data[:32]
    tail = data[32:]
    data = hex(int(front, 16) ^ int(tail, 16))
    return data


def pre_do(request):
    text = get_dict_from_request(request)
    if isinstance(text, HttpResponse):
        return text
    if 'username' not in text or 'password' not in text:
        return response_json(status='InvalidInput', message='Input key or value missing.')
    password = text['password']
    if len(password) < 6:
        return response_json(status='ShortPassword', message='Password is too short.')
    return None


@require_POST
def create_user(request):
    do = pre_do(request)
    if isinstance(do, HttpResponse):
        return do
    text = get_dict_from_request(request)
    username = text.get('username')
    password = text.get('password')
    user = models.User.objects.filter(username=username)
    if user.exists():
        return response_json(status='UserExist', message='User exists.')
    salt = create_random_string(Config.salt_len)
    password = hash_password(password, salt)
    try:
        user = models.User.objects.create(username=username, password=password, salt=salt)
    except IntegrityError:
        return response_json(status='SQLError', message='SQL server error.')
    return response_json(status='OK', message='')


@require_POST
def login(request):
    do = pre_do(request)
    if isinstance(do, HttpResponse):
        return do
    text = get_dict_from_request(request)
    username = text.get('username')
    password = text.get('password')
    try:
        user = models.User.objects.get(username=username)
    except models.User.DoesNotExist:
        return response_json(status='UserNotExist', message="User doesn't exist.")
    salt = user.salt
    password = hash_password(salt=salt, password=password)
    if password != user.password:
        return response_json(status='PasswordMismatch', message='Username and password mismatch.')
    cookie = session.set_session(user.uid)
    rep = response_json(status='OK', message='', is_admin=user.admin, token=cookie)
    rep.set_cookie('token', cookie)
    return rep


@require_POST
def logout(request):
    user = session.get_user_by_request(request)
    if not isinstance(user, models.User):
        return response_json(status='UserNotFound', message=f'Not login status.')
    uid = user.uid
    cookie = session.get_token_by_request(request)
    if not isinstance(cookie, str):
        return cookie
    session.del_session(uid, cookie)
    rep = response_json(status='OK', message='')
    rep.delete_cookie('token')
    return rep
