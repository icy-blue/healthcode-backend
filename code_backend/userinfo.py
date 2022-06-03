from django.views.decorators.http import require_POST

from . import session
from .orms import models
from .overall import *


def get_random_id():
    return '###' + create_random_string(15)


def is_random_id(id):
    return id[:3] == '###'


def pre_do(request):
    text = get_dict_from_request(request)
    if isinstance(text, HttpResponse):
        return text
    user = session.get_user_by_request(request)
    if not isinstance(user, models.User):
        return user
    username = text['username'] if 'username' in text and len(text.get('username')) != 0 else user.username
    if username != user.username and not user.admin:
        return response_json(status='Forbidden', message='Cannot get others\' information.')
    try:
        info = models.UserInfo.objects.get(user=user)
    except models.UserInfo.DoesNotExist:
        info = models.UserInfo.objects.create(user=user, real_id=get_random_id())
    except models.UserInfo.MultipleObjectsReturned:
        return response_json(status='SQLError', message='Multiple Objects Returned.')
    return info, text


def get_user_info(request):
    return_data = pre_do(request)
    if isinstance(return_data, HttpResponse):
        return return_data
    info, _ = return_data
    data = {'tel': info.tel, 'gender': info.gender, 'real_name': info.real_name, 'age': info.age,
            'id': info.real_id if not is_random_id(info.real_id) else ''}
    return response_json(status='OK', message='', data=data)


@require_POST
def set_user_info(request):
    return_data = pre_do(request)
    if isinstance(return_data, HttpResponse):
        return return_data
    info, text = return_data
    cnt = 0
    try:
        if 'id' in text:
            info.real_id = text['id'] if text['id'] != '' else get_random_id()
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
        if 'gender' in text:
            info.gender = text['gender']
            cnt += 1
        info.save()
    except:
        return response_json(status='SQLError', message='SQL server error.')
    return response_json(status='OK', message=f'{cnt} data updated.')
