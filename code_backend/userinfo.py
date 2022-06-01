from django.views.decorators.http import require_POST

from . import session
from .orms import models
from .overall import *


def pre_do(request):
    text = get_dict_from_request(request)
    if isinstance(text, HttpResponse):
        return text
    token = text['token'] if 'token' in text else None
    user = session.get_user_by_token(token)
    if not isinstance(user, models.User):
        return response_json(status='TokenInvalid', message='User token is outdated or not existed.')
    username = text['username'] if 'username' in text else None
    if username is not None and len(username) != 0 and username != user.username and not user.admin:
        return response_json(status='InvalidRequest', message='Cannot get others\' information.')
    try:
        info = models.UserInfo.objects.get(user=user)
    except models.UserInfo.DoesNotExist:
        info = models.UserInfo.objects.create(user=user)
    except models.UserInfo.MultipleObjectsReturned:
        return response_json(status='SQLError', message='Multiple Objects Returned.')
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
        return response_json(status='SQLError', message='Update error')
    return response_json(status='OK', message=f'{cnt} data updated.')
