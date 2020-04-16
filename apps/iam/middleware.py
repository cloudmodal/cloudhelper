#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: middleware.py
@ide: PyCharm
@time: 2020/3/2 21:00
@desc:
"""
import pytz
from django.conf import settings
from django.utils import timezone
from .utils import set_current_request


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.META.get('TZ')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        response = self.get_response(request)
        return response


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_request(request)
        response = self.get_response(request)
        is_request_api = request.path.startswith('/api')
        if not settings.SESSION_EXPIRE_AT_BROWSER_CLOSE and not is_request_api:
            age = request.session.get_expiry_age()
            request.session.set_expiry(age)
        return response
