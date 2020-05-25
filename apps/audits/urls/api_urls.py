#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: api_urls.py
@ide: PyCharm
@time: 2020/5/25 13:05
@desc:
"""
from django.urls.conf import re_path
from rest_framework.routers import DefaultRouter

# from common import api as capi
# from .. import api


app_name = "audits"

router = DefaultRouter()
# router.register(r'ftp-logs', api.FTPLogViewSet, 'ftp-log')

urlpatterns = [
]

old_version_urlpatterns = [
    # re_path('(?P<resource>ftp-log)/.*', capi.redirect_plural_name_api)
]

urlpatterns += router.urls
