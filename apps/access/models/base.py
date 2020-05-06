#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: base.py
@ide: PyCharm
@time: 2020/4/24 14:52
@desc:
"""
import uuid
from django.db import models
from organization.mixins.models import OrgModelMixin
from django.utils.translation import ugettext_lazy as _

from .. utils import create_or_update_credential, delete_credential_relevance


class BaseModel(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    credentials_name = models.CharField(
        max_length=256, verbose_name=_('Credentials Name')
    )
    account_type = models.CharField(
        max_length=50, verbose_name="Account Type"
    )
    credential_type = models.CharField(
        max_length=128, verbose_name="Credentials Type"
    )
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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(
            force_insert=force_insert, force_update=force_update,
            using=using, update_fields=update_fields,
        )
        tasks = {
            self.__str__(): {
                "org_id": self.org_id,
                "credential": self.id,
                "credentials_name": self.credentials_name,
                "account_type": self.account_type,
                "credential_type": self.credential_type,
                "date_created": self.date_created,
                "date_updated": self.date_updated,
                "created_by": self.created_by
            }
        }
        create_or_update_credential(tasks)

    def delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)
        delete_credential_relevance(self.__str__())

    class Meta:
        abstract = True
