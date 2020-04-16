#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: api_urls.py
@ide: PyCharm
@time: 2019/12/20 12:10
@desc:
"""
from django.urls import path
from rest_framework_bulk.routes import BulkRouter
from .. import api

app_name = 'authentication'
router = BulkRouter()
router.register(r'access-keys', api.AccessKeyViewSet, 'access-key')


urlpatterns = [
    path('access-keys/<uuid:pk>/user/', api.AccessKeyListView.as_view(), name='access-key-list'),
    path('sms/', api.SMSCreateApi.as_view(), name='sms'),
    path('tokens/', api.TokenCreateApi.as_view(), name='auth-token'),
    path('mfa/challenge/', api.MFAChallengeApi.as_view(), name='mfa-challenge'),
    path('connection-token/', api.UserConnectionTokenApi.as_view(), name='connection-token'),
    path('otp/verify/', api.UserOtpVerifyApi.as_view(), name='user-otp-verify'),
    path('login-confirm-ticket/status/', api.TicketStatusApi.as_view(), name='login-confirm-ticket-status'),
    path('login-confirm-settings/<uuid:user_id>/', api.LoginConfirmSettingUpdateApi.as_view(),
         name='login-confirm-setting-update'),
]

urlpatterns += router.urls
