#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: tag.py
@ide: PyCharm
@time: 2020/5/7 11:33
@desc:
"""
import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from organization.mixins.models import OrgModelMixin


class Tags(OrgModelMixin):
    SYSTEM_CATEGORY = "system"
    USER_CATEGORY = "user"
    CATEGORY_CHOICES = (
        ("system", _("System")),
        ("user", _("User"))
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    key = models.CharField(max_length=128, verbose_name=_("Key"))
    value = models.CharField(max_length=128, verbose_name=_("Value"))
    category = models.CharField(
        max_length=128, choices=CATEGORY_CHOICES,
        default=USER_CATEGORY, verbose_name=_("Category")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))
    comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name=_('Date created')
    )

    @classmethod
    def get_queryset_group_by_key(cls):
        names = cls.objects.values_list('key', flat=True)
        for key in names:
            yield key, cls.objects.filter(key=key)

    def __str__(self):
        return "{}:{}".format(self.key, self.value)

    class Meta:
        db_table = "assets_tags"
        unique_together = [('key', 'value', 'org_id')]
