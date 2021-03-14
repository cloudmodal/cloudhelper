#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: asset.py
@ide: PyCharm
@time: 2020/5/15 16:20
@desc:
"""
import random

from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin, IsOrgAdminOrAppUser
from organization.mixins.api import OrgBulkModelViewSet
from organization.mixins import generics
from ..models import Asset  # Node
from .. import serializers
# from ..tasks import update_asset_hardware_info_manual, \
#     test_asset_connectivity_manual
from ..filters import AssetByRegionFilterBackend, TagsFilterBackend


logger = get_logger(__file__)
__all__ = [
    'AssetViewSet',
    # 'AssetRefreshHardwareApi', 'AssetAdminUserTestApi',
    # 'AssetGatewayApi',
]


class AssetViewSet(OrgBulkModelViewSet):
    """
    API endpoint that allows Asset to be viewed or edited.
    """
    model = Asset
    filter_fields = ("hostname", "ip", "systemuser__id", "admin_user__id")
    search_fields = ("hostname", "ip")
    ordering_fields = ("hostname", "ip", "port", "cpu_cores")
    serializer_class = serializers.AssetSerializer
    permission_classes = (IsOrgAdminOrAppUser,)
    extra_filter_backends = [AssetByRegionFilterBackend, TagsFilterBackend]

    # def set_assets_node(self, assets):
    #     if not isinstance(assets, list):
    #         assets = [assets]
    #     node_id = self.request.query_params.get('node_id')
    #     if not node_id:
    #         return
    #     node = get_object_or_none(Node, pk=node_id)
    #     if not node:
    #         return
    #     node.assets.add(*assets)

    # def perform_create(self, serializer):
    #     assets = serializer.save()
    #     self.set_assets_node(assets)


# class AssetRefreshHardwareApi(generics.RetrieveAPIView):
#     """
#     Refresh asset hardware info
#     """
#     model = Asset
#     serializer_class = serializers.AssetSerializer
#     permission_classes = (IsOrgAdmin,)
#
#     def retrieve(self, request, *args, **kwargs):
#         asset_id = kwargs.get('pk')
#         asset = get_object_or_404(Asset, pk=asset_id)
#         task = update_asset_hardware_info_manual.delay(asset)
#         return Response({"task": task.id})


# class AssetAdminUserTestApi(generics.RetrieveAPIView):
#     """
#     Test asset admin user assets_connectivity
#     """
#     model = Asset
#     permission_classes = (IsOrgAdmin,)
#     serializer_class = serializers.TaskIDSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         asset_id = kwargs.get('pk')
#         asset = get_object_or_404(Asset, pk=asset_id)
#         task = test_asset_connectivity_manual.delay(asset)
#         return Response({"task": task.id})


