#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: tags.py
@ide: PyCharm
@time: 2020/5/12 11:56
@desc:
"""
from django.views.generic import TemplateView, CreateView, \
    UpdateView, DeleteView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from common.permissions import PermissionsMixin, IsOrgAdmin
from common.const import create_success_msg, update_success_msg
from ..models import Tags
from ..forms import TagsForm


__all__ = (
    "TagsListView", "TagsCreateView", "TagsUpdateView",
    "TagsDetailView", "TagsDeleteView",
)


class TagsListView(PermissionsMixin, TemplateView):
    template_name = 'assets/tags_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Tags list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TagsCreateView(PermissionsMixin, CreateView):
    model = Tags
    template_name = 'assets/tags_create_update.html'
    form_class = TagsForm
    success_url = reverse_lazy('assets:tags-list')
    success_message = create_success_msg
    disable_name = ['draw', 'search', 'limit', 'offset', '_']
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Create label'),
            'type': 'create'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        name = form.cleaned_data.get('key')
        if name in self.disable_name:
            msg = _(
                'Tips: Avoid using label names reserved internally: {}'
            ).format(', '.join(self.disable_name))
            form.add_error("key", msg)
            return self.form_invalid(form)
        return super().form_valid(form)


class TagsUpdateView(PermissionsMixin, UpdateView):
    model = Tags
    template_name = 'assets/tags_create_update.html'
    form_class = TagsForm
    success_url = reverse_lazy('assets:tags-list')
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Update label'),
            'type': 'update'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TagsDetailView(PermissionsMixin, DetailView):
    pass


class TagsDeleteView(PermissionsMixin, DeleteView):
    model = Tags
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('assets:label-list')
    permission_classes = [IsOrgAdmin]
