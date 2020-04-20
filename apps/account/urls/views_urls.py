#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: views_urls.py
@ide: PyCharm
@time: 2020/4/17 16:10
@desc:
"""
from django.urls import path

from .. import views

app_name = 'account'

urlpatterns = [
    path('first-login/', views.UserFirstLoginView.as_view(), name='user-first-login'),

    path('user/', views.UserListView.as_view(), name='user-list'),
    path('user/create/', views.UserCreateView.as_view(), name='user-create'),
    path('user/<uuid:pk>/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('user/update/', views.UserBulkUpdateView.as_view(), name='user-bulk-update'),
    path('user/<uuid:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    # User group view
    path('user-group/', views.UserGroupListView.as_view(), name='user-group-list'),
    path('user-group/<uuid:pk>/', views.UserGroupDetailView.as_view(), name='user-group-detail'),
    path('user-group/create/', views.UserGroupCreateView.as_view(), name='user-group-create'),
    path('user-group/<uuid:pk>/update/', views.UserGroupUpdateView.as_view(), name='user-group-update'),
    path('user-group/<uuid:pk>/assets/', views.UserGroupGrantedAssetView.as_view(), name='user-group-granted-asset'),
]
