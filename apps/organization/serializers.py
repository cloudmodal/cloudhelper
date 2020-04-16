#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: serializers.py
@ide: PyCharm
@time: 2020/1/2 18:46
@desc:
"""
import re
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from account.models import UserGroup
from common.serializers import AdaptedBulkListSerializer
from .utils import set_current_org, get_current_org
from .models import Organization
from common.const import GENERAL_FORBIDDEN_SPECIAL_CHARACTERS_PATTERN, \
    GENERAL_FORBIDDEN_SPECIAL_CHARACTERS_ERROR_MSG
from .mixins.serializers import OrgMembershipSerializerMixin


class OrgSerializer(ModelSerializer):
    class Meta:
        model = Organization
        list_serializer_class = AdaptedBulkListSerializer
        fields = '__all__'
        read_only_fields = ['created_by', 'date_created']

    @staticmethod
    def validate_name(name):
        pattern = GENERAL_FORBIDDEN_SPECIAL_CHARACTERS_PATTERN
        res = re.search(pattern, name)
        if res is not None:
            msg = GENERAL_FORBIDDEN_SPECIAL_CHARACTERS_ERROR_MSG
            raise serializers.ValidationError(msg)
        return name


class OrgReadSerializer(ModelSerializer):
    admins = serializers.SerializerMethodField(read_only=True)
    auditors = serializers.SerializerMethodField(read_only=True)
    users = serializers.SerializerMethodField(read_only=True)
    user_groups = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = '__all__'

    @staticmethod
    def get_data_from_model(obj, model):
        current_org = get_current_org()
        set_current_org(Organization.root())
        data = [o.name for o in model.objects.filter(org_id=obj.id)]
        set_current_org(current_org)
        return data

    def get_user_groups(self, obj):
        return self.get_data_from_model(obj, UserGroup)

    @staticmethod
    def get_admins(obj):
        return [{"id": admins.id, "username": admins.username} for admins in obj.admins.all()]

    @staticmethod
    def get_auditors(obj):
        return [{"id": auditors.id, "username": auditors.username} for auditors in obj.auditors.all()]

    @staticmethod
    def get_users(obj):
        return [{"id": users.id, "username": users.username} for users in obj.users.all()]


class OrgMembershipAdminSerializer(OrgMembershipSerializerMixin, ModelSerializer):
    class Meta:
        model = Organization.admins.through
        list_serializer_class = AdaptedBulkListSerializer
        fields = '__all__'


class OrgMembershipUserSerializer(OrgMembershipSerializerMixin, ModelSerializer):
    class Meta:
        model = Organization.users.through
        list_serializer_class = AdaptedBulkListSerializer
        fields = '__all__'


class OrganizationProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = [
            'id', 'name'
        ]
