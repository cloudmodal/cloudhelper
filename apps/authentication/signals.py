#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: signals.py
@ide: PyCharm
@time: 2019/12/20 12:16
@desc:
"""
from django.dispatch import Signal


post_auth_success = Signal(providing_args=('user', 'request'))
post_auth_failed = Signal(providing_args=('username', 'request', 'reason'))
