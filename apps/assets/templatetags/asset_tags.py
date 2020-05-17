#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: asset_tags.py
@ide: PyCharm
@time: 2020/5/16 23:46
@desc:
"""
from collections import defaultdict

from django import template
register = template.Library()


@register.filter
def group_labels(queryset):
    grouped = defaultdict(list)
    for tag in queryset:
        grouped[tag.key].append(tag)
    return [(key, tags) for key, tags in grouped.items()]
