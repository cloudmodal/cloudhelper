#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: region.py
@ide: PyCharm
@time: 2021/2/27 12:52
@desc:
"""
from rest_framework import serializers
from common.serializers import AdaptedBulkListSerializer
from organization.mixins.serializers import BulkOrgResourceModelSerializer

from ..models import Region


class RegionSerializer(BulkOrgResourceModelSerializer):
    open = serializers.SerializerMethodField(read_only=True)
    asset_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Region
        fields = [
            'id', 'parent', 'name', 'owner', 'telephone',
            'address', 'asset_count', 'assets_region',
            'open', 'date_created', 'comment'
        ]
        read_only_fields = (
            'assets_region', 'asset_count', 'date_created'
        )
        list_serializer_class = AdaptedBulkListSerializer

    @staticmethod
    def get_open(obj):
        if obj.name == 'Default':
            return True
        else:
            return False

    @staticmethod
    def get_asset_count(obj):
        return obj.assets_region.count()

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        return fields
