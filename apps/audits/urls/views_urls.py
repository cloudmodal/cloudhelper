#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: views_urls.py
@ide: PyCharm
@time: 2020/5/25 13:05
@desc:
"""
from django.urls import path
from .. import views


app_name = "audits"

urlpatterns = [
    path('login-log/', views.LoginLogListView.as_view(), name='login-log-list'),
    path('operate-log/', views.OperateLogListView.as_view(), name='operate-log-list'),
    path('password-log/', views.PasswordLogList.as_view(), name='password-log-list'),
    path('login-log/export/', views.LoginLogExportView.as_view(), name='login-log-export'),
]
