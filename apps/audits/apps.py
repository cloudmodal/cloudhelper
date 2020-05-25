#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: apps.py
@ide: PyCharm
@time: 2020/3/2 10:49
@desc:
"""
from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_save


class AuditsConfig(AppConfig):
    name = 'audits'

    def ready(self):
        from . import signals_handler
        if settings.SYSLOG_ENABLE:
            post_save.connect(signals_handler.on_audits_log_create)
