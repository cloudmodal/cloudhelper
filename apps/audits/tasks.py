#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: tasks.py
@ide: PyCharm
@time: 2020/3/2 10:55
@desc:
"""
from celery import shared_task
from .utils import write_login_log


@shared_task
def write_login_log_async(*args, **kwargs):
    write_login_log(*args, **kwargs)
