#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: api.py
@ide: PyCharm
@time: 2020/1/2 18:43
@desc:
"""
from rest_framework import status
from rest_framework.views import Response
from rest_framework_bulk import BulkModelViewSet

from common.permissions import (
    IsSuperUserOrAppUser
)
from .models import Organization
from .serializers import (
    OrgSerializer, OrgReadSerializer, OrgMembershipUserSerializer,
    OrgMembershipAdminSerializer
)
from account.models import User, UserGroup
from organization.utils import current_org
from common.utils import get_logger
from .mixins.api import OrgMembershipModelViewSetMixin

logger = get_logger(__file__)


class OrgViewSet(BulkModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrgSerializer
    permission_classes = (IsSuperUserOrAppUser,)
    org = None

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OrgReadSerializer
        else:
            return super().get_serializer_class()

    def get_data_from_model(self, model):
        if model == User:
            data = model.objects.filter(related_user_orgs__id=self.org.id)
        else:
            data = model.objects.filter(org_id=self.org.id)
        return data

    def destroy(self, request, *args, **kwargs):
        self.org = self.get_object()
        models = [
            User, UserGroup,
        ]
        for model in models:
            data = self.get_data_from_model(model)
            if data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if str(current_org) == str(self.org):
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            self.org.delete()
            return Response({'msg': True}, status=status.HTTP_200_OK)


class OrgMembershipAdminsViewSet(OrgMembershipModelViewSetMixin, BulkModelViewSet):
    serializer_class = OrgMembershipAdminSerializer
    membership_class = Organization.admins.through
    permission_classes = (IsSuperUserOrAppUser, )


class OrgMembershipUsersViewSet(OrgMembershipModelViewSetMixin, BulkModelViewSet):
    serializer_class = OrgMembershipUserSerializer
    membership_class = Organization.users.through
    permission_classes = (IsSuperUserOrAppUser, )


# class GetJoinedOrganizations(generics.RetrieveAPIView):
#     permission_classes = (IsSuperUser, IsOrgAdmin)
#
#     def get_object(self):
#         return self.request.user.related_admin_orgs.all()
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = OrgReadSerializer(instance, many=True)
#
#         if serializer:
#             return Response({'code': 200, 'data': serializer.data, 'msg': '请求成功'}, status=200)
#         else:
#             return Response(
#                 {'code': 200, 'data': [], 'msg': '请求成功,当前用户还未加入任何组织'}, status=200
#             )
