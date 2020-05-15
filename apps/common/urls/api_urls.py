#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: api_urls.py
@ide: PyCharm
@time: 2020/3/7 12:25
@desc:
"""
from django.urls import path

from .. import api

app_name = 'common'

urlpatterns = [
    path('resources/cache/',
         api.ResourcesIDCacheApi.as_view(), name='resources-cache'),
]
