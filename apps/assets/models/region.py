#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: region.py
@ide: PyCharm
@time: 2021/2/27 11:18
@desc:
"""
import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from organization.mixins.models import OrgModelMixin

from common.utils import get_logger
logger = get_logger(__name__)


class Region(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children', verbose_name=_("Parent"),
        help_text=_("Tips: If you create a top-level zone, leave this field blank.")
    )
    name = models.CharField(verbose_name=_("Region name"), max_length=64)
    owner = models.CharField(
        verbose_name=_("Owner"), blank=True, null=True, max_length=32
    )
    telephone = models.CharField(
        verbose_name=_("Telephone"), blank=True, null=True, max_length=32
    )
    address = models.CharField(
        verbose_name=_("Address"), blank=True, null=True, max_length=128
    )
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name=_('Date created')
    )
    comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "assets_region"
        verbose_name = _("Region")
        verbose_name_plural = verbose_name

    @classmethod
    def get_region_all_children_key_pattern(cls, key, with_self=True):
        pattern = r'^{0}:'.format(key)
        if with_self:
            pattern += r'|^{0}$'.format(key)
        return pattern

    @classmethod
    def get_region_children_key_pattern(cls, key, with_self=True):
        pattern = r'^{0}:[0-9]+$'.format(key)
        if with_self:
            pattern += r'|^{0}$'.format(key)
        return pattern

    def get_children_key_pattern(self, with_self=False):
        return self.get_region_children_key_pattern(self.name, with_self=with_self)

    def get_all_children_pattern(self, with_self=False):
        return self.get_region_all_children_key_pattern(self.name, with_self=with_self)
