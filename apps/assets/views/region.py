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
from django.views.generic import TemplateView, CreateView, \
    UpdateView
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from common.permissions import PermissionsMixin, IsOrgAdmin
from common.const import create_success_msg, update_success_msg
from ..models import Region
from ..forms import RegionForm


class RegionListView(PermissionsMixin, TemplateView):
    template_name = 'assets/region_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Region list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class RegionCreateView(PermissionsMixin, CreateView):
    model = Region
    template_name = 'assets/region_create_update.html'
    form_class = RegionForm
    success_url = reverse_lazy('assets:region-list')
    success_message = create_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Create region'),
            'type': 'create'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class RegionUpdateView(PermissionsMixin, UpdateView):
    model = Region
    template_name = 'assets/region_create_update.html'
    form_class = RegionForm
    success_url = reverse_lazy('assets:region-list')
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Update region'),
            'type': 'update'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
