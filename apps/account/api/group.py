#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: group.py
@ide: PyCharm
@time: 2019/12/20 11:17
@desc:
"""
from ..serializers import (
    UserGroupSerializer,
    UserGroupDisplaySerializer,
    UserGroupListSerializer,
    UserGroupUpdateMemberSerializer,
)
from ..models import UserGroup
from organization.mixins.api import OrgBulkModelViewSet
from organization.mixins import generics
from common.permissions import IsOrgAdmin


__all__ = ['UserGroupViewSet', 'UserGroupUpdateUserApi']


class UserGroupViewSet(OrgBulkModelViewSet):
    model = UserGroup
    filter_fields = ("name",)
    search_fields = filter_fields
    serializer_class = UserGroupSerializer
    permission_classes = (IsOrgAdmin,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserGroupDisplaySerializer
        if self.action in ("list", 'retrieve') and self.request.query_params.get("display"):
            return UserGroupListSerializer
        return self.serializer_class


class UserGroupUpdateUserApi(generics.RetrieveUpdateAPIView):
    model = UserGroup
    serializer_class = UserGroupUpdateMemberSerializer
    permission_classes = (IsOrgAdmin,)
