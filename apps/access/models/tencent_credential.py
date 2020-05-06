#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: tencent_credential.py
@ide: PyCharm
@time: 2020/4/11 19:06
@desc:
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common import fields
from .base import BaseModel

__all__ = [
    'TenCentCloudCredential'
]


class TenCentCloudCredential(BaseModel):
    SOURCE = ''
    SOURCE_STANDARD = 'tencnt-standard'
    SOURCE_INTERNATIONAL = 'tencnt-international'
    SOURCE_CHOICES = (
        (SOURCE_STANDARD, '中国站'),
        (SOURCE_INTERNATIONAL, 'International'),
    )

    user = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, blank=True, null=True,
        verbose_name=_("User"), related_name="user_qq_credential"
    )
    secret_id = fields.EncryptCharField(
        max_length=256, verbose_name="Secret ID"
    )
    secret_key = fields.EncryptCharField(
        max_length=256, verbose_name="Secret Key"
    )

    def __str__(self):
        return '{0.user}({0.credentials_name})'.format(self)

    class Meta:
        db_table = 'access_tencent_access_key'
        ordering = ['secret_id']
        verbose_name = _("TenCent Credential")
