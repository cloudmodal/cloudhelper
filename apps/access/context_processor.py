#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: context_processor.py
@ide: PyCharm
@time: 2020/4/29 18:31
@desc:
"""
from .utils import cross_accounts


def access_processor(request):
    context = {
        'CROSS_ACCOUNTS': cross_accounts(request.user.email)
    }
    return context
