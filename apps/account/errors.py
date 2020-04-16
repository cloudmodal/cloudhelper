#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: errors.py
@ide: PyCharm
@time: 2020/1/16 19:16
@desc:
"""
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ErrorDetail
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


def get_error_details(data, default_code=None):

    if isinstance(data, list):
        ret = [
            get_error_details(item, default_code) for item in data
        ]
        if isinstance(data, ReturnList):
            return ReturnList(ret, serializer=data.serializer)
        return ret
    elif isinstance(data, dict):
        ret = {
            key: get_error_details(value, default_code)
            for key, value in data.items()
        }
        if isinstance(data, ReturnDict):
            return ReturnDict(ret, serializer=data.serializer)
        return ret

    text = force_str(data)
    code = getattr(data, 'code', default_code)
    return ErrorDetail(text, code)


class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Incorrect authentication credentials.')
    default_code = 'authentication_failed'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = get_error_details(detail, code)


class MovedPermanently(APIException):
    status_code = status.HTTP_301_MOVED_PERMANENTLY
    default_detail = _('Incorrect authentication credentials.')
    default_code = 'authentication_failed'


class MFABindFailed(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _('Incorrect authentication credentials.')
    default_code = 'authentication_failed'


class NotAcceptable(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _('Could not satisfy the request Accept header.')
    default_code = 'not_acceptable'

    def __init__(self, detail=None, code=None, available_renderers=None):
        self.available_renderers = available_renderers
        super().__init__(detail, code)
