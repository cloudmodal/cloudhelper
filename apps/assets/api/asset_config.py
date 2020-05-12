#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: asset_config.py
@ide: PyCharm
@time: 2020/5/9 23:42
@desc:
"""
from organization.mixins.api import OrgBulkModelViewSet

from common.utils import get_logger
from common.permissions import IsOrgAdmin
from ..models import AssetConfigs
from .. import serializers


logger = get_logger(__file__)
__all__ = [
    'AssetConfigViewSet',
]


class AssetConfigViewSet(OrgBulkModelViewSet):
    """
    Asset config api set, for add,delete,update,list,retrieve resource
    """
    model = AssetConfigs
    filter_fields = ("name", "account")
    search_fields = filter_fields
    serializer_class = serializers.AssetConfigSerializer
    permission_classes = (IsOrgAdmin,)
