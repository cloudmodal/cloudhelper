#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: asset_config.py
@ide: PyCharm
@time: 2020/5/7 17:51
@desc:
"""
from django import forms
from django.utils.translation import gettext_lazy as _

# from common.utils import get_logger
from organization.mixins.forms import OrgModelForm

from ..models import AssetConfigs


class AssetConfigsCreateForm(OrgModelForm):
    SOURCE = ''
    SOURCE_AWS = 'aws'
    SOURCE_ALIYUN = 'aliyun'
    SOURCE_AZURE = 'azure'
    SOURCE_GOOGLE = 'google-cloud'
    SOURCE_TENCENT = 'tencent-cloud'
    SOURCE_HUAWEI = 'huawei-cloud'
    SOURCE_CHOICES = (
        (SOURCE_AWS, _('Amazon Web Services')),
        (SOURCE_ALIYUN, _('AliYun')),
        (SOURCE_AZURE, _('Azure')),
        (SOURCE_GOOGLE, _('Google Cloud Platform')),
        (SOURCE_TENCENT, _('Tencent Cloud')),
        (SOURCE_HUAWEI, _('HuaWei Cloud')),
    )
    account = forms.ChoiceField(
        choices=SOURCE_CHOICES, required=True
    )

    class Meta:
        model = AssetConfigs
        fields = [
            'name', 'account', 'credentials', 'region', 'default_admin_user',
            'state', 'comment'
        ]
