#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: region.py
@ide: PyCharm
@time: 2021/2/27 12:31
@desc:
"""
from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import Region, Asset


__all__ = ['RegionForm']


class RegionForm(forms.ModelForm):
    assets = forms.ModelMultipleChoiceField(
        queryset=Asset.objects.none(), label=_('Asset'), required=False,
        widget=forms.SelectMultiple(
            attrs={'class': 'select2', 'data-placeholder': _('Select assets')}
        )
    )

    class Meta:
        model = Region
        fields = [
            'parent', 'assets', 'name', 'owner',
            'telephone', 'address', 'comment'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.set_fields_queryset()

    def set_fields_queryset(self):
        assets_field = self.fields.get('assets')
        # 没有data代表是渲染表单, 有data代表是提交创建/更新表单
        if not self.data:
            # 有instance 代表渲染更新表单, 否则是创建表单
            # 前端渲染优化, 防止过多资产, 设置assets queryset为none
            if self.instance:
                assets_field.initial = self.instance.assets_region.all()
                assets_field.queryset = self.instance.assets_region.all()
            else:
                assets_field.queryset = Asset.objects.none()
        else:
            assets_field.queryset = Asset.objects.all()

    def save(self, commit=True):
        region = super().save(commit=commit)
        assets = self.cleaned_data['assets']
        region.assets_region.set(assets)
        return region
