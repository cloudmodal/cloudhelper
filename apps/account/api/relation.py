#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: relation.py
@ide: PyCharm
@time: 2019/12/20 11:53
@desc:
"""
from rest_framework_bulk import BulkModelViewSet
from django.db.models import F

from common.permissions import IsOrgAdmin
from .. import serializers
from ..models import User

__all__ = ['UserUserGroupRelationViewSet']


class UserUserGroupRelationViewSet(BulkModelViewSet):
    filter_fields = ('user', 'usergroup')
    search_fields = filter_fields
    serializer_class = serializers.UserUserGroupRelationSerializer
    permission_classes = (IsOrgAdmin,)

    def get_queryset(self):
        queryset = User.groups.through.objects.all()\
            .annotate(user_name=F('user__name'))\
            .annotate(usergroup_name=F('usergroup__name'))
        return queryset

    def allow_bulk_destroy(self, qs, filtered):
        if filtered.count() != 1:
            return False
        else:
            return True
