#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: tags.py
@ide: PyCharm
@time: 2020/5/12 13:30
@desc:
"""
from rest_framework import serializers

from common.serializers import AdaptedBulkListSerializer
from organization.mixins.serializers import BulkOrgResourceModelSerializer

from ..models import Tags


class TagsSerializer(BulkOrgResourceModelSerializer):
    asset_count = serializers.SerializerMethodField()

    class Meta:
        model = Tags
        fields = [
            'id', 'key', 'value', 'category', 'is_active', 'comment',
            'date_created', 'asset_count', 'assets', 'get_category_display'
        ]
        read_only_fields = (
            'category', 'date_created', 'asset_count', 'get_category_display'
        )
        list_serializer_class = AdaptedBulkListSerializer

    @staticmethod
    def get_asset_count(obj):
        return obj.assets.count()

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        fields.extend(['get_category_display'])
        return fields


class TagsDistinctSerializer(BulkOrgResourceModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = Tags
        fields = ("key", "value")

    @staticmethod
    def get_value(obj):
        labels = Tags.objects.filter(name=obj["key"])
        return ', '.join([label.value for label in labels])
