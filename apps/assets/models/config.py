#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: config.py
@ide: PyCharm
@time: 2020/4/25 21:42
@desc:
"""
import uuid
from django.db import models
from organization.mixins.models import OrgModelMixin
from django.utils.translation import ugettext_lazy as _


class AssetConfigs(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(
        max_length=128, unique=True, verbose_name=_('Name')
    )
    account = models.CharField(
        max_length=128, verbose_name=_('Cloud Account')
    )
    credentials = models.ForeignKey(
        'access.StatisticsCredential', related_name='assets_cofig',
        verbose_name=_("Credentials"), on_delete=models.NOT_PROVIDED
    )
    region = models.CharField(
        max_length=128, verbose_name=_('Region'),
        help_text='region：AWS：us-east-1 aliyun：cn-hangzhou'
    )
    default_admin_user = models.ForeignKey(
        'assets.AdminUser', on_delete=models.PROTECT, verbose_name=_('Admin user')
    )
    state = models.BooleanField(
        default=False, verbose_name=_('State')
    )  # 状态，Ture：开启，Flase:关闭
    comment = models.TextField(
        max_length=128, blank=True, verbose_name=_('Comment')
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
        return '{0.name}({0.account})'.format(self)

    class Meta:
        db_table = 'asset_config'
        verbose_name = _("Asset Config")
