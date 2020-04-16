#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: sms.py
@ide: PyCharm
@time: 2020/1/7 16:52
@desc:
"""
from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from common.utils import get_logger
from common.utils import create_captcha
from common.aliyunsm import SMSCaptcha

from .. import serializers, errors
from ..mixins import AuthMixin

logger = get_logger(__name__)

__all__ = ['SMSCreateApi']


class SMSCreateApi(AuthMixin, CreateAPIView):
    """获取短信动态码令牌"""
    permission_classes = (AllowAny,)
    serializer_class = serializers.SMSSerializer
    throttle_scope = 'send_sms'

    def create_session_if_need(self):
        if self.request.session.is_empty():
            self.request.session.create()

    def create(self, request, *args, **kwargs):
        self.create_session_if_need()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = self.check_user_auth_if_registered()
            # 发送阿里云短信模版
            sms = SMSCaptcha(template_code='SMS_181863597')
            # 写入缓存
            cache.set(user.phone, create_captcha(6), timeout=60 * 10)
            cache_captcha = cache.get(user.phone, None)
            logger.debug(f'手机{user.phone}的验证码: {cache_captcha}')
            # 发送验证码
            sms.send_sms(user.phone, cache_captcha)
            msg = "The verification code was sent successfully! The validity period is 10 minutes."
            return Response({'code': 201, "msg": msg}, status=status.HTTP_201_CREATED)
        except errors.AuthFailedError as e:
            return Response(e.as_data(), status=status.HTTP_400_BAD_REQUEST)
        except errors.NeedMoreInfoError as e:
            return Response(e.as_data(), status=status.HTTP_200_OK)
