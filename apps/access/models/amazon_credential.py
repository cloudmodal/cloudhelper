#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: amazon_credential.py
@ide: PyCharm
@time: 2020/2/10 20:56
@desc:
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common import fields
from .base import BaseModel


__all__ = ['AmazonCredentialRole']


class AmazonCredentialRole(BaseModel):
    user = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, blank=True, null=True,
        verbose_name=_("User"), related_name="user_aws_credential_role"
    )
    role_arn = fields.EncryptCharField(
        max_length=256, verbose_name="Amazon Credential Role Arn"
    )
    external_id = models.CharField(
        max_length=128, verbose_name="External ID", null=True, blank=True
    )
    require_mfa = models.BooleanField(
        default=False, blank=True, verbose_name="Require MFA"
    )
    is_local_role = models.BooleanField(
        default=False, blank=True,
        verbose_name=_("Choose local roles"),
        help_text=_(
            "For how to configure local roles, please refer to the "
            "<a href='https://docs.aws.amazon.com/cli/?id=docs_gateway' target='_blank'>"
            "AWS CLI</a> configuration and introduction"
        )
    )

    def __str__(self):
        return '{0.user}({0.credentials_name})'.format(self)

    class Meta:
        db_table = 'access_amazon_iam_role'
        ordering = ['role_arn']
        verbose_name = _("Amazon Credential Role")
