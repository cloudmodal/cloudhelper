#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: api_urls.py
@ide: PyCharm
@time: 2020/2/12 15:52
@desc:
"""
from django.urls import path
from rest_framework_bulk.routes import BulkRouter

from .. import api

app_name = 'access'
router = BulkRouter()
router.register(r'credentials', api.CredentialViewSet, 'credentials')
router.register(r'amazon-access-key', api.AmazonCredentialsViewSet, 'amazon--access-key')
router.register(r'amazon-iam-role', api.AmazonCredentialsRoleViewSet, 'amazon--iam-role')

urlpatterns = [
    # path('credentials/', api.CredentialsAPIView.as_view(), name='credentials'),
    path('amazon-cross-accounts/', api.CrossAccountsListView.as_view(), name='amazon-cross-accounts'),
]
urlpatterns += router.urls
