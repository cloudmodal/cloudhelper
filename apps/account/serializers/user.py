#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: user.py
@ide: PyCharm
@time: 2019/12/20 12:07
@desc:
"""
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from common.utils import validate_ssh_public_key, validate_phone_number
from common.mixins import BulkSerializerMixin
from common.serializers import AdaptedBulkListSerializer
from common.permissions import CanUpdateDeleteUser
from ..models import User, UserGroup


__all__ = [
    'UserSerializer', 'UserPKUpdateSerializer', 'UserUpdateGroupSerializer',
    'ChangeUserPasswordSerializer', 'ResetOTPSerializer',
    'UserProfileSerializer', 'UserDisplaySerializer',
    'MobileResetPasswordSerializer', 'EmailResetPasswordSerializer',
    'UserResetPasswordSerializer', 'UserOtpEnableAuthenticationSerializer',
    'UserCheckOtpCodeSerializer', 'VerifyCodeSerializer', 'ChangeAccountPhone',
    'OtpVerifySerializer', 'RegisterAccountSerializer'
]


class UserSerializer(BulkSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = User
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'account_id', 'name', 'username', 'password',
            'email', 'public_key', 'groups', 'role', 'wechat',
            'phone', 'mfa_level', 'comment', 'source',
            'is_valid', 'is_expired', 'is_active',
            'created_by', 'is_first_login', 'last_login',
            'date_joined', 'date_expired',
            'date_password_last_updated', 'avatar_url',
        ]
        extra_kwargs = {
            'account_id': {'read_only': True},
            'username': {'required': False},
            'password': {'write_only': True, 'required': False, 'allow_null': True, 'allow_blank': True},
            'public_key': {'write_only': True},
            'is_first_login': {'label': _('Is first login'), 'read_only': True},
            'is_valid': {'label': _('Is valid')},
            'is_expired': {'label': _('Is expired')},
            'avatar_url': {'label': _('Avatar url')},
            'date_joined': {'read_only': True},
            'created_by': {'read_only': True, 'allow_blank': True},
        }

    @staticmethod
    def validate_phone(phone):
        if not validate_phone_number(phone):
            msg = _("the phone '{}' is incorrect".format(phone))
            raise serializers.ValidationError(msg)
        return phone

    def validate_role(self, value):
        request = self.context.get('request')
        if not request.user.is_superuser and value != User.ROLE_USER:
            role_display = dict(User.ROLE_CHOICES)[User.ROLE_USER]
            msg = _("Role limit to {}".format(role_display))
            raise serializers.ValidationError(msg)
        return value

    def validate_password(self, password):
        from ..utils import check_password_rules
        password_strategy = self.initial_data.get('password_strategy')
        if password_strategy == '0':
            return
        if password_strategy is None and not password:
            return
        if not check_password_rules(password):
            msg = _('Password does not match security rules')
            raise serializers.ValidationError(msg)
        return password

    def validate_groups(self, groups):
        role = self.initial_data.get('role')
        if self.instance:
            role = role or self.instance.role
        if role == User.ROLE_AUDITOR:
            return []
        return groups

    @staticmethod
    def change_password_to_raw(attrs):
        password = attrs.pop('password', None)
        if password:
            attrs['password_raw'] = password
        return attrs

    @staticmethod
    def clean_auth_fields(attrs):
        for field in ('password', 'public_key'):
            value = attrs.get(field)
            if not value:
                attrs.pop(field, None)
        return attrs

    def validate(self, attrs):
        attrs = self.change_password_to_raw(attrs)
        return attrs


class UserDisplaySerializer(UserSerializer):
    can_update = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            'orgs_display', 'groups_display', 'role_display',
            'source_display', 'can_update', 'can_delete'
        ]

    def get_can_update(self, obj):
        return CanUpdateDeleteUser.has_update_object_permission(
            self.context['request'], self.context['view'], obj
        )

    def get_can_delete(self, obj):
        return CanUpdateDeleteUser.has_delete_object_permission(
            self.context['request'], self.context['view'], obj
        )

    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        kwargs.update({
            'can_update': {'read_only': True},
            'can_delete': {'read_only': True},
            'groups_display': {'label': _('Groups name')},
            'source_display': {'label': _('Source name')},
            'role_display': {'label': _('Role name')},
            'orgs_display': {'label': _('Organization name')},
        })
        return kwargs


class UserPKUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'public_key']

    @staticmethod
    def validate_public_key(value):
        if not validate_ssh_public_key(value):
            raise serializers.ValidationError(_('Not a valid ssh public key'))
        return value


class UserUpdateGroupSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=UserGroup.objects
    )

    class Meta:
        model = User
        fields = ['id', 'groups']


class ChangeUserPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['password']


class ResetOTPSerializer(serializers.Serializer):
    msg = serializers.CharField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'account_id', 'username', 'name',
            'role', 'role_display', 'email'
        ]


class MobileResetPasswordSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, min_length=11, required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @staticmethod
    def validate_mobile(mobile):
        try:
            User.objects.get(phone=mobile)
        except User.DoesNotExist as e:
            raise serializers.ValidationError(f"{e}")

        if not validate_phone_number(mobile):
            msg = _("the phone '{}' is incorrect".format(mobile))
            raise serializers.ValidationError(msg)
        return mobile


class EmailResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @staticmethod
    def validate_email(email):
        try:
            User.objects.get(email=email)
        except User.DoesNotExist as e:
            raise serializers.ValidationError(f"{e}")
        return email


class VerifyCodeSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, min_length=11, required=False)
    email = serializers.EmailField(required=False)
    code = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserResetPasswordSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, min_length=11, required=False)
    email = serializers.CharField(required=False)
    code = serializers.CharField(max_length=6, min_length=6, required=True)
    new_password = serializers.CharField(min_length=6, max_length=128, required=True)
    confirm_password = serializers.CharField(min_length=6, max_length=128, required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserOtpEnableAuthenticationSerializer(serializers.Serializer):
    password = serializers.CharField(
        label=_('密码'), write_only=True, max_length=128, required=True
    )
    mobile = serializers.CharField(max_length=11, min_length=11, required=False)
    email = serializers.CharField(required=False)
    code = serializers.CharField(max_length=6, min_length=6, required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserCheckOtpCodeSerializer(serializers.Serializer):
    otp_code = serializers.CharField(label=_('MFA code'), max_length=6)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ChangeAccountPhone(serializers.Serializer):
    phone = serializers.CharField(
        label=_('Phone'), required=True,
        max_length=11, min_length=11
    )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class OtpVerifySerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6, min_length=6)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RegisterAccountSerializer(serializers.Serializer):
    company = serializers.CharField(
        label=_('Company'), required=True,
        max_length=128, min_length=1
    )
    name = serializers.CharField(
        label=_('Name'), required=False,
    )
    phone = serializers.CharField(
        label=_('Phone'), required=False,
        max_length=11, min_length=11
    )
    email = serializers.EmailField(label=_('Email'), required=False)
    password = serializers.CharField(
        label=_('Password'), write_only=True, max_length=128, required=True
    )
    terms_of_service = serializers.BooleanField(label=_('Terms of Service'), required=True)
    privacy_policy = serializers.BooleanField(label=_('Privacy Policy'), required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @staticmethod
    def validate_email(email):
        if User.objects.filter(email=email):
            raise serializers.ValidationError("Email address already exists")
        return email

    @staticmethod
    def validate_phone(phone):
        if User.objects.filter(phone=phone):
            raise serializers.ValidationError("Phone number already exists")
        return phone

    @staticmethod
    def validate_company(company):
        from organization.models import Organization
        if Organization.objects.filter(name=company):
            raise serializers.ValidationError("Company name is illegal")
        return company
