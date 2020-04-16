#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: radius.py
@ide: PyCharm
@time: 2019/12/19 16:35
@desc:
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from radiusauth.backends import RADIUSBackend, RADIUSRealmBackend


User = get_user_model()


class CreateUserMixin:
    def get_django_user(self, username, password=None):
        if isinstance(username, bytes):
            username = username.decode()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            if '@' in username:
                email = username
            else:
                email_suffix = settings.EMAIL_SUFFIX
                email = '{}@{}'.format(username, email_suffix)
            user = User(username=username, name=username, email=email)
            user.source = user.SOURCE_RADIUS
            user.save()
        return user


class RadiusBackend(CreateUserMixin, RADIUSBackend):
    pass


class RadiusRealmBackend(CreateUserMixin, RADIUSRealmBackend):
    pass
