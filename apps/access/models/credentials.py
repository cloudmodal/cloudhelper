#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: credentials.py
@ide: PyCharm
@time: 2020/4/24 17:39
@desc:
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common import fields
from .base import BaseModel

__all__ = [
    'AccessKeys'
]


class AccessKeys(BaseModel):
    user = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, blank=True, null=True,
        verbose_name=_("User"), related_name="user_aws_credential"
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
        db_table = 'access_keys'
        ordering = ['access_key_id']
        verbose_name = _("Credential")


# class Credentials(OrgModelMixin):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True)
#     credentials_name = models.CharField(
#         max_length=50, verbose_name=_('Credentials Name')
#     )
#     account_type = models.CharField(
#         max_length=50, verbose_name="Account Type"
#     )
#     credentials_type = models.CharField(
#         blank=True, null=True,
#         max_length=128, verbose_name="Credentials Type"
#     )
#     user = models.ForeignKey(
#         'account.User', on_delete=models.CASCADE, blank=True, null=True,
#         verbose_name=_("User"), related_name="user_credential"
#     )
#     access_key_id = fields.EncryptCharField(
#         blank=True, null=True,
#         max_length=256, verbose_name="Access Key ID"
#     )
#     secret_access_key = fields.EncryptCharField(
#         blank=True, null=True,
#         max_length=256, verbose_name="Secret Access Key"
#     )
#     # role
#     role_arn = fields.EncryptCharField(
#         blank=True, null=True,
#         max_length=256, verbose_name="Amazon Credential Role Arn"
#     )
#     external_id = models.CharField(
#         max_length=128, verbose_name="External ID", null=True, blank=True
#     )
#     require_mfa = models.BooleanField(
#         default=False, blank=True, verbose_name="Require MFA"
#     )
#     is_local_role = models.BooleanField(
#         default=False, blank=True,
#         verbose_name="Whether to choose a local role"
#     )
#     google_service_account_key_json = JSONField(
#         default=dict, db_index=True, encoder=JSONEncoder,
#         verbose_name=_("Google Service Account Key JSON")
#     )
#     comment = models.TextField(
#         max_length=128, blank=True, verbose_name=_('Comment')
#     )
#     date_created = models.DateTimeField(
#         auto_now_add=True, verbose_name=_('Date created')
#     )
#     date_updated = models.DateTimeField(
#         auto_now=True, verbose_name=_("Date updated")
#     )
#     created_by = models.CharField(
#         max_length=128, null=True, verbose_name=_('Created by')
#     )
#
#     def __str__(self):
#         return '{0.user}({0.credentials_name})'.format(self)
#
#     class Meta:
#         # abstract = True
#         db_table = 'access_credential'
#         ordering = ['credentials_name']
#         unique_together = [('org_id', 'role_arn', 'access_key_id')]
#         verbose_name = _("Credential")
