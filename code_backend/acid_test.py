from datetime import datetime

from django.views.decorators.http import require_POST, require_GET

from . import session
from .orms import models
from .overall import *


@require_GET
def query_acid_record(request):
    user = session.get_user_by_request(request)
    if not isinstance(user, models.User):
        return user
    username = request.GET['username'] if 'username' in request.GET and len(
        request.GET['username']) != 0 else user.username
    if username != user.username and not user.admin:
        return response_json(status='Forbidden', message='No privilege.')
    limit = request.GET['limit'] if 'limit' in request.GET else 3
    limit = max(limit, 100)
    offset = request.GET['offset'] if 'offset' in request.GET else 0
    result = models.NuclearicAcid.objects.filter(user=user).order_by("time")[offset:offset + limit]
    export = []
    for i in result:
        export.append(
            generate_dict(place=i.place, status=i.status, time=datetime.strftime(i.time, "%Y-%m-%d %H:%M:%S")))
    return response_json(status='OK', message='', length=len(export), data=export)


@require_POST
def add_acid_record(request):
    text = get_dict_from_request(request)
    user = session.get_user_by_request(request)
    if not isinstance(user, models.User):
        return user
    if not user.admin:
        return response_json(status='Forbidden', message='No privilege.')
    if 'id' not in text:
        return response_json(status='IDError', message='Cannot find id.')
    id = text['id']
    try:
        des = models.User.objects.get(id=id)
    except models.UserInfo.DoesNotExist:
        return response_json(status='NotFoundError', message='User not found.')
    except models.UserInfo.MultipleObjectsReturned:
        return response_json(status='SQLError', message='Multiple Objects Returned.')
    place = text['place'] if 'place' in text else ''
    time = datetime.strptime(text['time'], '%Y-%m-%d %H:%M:%S') if 'time' in text else datetime.now()
    if 'status' not in text or not isinstance(text.get('status'), int):
        return response_json(status='StatusError', message='Cannot read status.')
    status = int(text['status'])
    models.NuclearicAcid.objects.create(user=des, place=place, time=time, status=status)
    return response_json(status='OK', message='')
