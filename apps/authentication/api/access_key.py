#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: access_key.py
@ide: PyCharm
@time: 2019/12/20 12:13
@desc:
"""
from rest_framework_bulk import BulkModelViewSet
from django.shortcuts import get_object_or_404
from organization.mixins import generics
from common.permissions import IsValidUser, IsOrgAdminOrAppUser
from .. import serializers
from ..models import AccessKey
from account.models import User
from ..utils import access_keys
__all__ = [
    'AccessKeyCreateView', 'AccessKeyViewSet', 'AccessKeyListView'
]


class AccessKeyCreateView(generics.CreateAPIView):
    """
    Create access key connective
    """
    serializer_class = serializers.AccessKeySerializer
    permission_classes = (IsValidUser,)

    def create(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        return access_keys(user)


class AccessKeyViewSet(BulkModelViewSet):
    permission_classes = (IsValidUser,)
    serializer_class = serializers.AccessKeySerializer
    search_fields = ["^access_key_id", "is_active", "date_created"]

    def get_queryset(self):
        return self.request.user.access_keys.all()

    def create(self, request, *args, **kwargs):
        user = self.request.user
        access_keys(user)


class AccessKeyListView(generics.ListAPIView):

    serializer_class = serializers.AccessKeySerializer
    permission_classes = [IsOrgAdminOrAppUser]
    http_method_names = ['get']
    filter_fields = [
        "id", "user", "access_key_id", "is_active", "date_created"
    ]
    search_fields = filter_fields

    def get_object(self):
        pk = self.kwargs.get('pk')
        return AccessKey.objects.filter(user=pk)

    def get_queryset(self):
        queryset = self.get_object()
        return queryset
