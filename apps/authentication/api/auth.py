#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: auth.py
@ide: PyCharm
@time: 2019/12/20 12:11
@desc:
"""
import uuid

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdminOrAppUser
from organization.mixins.api import RootOrgViewMixin
from account.models import User


logger = get_logger(__name__)
__all__ = [
    'UserConnectionTokenApi',
]


class UserConnectionTokenApi(RootOrgViewMixin, APIView):
    permission_classes = (IsOrgAdminOrAppUser,)
    http_method_names = ['get']

    def post(self, request):
        user_id = self.request.data.get('user', '')
        asset_id = self.request.data.get('asset', '')
        system_user_id = self.request.data.get('system_user', '')
        token = str(uuid.uuid4())
        user = get_object_or_404(User, id=user_id)
        # asset = get_object_or_404(Asset, id=asset_id)
        # system_user = get_object_or_404(SystemUser, id=system_user_id)
        value = {
            'user': user_id,
            'username': user.username,
            'asset': asset_id,
            # 'hostname': asset.hostname,
            'system_user': system_user_id,
            # 'system_user_name': system_user.name
        }
        cache.set(token, value, timeout=20)
        return Response({"token": token}, status=201)

    def get(self, request):
        token = self.request.data.get('token', None)
        headers = self.request.headers.get('Authorization', None)
        if token is None and headers:
            token = headers[7:]
        # user_only = self.request.query_params.get('user-only', None)
        value = cache.get(token, None)
        if value:
            user = get_object_or_none(User, id=value)
            data = {
                'role': user.role_display
            }
            return Response({"code": 200, "data": data, "msg": "OK"}, status=200)

        return Response({'code': 404, 'msg': 'User does not exist or credentials are wrong'}, status=404)

    def get_permissions(self):
        # if self.request.query_params.get('user-only', None):
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        return super().get_permissions()
