"""code_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import user, userinfo, acid_test, admin, place, color

urlpatterns = [
    path('session/login', user.login),
    path('session/logout', user.logout),
    path('user/create', user.create_user),
    path('user/get-info', userinfo.get_user_info),
    path('user/set-info', userinfo.set_user_info),
    path('record/get-acid', acid_test.query_acid_record),
    path('record/add-acid', acid_test.add_acid_record),
    path('user/list', admin.list_user),
    path('user/modify-privilege', admin.modify_permission),
    path('user/change-password', user.change_password),
    path('place/add', place.add_place),
    path('place/list', place.list_place),
    path('place/stay', place.stay_place),
    path('user/get-color', color.get_color)
]
