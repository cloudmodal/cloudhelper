#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: urls.py
@ide: PyCharm
@time: 2019/12/19 16:35
@desc:
"""
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.OpenIDLoginView.as_view(), name='openid-login'),
    path('login/complete/', views.OpenIDLoginCompleteView.as_view(),
         name='openid-login-complete'),
]
