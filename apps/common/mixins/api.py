#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: api.py
@ide: PyCharm
@time: 2019/12/20 11:44
@desc:
"""
from django.http import JsonResponse
from rest_framework.settings import api_settings

from ..filters import IDSpmFilter, CustomFilter

__all__ = [
    "JSONResponseMixin", "CommonApiMixin",
    "IDSpmFilterMixin", "CommonApiMixin",
]


class JSONResponseMixin(object):
    """JSON mixin"""
    @staticmethod
    def render_json_response(context):
        return JsonResponse(context)


class IDSpmFilterMixin:
    def get_filter_backends(self):
        backends = super().get_filter_backends()
        backends.append(IDSpmFilter)
        return backends


class SerializerMixin:
    action = None
    request = None

    def get_serializer_class(self):
        serializer_class = None
        if hasattr(self, 'serializer_classes') and isinstance(self.serializer_classes, dict):
            if self.action == "list" or "retrieve":
                serializer_class = self.serializer_classes.get('display')
            if self.action == 'list' and self.request.query_params.get('draw'):
                serializer_class = self.serializer_classes.get('display')
            if serializer_class is None:
                serializer_class = self.serializer_classes.get(
                    self.action, self.serializer_classes.get('default')
                )
        if serializer_class:
            return serializer_class
        return super().get_serializer_class()


class ExtraFilterFieldsMixin:
    default_added_filters = [CustomFilter, IDSpmFilter]
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    extra_filter_fields = []
    extra_filter_backends = []

    def get_filter_backends(self):
        if self.filter_backends != self.__class__.filter_backends:
            return self.filter_backends
        return list(self.filter_backends) + self.default_added_filters + list(self.extra_filter_backends)

    def filter_queryset(self, queryset):
        for backend in self.get_filter_backends():
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class CommonApiMixin(SerializerMixin, ExtraFilterFieldsMixin):
    pass
