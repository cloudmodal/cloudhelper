#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: local.py
@ide: PyCharm
@time: 2019/12/19 15:55
@desc:
"""
from werkzeug.local import Local

thread_local = Local()


def _find(attr):
    return getattr(thread_local, attr, None)
