import hashlib

from django.db import IntegrityError

from . import session
from .config import Config
from .orms import models
from .overall import *


def hash_password(password, salt):
    data = hashlib.sha256(password).hexdigest()
    data = data + salt
    data = hashlib.sha256(data).hexdigest()
    return data


def create_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username is None or password is None:
        return exit_json(status='InvalidInput', message='Input invalid.')
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


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username is None or password is None:
        return exit_json(status='InvalidInput', message='Input invalid.')
    if len(password) < 6:
        return exit_json(status='ShortPassword', message='Password is too short.')
    user = models.User.objects.get(username=username)
    if not user.exists():
        return exit_json(status='UserExist', message='User not exists.')
    salt = user.salt
    password = hash_password(salt=salt, password=password)
    if password != user[0].password:
        return exit_json(status='PasswordMismatch', message='Username and password mismatch.')
    cookie = session.set_session(user.uid)
    jsons = generate_json(status='OK', message='')
    rep = HttpResponse(jsons)
    return rep.set_cookie('token', cookie)


def logout(request):
    username = request.POST.get('username')
    cookie = request.COOKIES.get('token')
    user = models.User.objects.filter(username=username)
    if not user.exists():
        return exit_json(status='UserNotFound', message=f'Cannot find user{username}.')
    uid = user[0].uid
    session.del_session(uid, cookie)
    return exit_json(status='OK', message='')
