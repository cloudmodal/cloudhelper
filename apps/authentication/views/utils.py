#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: utils.py
@ide: PyCharm
@time: 2020/4/16 23:29
@desc:
"""
from django.shortcuts import reverse, redirect


def redirect_to_guard_view():
    continue_url = reverse('authentication:login-guard')
    return redirect(continue_url)
