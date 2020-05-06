#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: google_credential.py
@ide: PyCharm
@time: 2020/4/11 19:05
@desc:
"""
from django.db import models
from django.contrib.postgres.fields import JSONField
from rest_framework.utils.encoders import JSONEncoder
from django.utils.translation import ugettext_lazy as _

from .base import BaseModel

__all__ = ['GoogleCredential']


class GoogleCredential(BaseModel):
    SOURCE = ''
    GOOGLE_STANDARD = 'google-standard'
    SOURCE_CHOICES = (
        (GOOGLE_STANDARD, 'Google Standard (Commercial)'),
    )

    user = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, blank=True, null=True,
        verbose_name=_("User"), related_name="user_google_credential"
    )
    google_service_account_key_json = JSONField(
        db_index=True, encoder=JSONEncoder,
        verbose_name=_("Google Service Account Key JSON")
    )

    def __str__(self):
        return '{0.user}({0.credentials_name})'.format(self)

    class Meta:
        db_table = 'access_google_account_key'
        ordering = ['credentials_name']
        verbose_name = _("Google Credential")
