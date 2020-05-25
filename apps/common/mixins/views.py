#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: views.py
@ide: PyCharm
@time: 2020/5/25 13:23
@desc:
"""
from django.utils import timezone


__all__ = ["DatetimeSearchMixin"]


class DatetimeSearchMixin:
    date_format = '%Y-%m-%d'
    date_from = date_to = None

    def __init__(self):
        self.request = None

    def get_date_range(self):
        date_from_s = self.request.GET.get('date_from')
        date_to_s = self.request.GET.get('date_to')

        if date_from_s:
            date_from = timezone.datetime.strptime(date_from_s, self.date_format)
            tz = timezone.get_current_timezone()
            self.date_from = tz.localize(date_from)
        else:
            self.date_from = timezone.now() - timezone.timedelta(7)

        if date_to_s:
            date_to = timezone.datetime.strptime(
                date_to_s + ' 23:59:59', self.date_format + ' %H:%M:%S'
            )
            self.date_to = date_to.replace(
                tzinfo=timezone.get_current_timezone()
            )
        else:
            self.date_to = timezone.now()

    def get(self, request, *args, **kwargs):
        self.get_date_range()
        return super().get(request, *args, **kwargs)
