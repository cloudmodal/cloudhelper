#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: system_user.py
@ide: PyCharm
@time: 2020/5/11 18:25
@desc:
"""
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.response import Response

from common.serializers import CeleryTaskSerializer
from common.utils import get_logger
from common.permissions import IsOrgAdmin, IsOrgAdminOrAppUser, IsAppUser
from organization.mixins.api import OrgBulkModelViewSet
from organization.mixins import generics
from ..models import SystemUser
from .. import serializers
# from ..tasks import (
#     push_system_user_to_assets_manual, test_system_user_connectivity_manual,
#     push_system_user_a_asset_manual, test_system_user_connectivity_a_asset,
# )


logger = get_logger(__file__)
__all__ = [
    'SystemUserViewSet', 'SystemUserAuthInfoApi',
    # 'SystemUserAssetAuthInfoApi',
    # 'SystemUserPushApi', 'SystemUserTestConnectiveApi',
    # 'SystemUserAssetsListView', 'SystemUserPushToAssetApi',
    # 'SystemUserTestAssetConnectivityApi', 'SystemUserCommandFilterRuleListApi',

]


class SystemUserViewSet(OrgBulkModelViewSet):
    """
    System user api set, for add,delete,update,list,retrieve resource
    """
    model = SystemUser
    filter_fields = ("name", "username")
    search_fields = filter_fields
    serializer_class = serializers.SystemUserSerializer
    permission_classes = (IsOrgAdminOrAppUser,)


class SystemUserAuthInfoApi(generics.RetrieveUpdateDestroyAPIView):
    """
    Get system user auth info
    """
    model = SystemUser
    permission_classes = (IsOrgAdminOrAppUser,)
    serializer_class = serializers.SystemUserAuthSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.clear_auth()
        return Response(status=204)


# class SystemUserAssetAuthInfoApi(generics.RetrieveAPIView):
#     """
#     Get system user with asset auth info
#     """
#     model = SystemUser
#     permission_classes = (IsAppUser,)
#     serializer_class = serializers.SystemUserAuthSerializer
#
#     def get_object(self):
#         instance = super().get_object()
#         aid = self.kwargs.get('aid')
#         asset = get_object_or_404(Asset, pk=aid)
#         instance.load_specific_asset_auth(asset)
#         return instance


# class SystemUserPushApi(generics.RetrieveAPIView):
#     """
#     Push system user to cluster assets api
#     """
#     model = SystemUser
#     permission_classes = (IsOrgAdmin,)
#     serializer_class = CeleryTaskSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         system_user = self.get_object()
#         nodes = system_user.nodes.all()
#         for node in nodes:
#             system_user.assets.add(*tuple(node.get_all_assets()))
#         task = push_system_user_to_assets_manual.delay(system_user)
#         return Response({"task": task.id})


# class SystemUserTestConnectiveApi(generics.RetrieveAPIView):
#     """
#     Push system user to cluster assets api
#     """
#     model = SystemUser
#     permission_classes = (IsOrgAdmin,)
#     serializer_class = CeleryTaskSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         system_user = self.get_object()
#         task = test_system_user_connectivity_manual.delay(system_user)
#         return Response({"task": task.id})


# class SystemUserAssetsListView(generics.ListAPIView):
#     permission_classes = (IsOrgAdmin,)
#     serializer_class = serializers.AssetSimpleSerializer
#     filter_fields = ("hostname", "ip")
#     http_method_names = ['get']
#     search_fields = filter_fields
#
#     def get_object(self):
#         pk = self.kwargs.get('pk')
#         return get_object_or_404(SystemUser, pk=pk)
#
#     def get_queryset(self):
#         system_user = self.get_object()
#         return system_user.assets.all()


# class SystemUserPushToAssetApi(generics.RetrieveAPIView):
#     model = SystemUser
#     permission_classes = (IsOrgAdmin,)
#     serializer_class = serializers.TaskIDSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         system_user = self.get_object()
#         asset_id = self.kwargs.get('aid')
#         asset = get_object_or_404(Asset, id=asset_id)
#         task = push_system_user_a_asset_manual.delay(system_user, asset)
#         return Response({"task": task.id})


# class SystemUserTestAssetConnectivityApi(generics.RetrieveAPIView):
#     model = SystemUser
#     permission_classes = (IsOrgAdmin,)
#     serializer_class = serializers.TaskIDSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         system_user = self.get_object()
#         asset_id = self.kwargs.get('aid')
#         asset = get_object_or_404(Asset, id=asset_id)
#         task = test_system_user_connectivity_a_asset.delay(system_user, asset)
#         return Response({"task": task.id})


# class SystemUserCommandFilterRuleListApi(generics.ListAPIView):
#     permission_classes = (IsOrgAdminOrAppUser,)
#
#     def get_serializer_class(self):
#         from ..serializers import CommandFilterRuleSerializer
#         return CommandFilterRuleSerializer
#
#     def get_queryset(self):
#         pk = self.kwargs.get('pk', None)
#         system_user = get_object_or_404(SystemUser, pk=pk)
#         return system_user.cmd_filter_rules
