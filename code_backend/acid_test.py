from datetime import datetime, timedelta

from django.views.decorators.http import require_POST, require_GET
from pytz import utc

from . import session
from .color import set_color
from .config import Config
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
    limit = int(request.GET['limit']) if 'limit' in request.GET else 3
    limit = min(limit, 10)
    offset = int(request.GET['offset']) if 'offset' in request.GET else 0
    result = models.NuclearicAcid.objects.filter(user=user).order_by("-time")[offset:offset + limit]
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
        return response_json(status='InvalidInput', message='Input key or value missing.')
    if 'status' not in text or not isinstance(text.get('status'), int):
        return response_json(status='InvalidInput', message='Input key or value missing.')
    id = text['id']
    try:
        des = models.UserInfo.objects.get(real_id=id)
    except models.UserInfo.DoesNotExist:
        return response_json(status='NotFoundError', message='User not found.')
    except models.UserInfo.MultipleObjectsReturned:
        return response_json(status='SQLError', message='Multiple Objects Returned.')
    place = text['place'] if 'place' in text else ''
    try:
        time = datetime.strptime(text['time'], '%Y-%m-%d %H:%M:%S') - timedelta(hours=8) \
            if 'time' in text else datetime.now()
    except:
        return response_json(status='TimeError', message='Cannot parse time.')
    status = int(text['status'])
    try:
        set_color(des.user, models.Color.Type.Red if status == Config.positive_status else models.Color.Type.Green,
                  time)
        if status == Config.positive_status:
            timepoint = time - timedelta(seconds=Config.traceback_time)
            places = models.Place.objects.filter(passing__user=des.user, passing__time__gte=timepoint)
            records = models.Passing.objects.filter(place__in=places, time__gte=timepoint)
            if records.exists():
                for it in records:
                    if it.user != des.user:
                        set_color(it.user, models.Color.Type.Yellow, time)
    except models.Color.MultipleObjectsReturned:
        return response_json(status='SQLError', message='Multiple Objects Returned.')
    models.NuclearicAcid.objects.create(user=des.user, place=place, time=utc.localize(time), status=status)
    return response_json(status='OK', message='')
