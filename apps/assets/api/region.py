#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: region.py
@ide: PyCharm
@time: 2021/2/27 16:13
@desc:
"""
from django.db.models import Count

from common.utils import get_logger
from organization.mixins.api import OrgBulkModelViewSet
from common.permissions import IsOrgAdmin
from ..models import Region
from .. import serializers


logger = get_logger(__file__)
__all__ = ['RegionViewSet']


class RegionViewSet(OrgBulkModelViewSet):
    model = Region
    queryset = Region.objects.all()
    filter_fields = ("name", "owner", "telephone")
    search_fields = filter_fields
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.RegionSerializer

    def list(self, request, *args, **kwargs):
        if request.query_params.get("distinct"):
            self.serializer_class = serializers.RegionSerializer
            self.queryset = self.queryset.values("name").distinct()
        # elif request.query_params.get("tree"):
        #     _data = [
        #         {
        #             'id': region.id,
        #             'name': region.name,
        #             'pId': region.parent.id if region.parent else 0, 'open': True
        #         } for region in self.queryset
        #     ]
        #     self.queryset = _data
        #     print(self.queryset)
        #     self.serializer_class = serializers.RegionTreeSerializer
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = Region.objects.annotate(asset_count=Count("assets_region"))
        self.queryset = Region.objects.all()
        return self.queryset
