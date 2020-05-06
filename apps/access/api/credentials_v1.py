#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: credentials_v1.py
@ide: PyCharm
@time: 2020/2/12 15:37
@desc:
"""
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from django.db.utils import IntegrityError
from botocore.exceptions import ClientError
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.utils.translation import ugettext_lazy as _

from common.aws_connection.aws_helper import AwsHelper
from common.permissions import IsValidUser, IsOrgAdminOrAppUser
from common.utils import get_logger, get_object_or_none
from organization.mixins.api import OrgBulkModelViewSet
from .. import serializers
from .. import models
from .. import utils


__all__ = [
    "CredentialViewSet", "CredentialsAPIView",
    "AmazonCredentialsViewSet",
    "AmazonCredentialsRoleViewSet"
]


logger = get_logger(__name__)


class CredentialViewSet(OrgBulkModelViewSet):
    model = models.StatisticsCredential
    permission_classes = (IsValidUser,)
    serializer_class = serializers.CredentialSerializer
    search_fields = [
        '^account_type', '^credentials_name', '^credential_type'
    ]
    http_method_names = ['get']


class CredentialsAPIView(APIView):
    permission_classes = (IsOrgAdminOrAppUser,)
    http_method_names = ['get']

    def get(self, request):
        query_params = self.request.query_params
        credentials_id = query_params.get('credentials_id')
        credentials_type = query_params.get('type')
        if credentials_type == 'amazon-access-key' and credentials_id:
            access_key = get_object_or_none(models.AmazonCredential, pk=credentials_id)
            if access_key:
                serializer = serializers.AmazonCredentialSerializer(access_key)
            else:
                return Response({'code': 404, 'detail': '凭证不存在'}, status.HTTP_404_NOT_FOUND)

        elif credentials_type == 'amazon-iam-role' and credentials_id:
            iam_role = get_object_or_none(models.AmazonCredentialRole, pk=credentials_id)
            if iam_role:
                serializer = serializers.AmazonCredentialRoleSerializer(iam_role)
            else:
                return Response({'code': 404, 'detail': '凭证不存在'}, status.HTTP_404_NOT_FOUND)

        else:
            raise ValidationError({'code': 400, 'detail': 'The params is incorrect'})

        return Response(serializer.data, status.HTTP_200_OK)


class AmazonCredentialsViewSet(OrgBulkModelViewSet):
    serializer_class = serializers.AmazonCredentialSerializer
    permission_classes = [IsOrgAdminOrAppUser]
    # http_method_names = ['get', 'post']
    filter_fields = [
        "id", "user", "credentials_name", "credential_type",
        "date_created", "date_updated"
    ]
    search_fields = filter_fields

    def get_queryset(self):
        from organization.utils import current_org
        if current_org.can_admin_by(self.request.user):
            queryset = models.AmazonCredential.objects.all()
        else:
            queryset = self.request.user.user_credential.all()
        return queryset

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return serializers.AmazonCredentialAdminSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        # 获取相关serializer
        serializer = self.get_serializer(data=request.data)
        # 进行serializer的验证
        # raise_exception=True,一旦验证不通过，不再往下执行，直接引发异常
        serializer.is_valid(raise_exception=True)
        # 调用perform_create()方法，保存实例
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        action = serializer.save()
        action.user = self.request.user
        action.credential_type = 'Amazon Access Key'
        action.created_by = self.request.user.username
        if utils.credentials_amount(self.request.user):
            raise ValidationError({"code": 400, "msg": "您的凭证已经达到最大限制!"})
        try:
            action.save()
        except IntegrityError as e:
            raise ValidationError({"code": 400, "msg": "具有相同的凭证已存在，无法再次增加！", "data": [e]})


class AmazonCredentialsRoleViewSet(OrgBulkModelViewSet):
    serializer_class = serializers.AmazonCredentialRoleSerializer
    permission_classes = [IsOrgAdminOrAppUser]
    filter_fields = [
        "id", "user", "credentials_name", "credential_type",
        "date_created", "date_updated"
    ]
    search_fields = filter_fields
    # Please correct the errors and try again.Role not found or access denied
    message = _("'{}', Role not found or access denied")

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return serializers.AmazonCredentialRoleAdminSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        from organization.utils import current_org
        if current_org.can_admin_by(self.request.user):
            queryset = models.AmazonCredentialRole.objects.all()
        else:
            queryset = self.request.user.user_credential_role.all()
        return queryset

    def perform_create(self, serializer):
        action = serializer.save()
        self.validate_assume_role()
        action.user = self.request.user
        action.credential_type = 'Amazon IAM Role'
        action.created_by = self.request.user.username
        if utils.credentials_amount(self.request.user):
            raise ValidationError({"code": 400, "msg": "您的凭证已经达到最大限制！"})
        try:
            action.save()
        except IntegrityError as e:
            raise ValidationError({"code": 400, "msg": "具有相同的凭证已存在，无法再次增加！", "data": [e]})

    def validate_assume_role(self):
        is_local_role = self.request.data.get('is_local_role')
        account_type = self.request.data.get('account_type')
        role_arn = self.request.data.get('role_arn')
        external_id = self.request.data.get('external_id')
        role_session_name = settings.ROLE_SESSION_NAME
        # 本地角色认证
        if is_local_role:
            self.is_local_role(role_arn, role_session_name, external_id)

        # 为提供将根据配置文件的凭证
        else:
            if account_type == 'amazon-china':
                region_name = True
                aws_access_key_id = settings.CHINA_AWS_ACCESS_KEY_ID
                aws_secret_access_key = settings.CHINA_AWS_SECRET_ACCESS_KEY
            else:
                region_name = False
                aws_access_key_id = settings.GLOBAL_AWS_ACCESS_KEY_ID
                aws_secret_access_key = settings.GLOBAL_AWS_SECRET_ACCESS_KEY
            try:
                sts_client = AwsHelper.boto3_designation_credentials(
                    'sts', aws_access_key_id, aws_secret_access_key, region_name
                )
                credentials = AwsHelper.boto3_assume_role(sts_client, role_arn, external_id, role_session_name)
                if credentials['ResponseMetadata']['HTTPStatusCode'] != 200:
                    raise ValidationError(
                        {
                            "code": 400,
                            "msg": self.message.format(role_arn)
                        }
                    )

            except ClientError as e:
                logger.error(e)
                raise ValidationError(
                    {
                        "code": 400,
                        "msg": self.message.format(role_arn)
                    }
                )
            except Exception as e:
                raise ValidationError({'code': 400, 'msg': e})

    def is_local_role(self, role_arn, role_session_name, external_id):
        try:
            credentials = AwsHelper.boto3_sts(
                arn=role_arn, role_session_name=role_session_name, external_id=external_id
            )
            logger.debug(credentials['AssumedRoleUser'])
            logger.debug(credentials['ResponseMetadata'])
            return Response('ok')

        except ClientError as e:
            logger.error(e)
            raise ValidationError(
                {
                    "code": 400,
                    "msg": self.message.format(role_arn)
                }
            )
        except Exception as e:
            raise ValidationError({'code': 400, 'msg': e})
