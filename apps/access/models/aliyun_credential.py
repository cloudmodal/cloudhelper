#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: aliyun_credential.py
@ide: PyCharm
@time: 2020/4/11 19:06
@desc:
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common import fields
from .base import BaseModel

__all__ = [
    'AliYunCredential'
]


class AliYunCredential(BaseModel):
    SOURCE = ''
    SOURCE_STANDARD = 'aliyun-standard'
    SOURCE_CHOICES = (
        (SOURCE_STANDARD, 'AliYun Standard'),
    )
    user = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, blank=True, null=True,
        verbose_name=_("User"), related_name="user_aliyun_credential"
    )
    access_key_id = fields.EncryptCharField(
        max_length=256, verbose_name="Access Key ID"
    )
    secret_access_key = fields.EncryptCharField(
        max_length=256, verbose_name="Secret Access Key"
    )

    def __str__(self):
        return '{0.user}({0.credentials_name})'.format(self)

    class Meta:
        db_table = 'access_aliyun_access_key'
        ordering = ['access_key_id']
        verbose_name = _("AliYun Credential")
