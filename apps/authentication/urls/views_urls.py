#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: views_urls.py
@ide: PyCharm
@time: 2020/4/16 23:28
@desc:
"""
from django.urls import path, include

from .. import views

app_name = 'authentication'

urlpatterns = [
    # openid
    path('openid/', include(('authentication.backends.openid.urls', 'authentication'), namespace='openid')),

    # login
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('login/otp/', views.UserLoginOtpView.as_view(), name='login-otp'),
    path('login/wait-confirm/', views.UserLoginWaitConfirmView.as_view(), name='login-wait-confirm'),
    path('login/guard/', views.UserLoginGuardView.as_view(), name='login-guard'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]
