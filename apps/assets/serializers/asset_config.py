#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: asset_config.py
@ide: PyCharm
@time: 2020/5/9 23:38
@desc:
"""
from common.serializers import AdaptedBulkListSerializer
from organization.mixins.serializers import BulkOrgResourceModelSerializer

from ..models import AssetConfigs
from .base import AuthSerializerMixin


class AssetConfigSerializer(AuthSerializerMixin, BulkOrgResourceModelSerializer):
    """
    管理用户
    """

    class Meta:
        list_serializer_class = AdaptedBulkListSerializer
        model = AssetConfigs
        fields = [
            'id', 'name', 'account', 'credentials', 'region', 'default_admin_user',
            'state', 'comment', 'date_created', 'date_updated', 'created_by',
        ]
        read_only_fields = ['date_created', 'date_updated', 'created_by']

        extra_kwargs = {
            'password': {"write_only": True},
            'private_key': {"write_only": True},
            'public_key': {"write_only": True},
        }
