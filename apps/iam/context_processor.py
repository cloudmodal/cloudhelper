#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: context_processor.py
@ide: PyCharm
@time: 2020/4/11 12:21
@desc:
"""
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings


def iam_processor(request):
    # Setting default pk
    context = {
        'CH_TITLE': 'CloudHelper',
        'DEFAULT_PK': '00000000-0000-0000-0000-000000000000',
        'SITE_URL': settings.SITE_URL,
        'LOGO_URL': static('assets/images/logo-icon.png'),
        'LOGO_TEXT_URL': static('assets/images/logo-text.png'),
        'VERSION': settings.VERSION,
    }
    return context
