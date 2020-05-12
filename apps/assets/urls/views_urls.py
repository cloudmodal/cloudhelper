#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: views_urls.py
@ide: PyCharm
@time: 2020/5/7 17:08
@desc:
"""
from django.urls import path
from .. import views

app_name = 'assets'

urlpatterns = [
    path('', views.AssetListView.as_view(), name='asset-index'),
    path('asset/', views.AssetListView.as_view(), name='asset-list'),

    path('asset-config/', views.AssetConfigListView.as_view(), name='asset-config'),
    path('asset-config/create/', views.AssetConfigCreateView.as_view(), name='asset-config-create'),
    path('asset-config/<uuid:pk>/update/', views.AssetConfigUpdateView.as_view(), name='asset-config-update'),
    path('asset-config/<uuid:pk>/', views.AssetConfigDetailView.as_view(), name='asset-config-detail'),

    # Asset admin user url
    path('admin-user/', views.AdminUserListView.as_view(), name='admin-user-list'),
    path('admin-user/create/', views.AdminUserCreateView.as_view(), name='admin-user-create'),
    path('admin-user/<uuid:pk>/', views.AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin-user/<uuid:pk>/update/', views.AdminUserUpdateView.as_view(), name='admin-user-update'),
    path('admin-user/<uuid:pk>/delete/', views.AdminUserDeleteView.as_view(), name='admin-user-delete'),
    path('admin-user/<uuid:pk>/assets/', views.AdminUserAssetsView.as_view(), name='admin-user-assets'),

    # Asset system user url
    path('system-user/', views.SystemUserListView.as_view(), name='system-user-list'),
    path('system-user/create/', views.SystemUserCreateView.as_view(), name='system-user-create'),
    path('system-user/<uuid:pk>/', views.SystemUserDetailView.as_view(), name='system-user-detail'),
    path('system-user/<uuid:pk>/update/', views.SystemUserUpdateView.as_view(), name='system-user-update'),
    path('system-user/<uuid:pk>/delete/', views.SystemUserDeleteView.as_view(), name='system-user-delete'),
    path('system-user/<uuid:pk>/asset/', views.SystemUserAssetView.as_view(), name='system-user-asset'),

    path('tags/', views.TagsListView.as_view(), name='tags-list'),
    path('tags/create/', views.TagsCreateView.as_view(), name='tags-create'),
    path('tags/<uuid:pk>/update/', views.TagsUpdateView.as_view(), name='tags-update'),
    path('tags/<uuid:pk>/delete/', views.TagsDeleteView.as_view(), name='tags-delete'),
]
