from django.db import IntegrityError
from django.views.decorators.http import require_POST

from . import session
from .orms import models
from .overall import *


def pre_do(request):
    try:
        text = json.loads(request.body)
    except:
        return exit_json(status='InvalidInput', message='Input invalid.')
    token = None
    if 'token' in text:
        token = text['token']
    if token is None or len(token) == 0:
        return exit_json(status='RequireToken', message='Cannot find token.')
    uid = session.query_session(token)
    if uid is None:
        return exit_json(status='TokenInvalid', message='User token is outdated or not existed.')
    try:
        user = models.User.objects.get(uid=uid)
    except IntegrityError:
        return exit_json(status='SQLError', message='SQL server error.')
    username = None
    if 'username' in text:
        username = text['username']
    if username is not None and len(username) != 0 and username != user.username and not user.admin:
        return exit_json(status='InvalidRequest', message='Cannot get others\' information.')
    try:
        info = models.UserInfo.objects.get(user=user)
    except models.UserInfo.DoesNotExist:
        info = models.UserInfo.objects.create(user=user)
    except models.UserInfo.MultipleObjectsReturned:
        return exit_json(status='SQLError', message='Multiple Objects Returned.')
    return info, text


@require_POST
def get_user_info(request):
    return_data = pre_do(request)
    if isinstance(return_data, HttpResponse):
        return return_data
    info, _ = return_data
    data = {'id': info.real_id, 'tel': info.tel, 'gender': info.gender, 'real_name': info.real_name}
    if info.age != -1:
        data['age'] = info.age
    return exit_json(status='OK', message='', data=data)


@require_POST
def set_user_info(request):
    return_data = pre_do(request)
    if isinstance(return_data, HttpResponse):
        return return_data
    info, text = return_data
    cnt = 0
    try:
        if 'id' in text:
            info.real_id = text['id']
            cnt += 1
        if 'age' in text:
            info.age = text['age']
            cnt += 1
        if 'tel' in text:
            info.tel = text['tel']
            cnt += 1
        if 'real_name' in text:
            info.real_name = text['real_name']
            cnt += 1
        info.save()
    except:
        return exit_json(status='SQLError', message='Update error')
    return exit_json(status='OK', message=f'{cnt} data updated.')
