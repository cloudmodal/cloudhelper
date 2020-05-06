#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: forms.py
@ide: PyCharm
@time: 2020/4/24 14:05
@desc:
"""
import re
from django import forms
from django.utils.translation import gettext_lazy as _

from organization.mixins.forms import OrgModelForm
from . import models

SOURCE = ''
SOURCE_CHINA = 'amazon-china'
SOURCE_STANDARD = 'amazon-standard'
SOURCE_CHOICES = (
    (SOURCE_CHINA, 'Amazon China (Beijing, Ningxia)'),
    (SOURCE_STANDARD, 'Amazon Standard'),
)


class SecretAccessKeyAuthForm(forms.ModelForm):
    secret_access_key = forms.CharField(
        widget=forms.PasswordInput, required=False, strip=True,
        max_length=40, min_length=40, label=_("Secret Access Key"),
        help_text=_(
            'Leave the secret access key blank to keep the same value, otherwise specify a new secret access key.'
        ),
    )

    def clean_access_key_id(self):
        access_key_id = self.cleaned_data['access_key_id']
        key_id = '^[A-Za-z0-9_]{20}$'
        p = re.compile(key_id)
        if not p.match(access_key_id):
            msg = _('Access Key IDs must be 20 characters.')
            raise forms.ValidationError(msg, code='ids_invalid')
        return access_key_id

    def clean_secret_access_key(self):
        secret_access_key = self.cleaned_data['secret_access_key']
        if len(secret_access_key) != 40:
            msg = _('Secret Access Keys must be 40 characters.')
            # msg = _('Secret Access Keys must not contain any whitespace.')
            raise forms.ValidationError(msg, code='ids_invalid')
        return secret_access_key


class CredentialsUpdateForm(OrgModelForm):

    class Meta:
        model = models.StatisticsCredential
        fields = [
            'name', 'credential', 'credentials_name',
            'account_type', 'credential_type'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(CredentialsUpdateForm, self).__init__(*args, **kwargs)


class AccessKeyCreateUpdateFormMixin(OrgModelForm):

    class Meta:
        model = models.AccessKeys
        fields = [
            'credentials_name', 'account_type',
            'access_key_id', 'secret_access_key',
            'comment'
        ]
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'rows': '3',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(AccessKeyCreateUpdateFormMixin, self).__init__(*args, **kwargs)
        self.fields['access_key_id'].required = True

    def clean_access_key_id(self):
        access_key_id = self.cleaned_data['access_key_id']
        key_id = '^[A-Za-z0-9_]{20}$'
        p = re.compile(key_id)
        if not p.match(access_key_id):
            msg = _('Access Key IDs must be 20 characters.')
            raise forms.ValidationError(msg, code='ids_invalid')
        return access_key_id


class AmazonAccessKeyCreateForm(AccessKeyCreateUpdateFormMixin):
    account_type = forms.ChoiceField(
        choices=SOURCE_CHOICES, required=True
    )
    secret_access_key = forms.CharField(
        label=_("Secret Access Key"), strip=True,
        max_length=40, min_length=40
    )

    def clean_secret_access_key(self):
        secret_access_key = self.cleaned_data['secret_access_key']
        if len(secret_access_key) != 40:
            msg = _('Secret Access Keys must be 40 characters.')
            raise forms.ValidationError(msg, code='ids_invalid')
        return secret_access_key


class AmazonAccessKeyUpdateForm(AccessKeyCreateUpdateFormMixin):
    account_type = forms.ChoiceField(
        choices=SOURCE_CHOICES, required=True
    )
    secret_access_key = forms.CharField(
        label=_("Secret Access Key"), required=False,
        strip=True, max_length=40, min_length=40,
        help_text=_(
            'Leave the secret access key blank to keep the same value, otherwise specify a new secret access key.'
        ),
    )

    def clean_secret_access_key(self):
        secret_access_key = self.cleaned_data['secret_access_key']
        if secret_access_key and len(secret_access_key) != 40:
            msg = _('Secret Access Keys must be 40 characters.')
            raise forms.ValidationError(msg, code='ids_invalid')
        return secret_access_key


class AmazonRoleCreateUpdateFormMixin(OrgModelForm):
    account_type = forms.ChoiceField(
        choices=SOURCE_CHOICES, required=True
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(AmazonRoleCreateUpdateFormMixin, self).__init__(*args, **kwargs)
        self.fields['role_arn'].required = True

    def clean_role_arn(self):
        role_arn = self.cleaned_data['role_arn']
        if not re.match("^arn:(aws|aws-cn):iam::[0-9]{12}:role/.*$", role_arn) and role_arn:
            raise forms.ValidationError(_('Not a valid role ARN.'), code='ids_invalid')
        return role_arn

    # def clean(self):
    #     print(self.cleaned_data)
    #     role_arn = self.cleaned_data['role_arn']
    #     account_type = self.cleaned_data['account_type']
    #     if account_type == 'amazon-china':
    #         if not re.match("^arn:aws-cn:iam::[0-9]{12}:role/[ -~]{1,150}$", role_arn):
    #             raise forms.ValidationError(_('Not a valid role ARN.'), code='ids_invalid')
    #
    #     else:
    #         if not re.match("^arn:aws:iam::[0-9]{12}:role/[ -~]{1,150}$", role_arn):
    #             raise forms.ValidationError(_('Not a valid role ARN.'), code='ids_invalid')
    #
    #     return self.cleaned_data


class AmazonRoleCreate(AmazonRoleCreateUpdateFormMixin):

    class Meta:
        model = models.AmazonCredentialRole
        fields = [
            'credentials_name', 'role_arn', 'external_id',
            'require_mfa', 'account_type', 'is_local_role',
            'comment'
        ]
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'rows': '3',
                }
            ),
            'external_id': forms.HiddenInput(),
            'require_mfa': forms.HiddenInput(),
            'credential_type': forms.HiddenInput(),
        }


class AmazonRoleUpdate(AmazonRoleCreateUpdateFormMixin):
    external_id = forms.CharField(disabled=True, label=_("External id"))

    class Meta:
        model = models.AmazonCredentialRole
        fields = [
            'credentials_name', 'role_arn', 'external_id',
            'require_mfa', 'account_type', 'is_local_role',
            'comment'
        ]
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'rows': '3',
                }
            )
        }
