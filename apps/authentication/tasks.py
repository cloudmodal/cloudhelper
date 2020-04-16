#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: tasks.py
@ide: PyCharm
@time: 2020/3/2 09:57
@desc:
"""
from celery import shared_task
from ops.celery.decorator import register_as_period_task
from django.contrib.sessions.models import Session
from django.utils import timezone


@register_as_period_task(interval=3600*24)
@shared_task
def clean_django_sessions():
    Session.objects.filter(expire_date__lt=timezone.now()).delete()
