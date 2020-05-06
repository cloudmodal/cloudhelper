#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: view_urls.py
@ide: PyCharm
@time: 2020/4/23 22:43
@desc:
"""
from django.urls import path, include

from .. import views

app_name = 'access'

urlpatterns = [
    path('', views.CredentialsListView.as_view(), name='credentials-list'),
    path('create', views.CredentialsCreateView.as_view(), name='credentials-create'),
    path('edit/amazon-role/<uuid:pk>', views.AmazonRoleUpdateView.as_view(), name='amazon-role-update'),
    path('edit/amazon-access/<uuid:pk>', views.AmazonAccessKeyUpdateView.as_view(), name='amazon-access-update'),
    path('view/<uuid:pk>', views.CredentialsDetailView.as_view(), name='credentials-detail'),
    path('create/amazon-access-key/', views.AmazonAccessKeyCreateView.as_view(), name='amazon-access-key-create'),
    path('create/amazon-iam-role/', views.AmazonRoleCreateView.as_view(), name='amazon-iam-role-create'),
]
