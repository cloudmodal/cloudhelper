#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: api_urls.py
@ide: PyCharm
@time: 2020/1/2 19:13
@desc:
"""
from django.urls import re_path
from rest_framework.routers import DefaultRouter

from common import api as capi
from .. import api


app_name = 'organization'
router = DefaultRouter()

# 将会删除
router.register(r'orgs/(?P<org_id>[0-9a-zA-Z\-]{36})/membership/admins',
                api.OrgMembershipAdminsViewSet, 'membership-admins')
router.register(r'orgs/(?P<org_id>[0-9a-zA-Z\-]{36})/membership/users',
                api.OrgMembershipUsersViewSet, 'membership-users'),

router.register('', api.OrgViewSet, 'organization')

old_version_urlpatterns = [
    re_path('(?P<resource>org)/.*', capi.redirect_plural_name_api)
]

urlpatterns = [
    # path('my-orgs/', api.GetJoinedOrganizations.as_view(), name='my-orgs')
]

urlpatterns += router.urls + old_version_urlpatterns
