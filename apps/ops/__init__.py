#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: __init__.py
@ide: PyCharm
@time: 2020/2/21 22:09
@desc:
"""
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
