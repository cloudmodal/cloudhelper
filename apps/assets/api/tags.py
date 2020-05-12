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
from django.db.models import Count

from common.utils import get_logger
from organization.mixins.api import OrgBulkModelViewSet
from common.permissions import IsOrgAdmin
from ..models import Tags
from .. import serializers


logger = get_logger(__file__)
__all__ = ['TagsViewSet']


class TagsViewSet(OrgBulkModelViewSet):
    model = Tags
    filter_fields = ("key", "value")
    search_fields = filter_fields
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.TagsSerializer

    def list(self, request, *args, **kwargs):
        if request.query_params.get("distinct"):
            self.serializer_class = serializers.TagsDistinctSerializer
            self.queryset = self.queryset.values("key").distinct()
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = Tags.objects.annotate(asset_count=Count("assets"))
        return self.queryset
