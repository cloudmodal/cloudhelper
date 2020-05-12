#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: admin_user.py
@ide: PyCharm
@time: 2020/5/9 16:58
@desc:
"""
# from django.db import transaction
# from django.shortcuts import get_object_or_404
# from rest_framework.response import Response
from organization.mixins.api import OrgBulkModelViewSet
from organization.mixins import generics

from common.utils import get_logger
from common.permissions import IsOrgAdmin
from ..models import AdminUser
from .. import serializers
# from ..tasks import test_admin_user_connectivity_manual


logger = get_logger(__file__)
__all__ = [
    'AdminUserViewSet',
    # 'ReplaceNodesAdminUserApi',
    # 'AdminUserTestConnectiveApi', 'AdminUserAuthApi',
    # 'AdminUserAssetsListView',
]


class AdminUserViewSet(OrgBulkModelViewSet):
    """
    Admin user api set, for add,delete,update,list,retrieve resource
    """
    model = AdminUser
    filter_fields = ("name", "username")
    search_fields = filter_fields
    serializer_class = serializers.AdminUserSerializer
    permission_classes = (IsOrgAdmin,)


class AdminUserAuthApi(generics.UpdateAPIView):
    model = AdminUser
    serializer_class = serializers.AdminUserAuthSerializer
    permission_classes = (IsOrgAdmin,)


# class ReplaceNodesAdminUserApi(generics.UpdateAPIView):
#     model = AdminUser
#     serializer_class = serializers.ReplaceNodeAdminUserSerializer
#     permission_classes = (IsOrgAdmin,)
#
#     def update(self, request, *args, **kwargs):
#         admin_user = self.get_object()
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             nodes = serializer.validated_data['nodes']
#             assets = []
#             for node in nodes:
#                 assets.extend([asset.id for asset in node.get_all_assets()])
#
#             with transaction.atomic():
#                 Asset.objects.filter(id__in=assets).update(admin_user=admin_user)
#
#             return Response({"msg": "ok"})
#         else:
#             return Response({'error': serializer.errors}, status=400)


# class AdminUserTestConnectiveApi(generics.RetrieveAPIView):
#     """
#     Test asset admin user assets_connectivity
#     """
#     model = AdminUser
#     permission_classes = (IsOrgAdmin,)
#     serializer_class = serializers.TaskIDSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         admin_user = self.get_object()
#         task = test_admin_user_connectivity_manual.delay(admin_user)
#         return Response({"task": task.id})
#
#
# class AdminUserAssetsListView(generics.ListAPIView):
#     permission_classes = (IsOrgAdmin,)
#     serializer_class = serializers.AssetSimpleSerializer
#     filter_fields = ("hostname", "ip")
#     http_method_names = ['get']
#     search_fields = filter_fields
#
#     def get_object(self):
#         pk = self.kwargs.get('pk')
#         return get_object_or_404(AdminUser, pk=pk)
#
#     def get_queryset(self):
#         admin_user = self.get_object()
#         return admin_user.get_related_assets()
