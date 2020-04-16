#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: serializers.py
@ide: PyCharm
@time: 2019/12/20 12:10
@desc:
"""
import re
from rest_framework import serializers
from common.utils import get_object_or_none
from account.models import User
from account.serializers import UserProfileSerializer
from .models import AccessKey, LoginConfirmSetting
from organization.serializers import OrganizationProfileSerializer


__all__ = [
    'AccessKeySerializer', 'OtpVerifySerializer', 'BearerTokenSerializer',
    'MFAChallengeSerializer', 'LoginConfirmSettingSerializer',
]


class AccessKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessKey
        fields = [
            'id', 'access_key_id', 'is_active', 'date_created'
        ]
        extra_kwargs = {
            'access_key_id': {'read_only': True},
            'date_created': {'read_only': True},
        }


class OtpVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class BearerTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        allow_null=True, required=False, write_only=True
    )
    password = serializers.CharField(
        write_only=True, allow_null=True, required=False, allow_blank=True
    )
    public_key = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )
    mobile = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )
    code = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )
    SessionToken = serializers.CharField(read_only=True)
    keyword = serializers.SerializerMethodField()
    Expiration = serializers.DateTimeField(read_only=True)
    Organization = OrganizationProfileSerializer(read_only=True, many=True)
    user = UserProfileSerializer(read_only=True)

    @staticmethod
    def get_keyword(obj):
        return 'Bearer'

    def create(self, validated_data):
        request = self.context.get('request')
        if request.user and not request.user.is_anonymous:
            user = request.user
        else:
            user_id = request.session.get('user_id')
            user = get_object_or_none(User, pk=user_id)
            if not user:
                raise serializers.ValidationError(
                    {
                        "status": 400,
                        "error_code": 40000,
                        "error": "Invalid API key",
                        "msg": f"用户ID：'{user_id}'不存在"
                    }
                )
        token, date_expired = user.create_bearer_token(request)
        organization = user.user_or_admin_audit_orgs
        instance = {
            "SessionToken": token,
            "Expiration": date_expired,
            "Organization": organization,
            "user": user,
        }
        return instance

    def update(self, instance, validated_data):
        pass


class MFAChallengeSerializer(serializers.Serializer):
    type = serializers.CharField(write_only=True, required=False, allow_blank=True)
    code = serializers.CharField(write_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class LoginConfirmSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginConfirmSetting
        fields = ['id', 'user', 'reviewers', 'date_created', 'date_updated']
        read_only_fields = ['date_created', 'date_updated']


class SMSSerializer(serializers.Serializer):
    mobile = serializers.CharField(write_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @staticmethod
    def validate_mobile(mobile):
        """验证手机号码"""

        # 验证手机号码是否合法
        if not re.match("^(13[0-9]|14[5|7]|15[0-9]|166|17[367]|18[0-9])[0-9]{8}$", mobile):
            raise serializers.ValidationError("手机号码非法")
