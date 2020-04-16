#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: api_urls.py
@ide: PyCharm
@time: 2019/12/20 11:50
@desc:
"""
from django.urls import path
from rest_framework_bulk.routes import BulkRouter

from authentication import api as auth_api
from .. import api

app_name = 'account'

router = BulkRouter()
router.register(r'users', api.UserViewSet, 'user')
router.register(r'groups', api.UserGroupViewSet, 'user-group')
router.register(r'users-groups-relations', api.UserUserGroupRelationViewSet, 'user-group-relation')


urlpatterns = [
    path('connection-token/', auth_api.UserConnectionTokenApi.as_view(), name='connection-token'),
    path('profile/', api.UserProfileApi.as_view(), name='user-profile'),
    path('otp/disable/authentication/', api.UserDisableMFAAPI.as_view(), name='user-otp-disable-authentication'),
    path('security-check/', api.SecuritySettingsCheckApi.as_view(), name='security-settings-check'),
    path('otp/enable/authentication/', api.UserOtpEnableAuthenticationApi.as_view(), name='otp-enable-authentication'),
    path('otp/enable/bind/', api.UserOtpEnableBindApi.as_view(), name='otp-enable-bind'),
    path('otp/reset/', api.UserResetOTPApi.as_view(), name='my-otp-reset'),
    path('users/<uuid:pk>/otp/reset/', api.UserResetOTPApi.as_view(), name='user-reset-otp'),
    path('users/<uuid:pk>/password/', api.AdminChangeUserPasswordApi.as_view(), name='admin-change-user-password'),
    path('users/<uuid:pk>/pubkey/reset/', api.UserResetPKApi.as_view(), name='user-public-key-reset'),
    path('users/<uuid:pk>/pubkey/update/', api.UserUpdatePKApi.as_view(), name='user-public-key-update'),
    path('users/<uuid:pk>/unblock/', api.UserUnblockPKApi.as_view(), name='user-unblock'),
    path('users/<uuid:pk>/groups/', api.UserUpdateGroupApi.as_view(), name='user-update-group'),
    path('groups/<uuid:pk>/users/', api.UserGroupUpdateUserApi.as_view(), name='user-group-update-user'),

    # 重置密码
    path('users/password/reset/', api.UserResetPasswordApi.as_view(), name='user-reset-password'),
    # 发送验证码
    path('send/mobile_captcha/', api.RetrievePasswordSendSMSApi.as_view(), name='mobile-captcha'),
    path('send/email_captcha/', api.RetrievePasswordSendSESApi.as_view(), name='email-captcha'),
    path('verify/captcha/', api.VerifyCodeApi.as_view(), name='verify-captcha'),

    path('register/', api.RegisterAccountAPI.as_view(), name='register-account'),
    path('confirm_verification/<str:token>', api.ConfirmVerificationApi.as_view(), name='confirm-verification'),
]
urlpatterns += router.urls
