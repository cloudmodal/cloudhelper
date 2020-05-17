#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: asset.py
@ide: PyCharm
@time: 2020/5/12 15:10
@desc:
"""
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.core.cache import cache
from django.shortcuts import redirect
from django.forms.formsets import formset_factory

from common.utils import get_logger
from common.permissions import PermissionsMixin, IsOrgAdmin, IsValidUser
from common.const import KEY_CACHE_RESOURCES_ID
from .. import forms
from ..models import Asset, Tags


__all__ = [
    'AssetListView', 'AssetCreateView', 'AssetUpdateView',
    # 'AssetUserListView', 'UserAssetListView',
    'AssetBulkUpdateView', 'AssetDetailView',
]
logger = get_logger(__file__)


class AssetListView(PermissionsMixin, TemplateView):
    template_name = 'assets/asset_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        # Node.org_root()
        context = {
            'app': _('Assets'),
            'action': _('Asset list'),
            'tags': Tags.objects.all().order_by('name'),
            # 'nodes': Node.objects.all().order_by('-key'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


# class AssetUserListView(PermissionsMixin, DetailView):
#     model = Asset
#     context_object_name = 'asset'
#     template_name = 'assets/asset_asset_user_list.html'
#     permission_classes = [IsOrgAdmin]
#
#     def get_context_data(self, **kwargs):
#         context = {
#             'app': _('Assets'),
#             'action': _('Asset user list'),
#         }
#         kwargs.update(context)
#         return super().get_context_data(**kwargs)
#
#
# class UserAssetListView(PermissionsMixin, TemplateView):
#     template_name = 'assets/user_asset_list.html'
#     permission_classes = [IsValidUser]
#
#     def get_context_data(self, **kwargs):
#         context = {
#             'action': _('My assets'),
#             'labels': Label.objects.all().order_by('name'),
#             'show_actions': True
#         }
#         kwargs.update(context)
#         return super().get_context_data(**kwargs)


class AssetCreateView(PermissionsMixin, FormMixin, TemplateView):
    model = Asset
    form_class = forms.AssetCreateForm
    template_name = 'assets/asset_create.html'
    success_url = reverse_lazy('assets:asset-list')
    permission_classes = [IsOrgAdmin]

    def get_protocol_formset(self):
        protocol_formset = formset_factory(forms.ProtocolForm, extra=0, min_num=1, max_num=5)
        if self.request.method == "POST":
            formset = protocol_formset(self.request.POST)
        else:
            formset = protocol_formset()
        return formset

    def get_context_data(self, **kwargs):
        formset = self.get_protocol_formset()
        context = {
            'app': _('Assets'),
            'action': _('Create asset'),
            'formset': formset,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AssetUpdateView(PermissionsMixin, UpdateView):
    model = Asset
    form_class = forms.AssetUpdateForm
    template_name = 'assets/asset_update.html'
    success_url = reverse_lazy('assets:asset-list')
    permission_classes = [IsOrgAdmin]

    def get_protocol_formset(self):
        protocol_formset = formset_factory(forms.ProtocolForm, extra=0, min_num=1, max_num=5)
        if self.request.method == "POST":
            formset = protocol_formset(self.request.POST)
        else:
            initial_data = self.object.protocols_as_json
            formset = protocol_formset(initial=initial_data)
        return formset

    def get_context_data(self, **kwargs):
        formset = self.get_protocol_formset()
        context = {
            'app': _('Assets'),
            'action': _('Update asset'),
            'formset': formset,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AssetBulkUpdateView(PermissionsMixin, ListView):
    model = Asset
    form_class = forms.AssetBulkUpdateForm
    template_name = 'assets/asset_bulk_update.html'
    success_url = reverse_lazy('assets:asset-list')
    success_message = _("Bulk update asset success")
    id_list = None
    form = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        spm = request.GET.get('spm', '')
        assets_id = cache.get(KEY_CACHE_RESOURCES_ID.format(spm))
        if kwargs.get('form'):
            self.form = kwargs['form']
        elif assets_id:
            self.form = self.form_class(initial={'assets': assets_id})
        else:
            self.form = self.form_class()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        else:
            return self.get(request, form=form, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Bulk update asset'),
            'form': self.form,
            'assets_selected': self.id_list,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AssetDetailView(PermissionsMixin, DetailView):
    model = Asset
    context_object_name = 'asset'
    template_name = 'assets/asset_detail.html'
    permission_classes = [IsValidUser]

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            "tags",
        ).select_related('admin_user')

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Asset detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
