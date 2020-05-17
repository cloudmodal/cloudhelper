#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: api_urls.py
@ide: PyCharm
@time: 2020/5/9 17:05
@desc:
"""
from django.urls import path, re_path
# from rest_framework_nested import routers
# from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter

from common import api as capi

from .. import api

app_name = 'assets'

router = BulkRouter()
router.register(r'tags', api.TagsViewSet, 'tags')
router.register(r'assets', api.AssetViewSet, 'asset')
router.register(r'asset-users', api.AssetUserViewSet, 'asset-user')
router.register(r'admin-users', api.AdminUserViewSet, 'admin-user')
router.register(r'system-users', api.SystemUserViewSet, 'system-user')
router.register(r'asset-config', api.AssetConfigViewSet, 'asset-config')


urlpatterns = [
    path('<uuid:pk>/synchronize/', api.AssetSynchronizeApi.as_view(), name='asset-synchronize'),

    path('asset-users/test-connective/',
         api.AssetUserTestConnectiveApi.as_view(), name='asset-user-connective'),
]

urlpatterns += router.urls
