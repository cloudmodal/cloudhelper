#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: signals.py
@ide: PyCharm
@time: 2019/12/19 18:51
@desc:
"""
from django.dispatch import Signal


post_user_create = Signal(providing_args=('user',))
post_user_registered = Signal(providing_args=('user',))
