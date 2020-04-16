#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: utils.py
@ide: PyCharm
@time: 2019/12/19 16:35
@desc:
"""
from django.conf import settings
from .models import Client

__all__ = ['new_client']


def new_client():
    """
    :return: authentication.models.Client
    """
    return Client(
        server_url=settings.AUTH_OPENID_SERVER_URL,
        realm_name=settings.AUTH_OPENID_REALM_NAME,
        client_id=settings.AUTH_OPENID_CLIENT_ID,
        client_secret=settings.AUTH_OPENID_CLIENT_SECRET
    )
