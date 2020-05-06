#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: statistics.py
@ide: PyCharm
@time: 2020/4/28 14:30
@desc:
"""
import uuid
from django.db import models
from organization.mixins.models import OrgModelMixin
from django.utils.translation import ugettext_lazy as _


__all__ = ['StatisticsCredential']


class StatisticsCredential(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(
        max_length=256, blank=True,
        null=True, verbose_name=_('Name')
    )
    credential = models.CharField(
        max_length=36, blank=True, default='',
        verbose_name=_("Credentials"), db_index=True
    )
    credentials_name = models.CharField(
        blank=True, null=True,
        max_length=256, verbose_name=_('Credentials Name')
    )
    account_type = models.CharField(
        blank=True, null=True,
        max_length=50, verbose_name="Account Type"
    )
    credential_type = models.CharField(
        blank=True, null=True,
        max_length=128, verbose_name="Credentials Type"
    )
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date created')
    )
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name=_("Date updated")
    )
    created_by = models.CharField(
        max_length=128, null=True, verbose_name=_('Created by')
    )

    def __str__(self):
        return '{0.credentials_name}({0.account_type})'.format(self)

    class Meta:
        db_table = 'access_statistics_credentials'
        verbose_name = _("Credential Statistics")
