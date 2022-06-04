from datetime import datetime

from django.views.decorators.http import require_POST, require_GET

from . import session, admin
from .orms import models
from .overall import *


@require_GET
def list_place(request):
    out = admin.admin_query_template(request)
    if isinstance(out, HttpResponse):
        return out
    limit, offset = out
    result = models.Place.objects.all()[offset:offset + limit]
    data = []
    for it in result:
        data.append(it.name)
    return response_json(status="OK", message="", length=len(data), data=data)


@require_POST
def add_place(request):
    text = get_dict_from_request(request)
    user = session.get_user_by_request(request)
    if not isinstance(user, models.User):
        return user
    if not user.admin:
        return response_json(status='Forbidden', message='No privilege.')
    if 'name' not in text:
        return response_json(status='InvalidInput', message='Input key or value missing.')
    name = text['name']
    try:
        if not isinstance(name, str):
            return response_json(status='InvalidInput', message='Name is not a string.')
        models.Place.objects.create(name=name)
    except:
        return response_json(status='PlaceExist', message='Place exists.')
    return response_json(status='OK', message='')


@require_POST
def stay_place(request):
    text = get_dict_from_request(request)
    user = session.get_user_by_request(request)
    if not isinstance(user, models.User):
        return user
    if 'place' not in text:
        return response_json(status='InvalidInput', message='Input key or value missing.')
    time = datetime.strptime(text['time'], '%Y-%m-%d %H:%M:%S') if 'time' in text else datetime.now()
    placename = text['place']
    try:
        place = models.Place.objects.get(name=placename)
    except:
        return response_json(status='NotFoundError', message=f'Cannot find place {placename}.')
    try:
        models.Stay.objects.create(user=user, place=place, time=time)
    except:
        return response_json(status='SQLError', message='SQL server error.')
    return response_json(status='OK', message='')
