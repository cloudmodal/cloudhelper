#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: credentials.py
@ide: PyCharm
@time: 2020/2/12 14:55
@desc:
"""
import re
from rest_framework import serializers
from common.serializers import AdaptedBulkListSerializer
from organization.mixins.serializers import BulkOrgResourceModelSerializer
from .. import models


__all__ = [
    "CredentialSerializer",
    "AmazonCredentialSerializer", "AmazonCredentialRoleSerializer",
    "AmazonCredentialRoleAdminSerializer", "AmazonCredentialAdminSerializer"
]


class CredentialSerializer(BulkOrgResourceModelSerializer):
    class Meta:
        model = models.StatisticsCredential
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            "id", "name", "credential", "credentials_name",
            "account_type", "credential_type", "date_created",
            "date_updated", "created_by"
        ]
        extra_kwargs = {
            "account_type": {'required': True, 'allow_null': False, 'allow_blank': False},
            "credential_type": {'read_only': True, 'allow_blank': True},
            "date_created": {'read_only': True},
            "date_updated": {'read_only': True},
            "created_by": {'read_only': True, 'allow_blank': True, 'allow_null': True},
        }


class AmazonCredentialSerializer(BulkOrgResourceModelSerializer):

    class Meta:
        model = models.AccessKeys
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            "id", "credentials_name",  "account_type",
            "access_key_id", "secret_access_key", "credential_type",
            "date_created", "date_updated",
            "created_by"
        ]
        extra_kwargs = {
            "user": {'write_only': True, 'required': False, 'allow_null': True, 'allow_blank': True},
            "account_type": {'required': True, 'allow_null': False, 'allow_blank': False},
            "credential_type": {'read_only': True, 'allow_blank': True},
            "date_created": {'read_only': True},
            "date_updated": {'read_only': True},
            "created_by": {'read_only': True, 'allow_blank': True, 'allow_null': True},
        }

    def validate_access_key_id(self, access_key_id):
        self.initial_data.get('credential_type')
        if len(access_key_id) != 20:
            raise serializers.ValidationError("Access Key IDs must be 20 characters.")
        return access_key_id

    def validate_secret_access_key(self, secret_access_key):
        self.initial_data.get('credential_type')
        if len(secret_access_key) != 40:
            raise serializers.ValidationError({"msg": "Secret Access Keys must be 40 characters"})
        return secret_access_key


class AmazonCredentialAdminSerializer(AmazonCredentialSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta(AmazonCredentialSerializer.Meta):
        fields = AmazonCredentialSerializer.Meta.fields + [
            'user'
        ]

    @staticmethod
    def get_user(obj):
        return [{"id": obj.user.id, "username": obj.user.username, "email": obj.user.email}]


class AmazonCredentialRoleSerializer(BulkOrgResourceModelSerializer):

    class Meta:
        model = models.AmazonCredentialRole
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            "id", "credentials_name",  "account_type",
            "role_arn", "external_id", "require_mfa",
            "credential_type", "date_created",
            "date_updated", "created_by"
        ]
        extra_kwargs = {
            "user": {'write_only': True, 'required': False, 'allow_null': True, 'allow_blank': True},
            "account_type": {'required': True, 'allow_null': False, 'allow_blank': False},
            "credential_type": {'read_only': True, 'allow_blank': True},
            "is_local_role": {'required': False, 'allow_blank': True},
            "date_created": {'read_only': True},
            "date_updated": {'read_only': True},
            "created_by": {'read_only': True, 'allow_blank': True, 'allow_null': True},
        }

    def validate_role_arn(self, role_arn):
        credential_type = self.initial_data.get('credential_type')
        if credential_type == 'amazon-china' or credential_type == 'amazon-standard':
            if not re.match("^(arn:aws|aws-cn):iam::[0-9]{12}:role/[ -~]{1,150}$", role_arn):
                raise serializers.ValidationError("Not a valid role ARN.")
        return role_arn


class AmazonCredentialRoleAdminSerializer(AmazonCredentialRoleSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta(AmazonCredentialRoleSerializer.Meta):
        fields = AmazonCredentialRoleSerializer.Meta.fields + [
            'user'
        ]

    @staticmethod
    def get_user(obj):
        return [{"id": obj.user.id, "username": obj.user.username, "email": obj.user.email}]
