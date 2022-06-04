from django.views.decorators.http import require_GET

from code_backend import session
from code_backend.orms import models
from .overall import *


def set_color(user, _color, time):
    try:
        color = models.Color.objects.get(user=user)
        color.color = _color
        color.save()
    except models.Color.DoesNotExist:
        models.Color.objects.create(user=user, color=_color, update_time=time)


@require_GET
def get_color(request):
    user = session.get_user_by_request(request)
    try:
        color = models.Color.objects.get(user=user)
    except models.Color.DoesNotExist:
        color = models.Color.objects.create(user=user, color=models.Color.Type.Undefined)
    return response_json(status='OK', message='', color=color.color)
