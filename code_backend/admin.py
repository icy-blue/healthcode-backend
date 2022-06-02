from django.views.decorators.http import require_POST, require_GET

from . import session
from .orms import models
from .overall import *


@require_GET
def list_user(request):
    user = session.get_user_by_request(request)
    if not isinstance(user, models.User):
        return user
    if not user.admin:
        return response_json(status='Forbidden', message='Request is not allowed.')
    limit = request.GET.get('limit') if 'limit' in request.GET else 50
    limit = max(limit, 50)
    offset = request.GET.get('offset') if 'offset' in request.GET else 0
    result = models.User.objects.all()[offset:offset + limit]
    data = []
    for id, i in enumerate(result):
        try:
            info = models.UserInfo.objects.get(user=i)
        except models.UserInfo.DoesNotExist:
            info = models.UserInfo.objects.create(user=i)
        except models.UserInfo.MultipleObjectsReturned:
            return response_json(status='SQLError', message='Multiple Objects Returned.')
        data.append(generate_dict(username=i.username, is_admin=i.admin, id=info.real_id, tel=info.tel,
                                  gender=info.gender, real_name=info.real_name))
    return response_json(status="OK", message="", length=len(data), data=data)


@require_POST
def modify_permission(request):
    text = get_dict_from_request(request)
    user = session.get_user_by_request(request)
    if not isinstance(user, models.User):
        return user
    if not user.admin:
        return response_json(status='Forbidden', message='Request is not allowed.')
    username = text['username'] if 'username' in text else None
    if username is None or len(username) == 0:
        return response_json(status='UsernameNotFound', message='Cannot find username')
    user = models.User.objects.filter(username=username)
    if not user.exists():
        return response_json(status="UserNotFound", message=f'Cannot find user {username}.')
    is_admin = text['is_admin'] if 'is_admin' in text else True
    try:
        user[0].admin = is_admin
        user[0].save()
    except:
        return response_json(status="SQLError", message="SQL server error.")
    return response_json(status="OK", message=f"User {username} ")
