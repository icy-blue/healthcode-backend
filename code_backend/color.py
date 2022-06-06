from datetime import datetime

from django.views.decorators.http import require_GET
from pytz import utc

from code_backend import session
from code_backend.orms import models
from .overall import *


def set_color(user, _color, time):
    time = utc.localize(time)
    try:
        color = models.Color.objects.get(user=user)
        if color.update_time < time:
            color.color = _color
            color.time = time
            color.save()
    except models.Color.DoesNotExist:
        models.Color.objects.create(user=user, color=_color, update_time=time)


@require_GET
def get_color(request):
    text = get_dict_from_request(request)
    user = session.get_user_by_request(request)
    if not isinstance(user, models.User):
        return user
    if 'id' in text or 'username' in text:
        if not user.admin:
            return response_json(status='Forbidden', message='Request is not allowed.')
        try:
            if 'id' in text:
                user = models.UserInfo.objects.filter(id=text['id'])
            else:
                user = models.UserInfo.objects.filter(user__username=text['username'])
        except models.UserInfo.DoesNotExist:
            return response_json(status='NotFoundError', message='User not found.')
        except models.UserInfo.MultipleObjectsReturned:
            return response_json(status='SQLError', message='Multiple Objects Returned.')
    try:
        color = models.Color.objects.get(user=user)
    except models.Color.DoesNotExist:
        time = datetime.strptime("1970-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        color = models.Color.objects.create(user=user, color=models.Color.Type.Undefined, update_time=time)
    return response_json(status='OK', message='', color=color.color)
