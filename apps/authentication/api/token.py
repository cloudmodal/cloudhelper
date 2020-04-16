#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: token.py
@ide: PyCharm
@time: 2019/12/20 12:14
@desc:
"""
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from common.utils import get_logger

from .. import serializers, errors
from ..mixins import AuthMixin


logger = get_logger(__name__)

__all__ = ['TokenCreateApi']


class TokenCreateApi(AuthMixin, CreateAPIView):
    """获取Token令牌"""
    permission_classes = (AllowAny,)
    serializer_class = serializers.BearerTokenSerializer

    def create_session_if_need(self):
        if self.request.session.is_empty():
            self.request.session.create()

    def create(self, request, *args, **kwargs):
        self.create_session_if_need()
        # 如果认证没有过，检查账号密码
        try:
            user = self.check_user_auth_if_need()
            self.check_user_mfa_if_need(user)
            self.check_user_login_confirm_if_need(user)
            self.send_auth_signal(success=True, user=user)
            self.clear_auth_mark()
            resp = super().create(request, *args, **kwargs)
            return resp
        except errors.AuthFailedError as e:
            return Response(e.as_data(), status=status.HTTP_400_BAD_REQUEST)
        except errors.MFARequiredError as e:
            return Response(e.as_data(), status=status.HTTP_301_MOVED_PERMANENTLY)
        except errors.NeedMoreInfoError as e:
            return Response(e.as_data(), status=status.HTTP_200_OK)
