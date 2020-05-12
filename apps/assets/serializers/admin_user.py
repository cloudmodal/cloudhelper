#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: admin_user.py
@ide: PyCharm
@time: 2020/5/9 16:54
@desc:
"""
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from common.serializers import AdaptedBulkListSerializer

from ..models import AdminUser
from organization.mixins.serializers import BulkOrgResourceModelSerializer

from .base import AuthSerializer, AuthSerializerMixin


class AdminUserSerializer(AuthSerializerMixin, BulkOrgResourceModelSerializer):
    """
    管理用户
    """

    class Meta:
        list_serializer_class = AdaptedBulkListSerializer
        model = AdminUser
        fields = [
            'id', 'name', 'username', 'password', 'private_key', 'public_key',
            'comment', 'assets_amount', 'date_created', 'date_updated', 'created_by',
        ]
        read_only_fields = ['date_created', 'date_updated', 'created_by', 'assets_amount']

        extra_kwargs = {
            'password': {"write_only": True},
            'private_key': {"write_only": True},
            'public_key': {"write_only": True},
            'assets_amount': {'label': _('Asset')},
        }


class AdminUserAuthSerializer(AuthSerializer):

    class Meta:
        model = AdminUser
        fields = ['password', 'private_key']


# class ReplaceNodeAdminUserSerializer(serializers.ModelSerializer):
#     """
#     管理用户更新关联到的集群
#     """
#     nodes = serializers.PrimaryKeyRelatedField(
#         many=True, queryset=Node.objects
#     )
#
#     class Meta:
#         model = AdminUser
#         fields = ['id', 'nodes']


class TaskIDSerializer(serializers.Serializer):
    task = serializers.CharField(read_only=True)
