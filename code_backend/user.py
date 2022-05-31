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


@require_POST
def create_user(request):
    try:
        text = json.loads(request.body)
    except:
        return exit_json(status='InvalidInput', message='Input invalid.')
    username = text['username']
    password = text['password']
    if username is None or password is None:
        return exit_json(status='InvalidInput', message='Input key or value missing.')
    if len(password) < 6:
        return exit_json(status='ShortPassword', message='Password is too short.')
    user = models.User.objects.filter(username=username)
    if user.exists():
        return exit_json(status='UserExist', message='User exists.')
    salt = create_random_string(Config.salt_len)
    password = hash_password(password, salt)
    try:
        user = models.User.objects.create(username=username, password=password, salt=salt)
    except IntegrityError:
        return exit_json(status='SQLError', message='SQL server error.')
    return exit_json(status='OK', message='')


@require_POST
def login(request):
    try:
        print(request.body)
        text = json.loads(request.body)
    except:
        return exit_json(status='InvalidInput', message='Input invalid.')
    username = text['username']
    password = text['password']
    if username is None or password is None:
        return exit_json(status='InvalidInput', message='Input key or value missing.')
    if len(password) < 6:
        return exit_json(status='ShortPassword', message='Password is too short.')
    try:
        user = models.User.objects.get(username=username)
    except models.User.DoesNotExist:
        return exit_json(status='UserNotExist', message="User doesn't exist.")
    salt = user.salt
    password = hash_password(salt=salt, password=password)
    if password != user.password:
        return exit_json(status='PasswordMismatch', message='Username and password mismatch.')
    cookie = session.set_session(user.uid)
    return exit_json(status='OK', message='', token=cookie)


@require_POST
def logout(request):
    try:
        text = json.load(request.body)
    except:
        return exit_json(status='InvalidInput', message='Input invalid.')
    username = text['username']
    cookie = text['token']
    user = models.User.objects.filter(username=username)
    if not user.exists():
        return exit_json(status='UserNotFound', message=f'Cannot find user{username}.')
    uid = user[0].uid
    session.del_session(uid, cookie)
    return exit_json(status='OK', message='')
