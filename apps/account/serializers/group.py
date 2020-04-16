#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: group.py
@ide: PyCharm
@time: 2019/12/20 11:18
@desc:
"""
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from common.fields import StringManyToManyField
from common.serializers import AdaptedBulkListSerializer
from organization.mixins.serializers import BulkOrgResourceModelSerializer
from ..models import User, UserGroup
from .. import utils

__all__ = [
    'UserGroupSerializer', 'UserGroupDisplaySerializer',
    'UserGroupListSerializer', 'UserGroupUpdateMemberSerializer',
]


class UserGroupSerializer(BulkOrgResourceModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        required=False, many=True, queryset=User.objects, label=_('User')
    )
    users_info = serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = UserGroup
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name',  'users', 'comment', 'date_created',
            'created_by', 'users_info'
        ]
        extra_kwargs = {
            'created_by': {'label': _('Created by'), 'read_only': True}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_fields_queryset()

    @staticmethod
    def get_users_info(obj):
        return [{"id": users.id, "username": users.username, "email": users.email} for users in obj.users.all()]

    def set_fields_queryset(self):
        users_field = self.fields['users']
        users_field.child_relation.queryset = utils.get_current_org_members()

    def validate_users(self, users):
        for user in users:
            if user.is_super_auditor:
                msg = _('Auditors cannot be join in the user group')
                raise serializers.ValidationError(msg)
        return users


class UserGroupListSerializer(UserGroupSerializer):
    users = StringManyToManyField(many=True, read_only=True)


class UserGroupDisplaySerializer(UserGroupSerializer):

    class Meta(UserGroupSerializer.Meta):
        fields = UserGroupSerializer.Meta.fields + [
            'users_display'
        ]

    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        kwargs.update({
            'users_display': {'label': _('Users name')},
        })
        return kwargs


class UserGroupUpdateMemberSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects)

    class Meta:
        model = UserGroup
        fields = ['id', 'users']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_fields_queryset()

    def set_fields_queryset(self):
        users_field = self.fields['users']
        users_field.child_relation.queryset = utils.get_current_org_members()
