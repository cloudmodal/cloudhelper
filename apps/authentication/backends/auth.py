#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: auth.py
@ide: PyCharm
@time: 2020/1/1 18:39
@desc:
"""
from django.db.models import Q
from account.models import User
# from django.contrib.auth import get_user_model
# from account.utils import get_user_lookup_kwargs
from django.contrib.auth.backends import ModelBackend


__all__ = ['EmailAuthenticationBackend']


# class UsernameAuthenticationBackend(ModelBackend):
#
#     def authenticate(self, *args, **credentials):
#         User = get_user_model()
#         try:
#             lookup_kwargs = get_user_lookup_kwargs({
#                 "{username}__iexact": credentials["username"]
#             })
#             user = User.objects.get(**lookup_kwargs)
#         except (User.DoesNotExist, KeyError):
#             return None
#         else:
#             try:
#                 if user.check_password(credentials["password"]):
#                     return user
#             except KeyError:
#                 return None


class EmailAuthenticationBackend(ModelBackend):
    """邮箱登录"""
    def authenticate(self, *args, **credentials):
        try:
            user = User.objects.get(Q(email=credentials["username"]))
        except (User.DoesNotExist, KeyError):
            return None
        else:
            try:
                if user.check_password(credentials["password"]):
                    return user
            except KeyError:
                return None


class MobileAuthenticationBackend(ModelBackend):
    """手机登录"""
    def authenticate(self, *args, **credentials):
        try:
            user = User.objects.get(phone=credentials["username"])
        except (User.DoesNotExist, KeyError):
            return None
        else:
            try:
                if user.check_password(credentials["password"]):
                    return user
            except KeyError:
                return None
