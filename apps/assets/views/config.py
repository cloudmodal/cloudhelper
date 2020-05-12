#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: config.py
@ide: PyCharm
@time: 2020/5/7 17:30
@desc:
"""
from django.views.generic import TemplateView, CreateView, \
    UpdateView, DeleteView, DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, reverse

from common.permissions import PermissionsMixin, IsOrgAdmin
from common.const import create_success_msg, update_success_msg
from ..models import AssetConfigs
from .. import forms


__all__ = (
    "AssetConfigListView", "AssetConfigCreateView",
    "AssetConfigUpdateView", "AssetConfigDetailView",
    # "CommandFilterRuleListView", "CommandFilterRuleCreateView",
    # "CommandFilterRuleUpdateView", "CommandFilterDetailView",
)


class AssetConfigListView(PermissionsMixin, TemplateView):
    template_name = 'assets/asset_config_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Assets config'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AssetConfigCreateView(PermissionsMixin, SuccessMessageMixin, CreateView):
    model = AssetConfigs
    form_class = forms.AssetConfigsCreateForm
    template_name = 'assets/asset_config_create_update.html'
    success_url = reverse_lazy('assets:asset-config')
    success_message = create_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Create asset config'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AssetConfigUpdateView(PermissionsMixin, SuccessMessageMixin, UpdateView):
    model = AssetConfigs
    form_class = forms.AssetConfigsCreateForm
    template_name = 'assets/asset_config_create_update.html'
    success_url = reverse_lazy('assets:asset-config')
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Update asset config'),
            "type": "update"
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AssetConfigDetailView(PermissionsMixin, DetailView):
    model = AssetConfigs
    template_name = 'assets/asset_config_detail.html'
    context_object_name = 'asset_config'
    object = None
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Asset config detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
