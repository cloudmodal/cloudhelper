#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: utils.py
@ide: PyCharm
@time: 2019/12/20 12:16
@desc:
"""
from django.core.cache import cache
from django.contrib.auth import authenticate
from common.utils import get_object_or_none
from account.models import User
from . import errors


def check_user_valid(**kwargs):
    password = kwargs.pop('password', None)
    code = kwargs.pop('code', None)
    public_key = kwargs.pop('public_key', None)
    mobile = kwargs.pop('mobile', None)
    email = kwargs.pop('email', None)
    username = kwargs.pop('username', None)
    request = kwargs.get('request')

    if username:
        user = get_object_or_none(User, username=username) or \
               get_object_or_none(User, email=username) or \
               get_object_or_none(User, phone=username)
    elif email:
        user = get_object_or_none(User, email=email)
    # 手机验证码登录
    elif mobile:
        user = get_object_or_none(User, phone=mobile)
    else:
        user = None

    if user is None:
        return None, errors.reason_user_not_exist
    elif user.is_expired:
        return None, errors.reason_user_inactive
    elif not user.is_active:
        return None, errors.reason_user_inactive
    elif user.password_has_expired:
        return None, errors.reason_password_expired

    if password or public_key:
        user = authenticate(
            request, username=username, email=username, phone=username, password=password, public_key=public_key
        )

        if user:
            return user, ''
    elif code:
        if code == cache.get(user.phone):
            return user, ''
        else:
            return None, errors.reason_code_failed

    elif mobile:
        return user, ''

    return None, errors.reason_password_failed
