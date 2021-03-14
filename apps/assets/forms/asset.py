#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: asset.py
@ide: PyCharm
@time: 2020/5/12 15:09
@desc:
"""
from django import forms
from django.utils.translation import gettext_lazy as _

from common.utils import get_logger
from organization.mixins.forms import OrgModelForm

from ..models import Asset
from ..const import GENERAL_FORBIDDEN_SPECIAL_CHARACTERS_HELP_TEXT


logger = get_logger(__file__)
__all__ = [
    'AssetCreateForm', 'AssetUpdateForm', 'AssetBulkUpdateForm', 'ProtocolForm',
]


class ProtocolForm(forms.Form):
    name = forms.ChoiceField(
        choices=Asset.PROTOCOL_CHOICES, label=_("Name"), initial='ssh',
        widget=forms.Select(attrs={'class': 'form-control protocol-name'})
    )
    port = forms.IntegerField(
        max_value=65534, min_value=1, label=_("Port"), initial=22,
        widget=forms.TextInput(attrs={'class': 'form-control protocol-port'})
    )


class AssetCreateForm(OrgModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Asset
        fields = [
            'hostname', 'ip', 'public_ip', 'protocol', 'comment',
            'instance_id', 'instance_type', 'instance_state',
            'is_active', 'admin_user', 'tags', 'platform', 'region'
        ]
        widgets = {
            # 'admin_user': forms.Select(attrs={
            #     'class': 'select2', 'data-placeholder': _('Admin user')
            # }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'select2', 'data-placeholder': _('Tags')
            }),
        }
        help_texts = {
            'hostname': GENERAL_FORBIDDEN_SPECIAL_CHARACTERS_HELP_TEXT,
            'admin_user': _(
                'root or other NOPASSWD sudo privilege user existed in asset,'
                'If asset is windows or other set any one, more see admin user left menu'
            ),
            'platform': _("Windows 2016 RDP protocol is different, If is window 2016, set it")
        }


class AssetUpdateForm(OrgModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Asset
        fields = [
            'hostname', 'ip', 'public_ip', 'protocol', 'comment',
            'instance_id', 'instance_type', 'instance_state',
            'is_active', 'admin_user', 'tags', 'platform', 'region'
        ]
        widgets = {
            # 'admin_user': forms.Select(attrs={
            #     'class': 'select2', 'data-placeholder': _('Admin user')
            # }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'select2', 'data-placeholder': _('Tags')
            }),
        }
        help_texts = {
            'hostname': GENERAL_FORBIDDEN_SPECIAL_CHARACTERS_HELP_TEXT,
            'admin_user': _(
                'root or other NOPASSWD sudo privilege user existed in asset,'
                'If asset is windows or other set any one, more see admin user left menu'
            ),
            'platform': _("Windows 2016 RDP protocol is different, If is window 2016, set it"),
        }


class AssetBulkUpdateForm(OrgModelForm):
    assets = forms.ModelMultipleChoiceField(
        required=True,
        label=_('Select assets'), queryset=Asset.objects,
        widget=forms.SelectMultiple(
            attrs={
                'class': 'select2',
                'data-placeholder': _('Select assets')
            }
        )
    )

    class Meta:
        model = Asset
        fields = [
            'assets', 'admin_user', 'tags', 'platform', 'region'
        ]
        widgets = {
            'tags': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _('Tags')}
            ),
            'nodes': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _('Node')}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_fields_queryset()

        # 重写其他字段为不再required
        for name, field in self.fields.items():
            if name != 'assets':
                field.required = False

    def set_fields_queryset(self):
        assets_field = self.fields['assets']
        if hasattr(self, 'data'):
            assets_field.queryset = Asset.objects.all()

    def save(self, commit=True):
        changed_fields = []
        for field in self._meta.fields:
            if self.data.get(field) not in [None, '']:
                changed_fields.append(field)

        cleaned_data = {k: v for k, v in self.cleaned_data.items()
                        if k in changed_fields}
        assets = cleaned_data.pop('assets')
        labels = cleaned_data.pop('labels', [])
        nodes = cleaned_data.pop('nodes', None)
        assets = Asset.objects.filter(id__in=[asset.id for asset in assets])
        assets.update(**cleaned_data)

        if labels:
            for asset in assets:
                asset.labels.set(labels)
        if nodes:
            for asset in assets:
                asset.nodes.set(nodes)
        return assets
