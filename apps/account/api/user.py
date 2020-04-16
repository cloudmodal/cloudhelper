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
from django.core.cache import cache
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_bulk import BulkModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from common.aliyunsm import SMSCaptcha
from common.permissions import (
    IsOrgAdmin, IsCurrentUserOrReadOnly, IsOrgAdminOrAppUser,
    CanUpdateDeleteUser, IsSuperUser, IsValidUser
)
from common.send_email import send_user_code_mail
from common.utils import create_captcha
from common.mixins import CommonApiMixin
from common.utils import get_logger
from organization.utils import current_org
from .. import serializers, utils
from ..models import User
from .. import signals
from .. import errors


logger = get_logger(__name__)

__all__ = [
    'UserViewSet', 'AdminChangeUserPasswordApi', 'UserUpdateGroupApi',
    'UserResetPasswordApi', 'UserResetPKApi', 'UserUpdatePKApi',
    'UserUnblockPKApi', 'UserProfileApi', 'UserResetOTPApi',
    'RetrievePasswordSendSMSApi', 'RetrievePasswordSendSESApi',
    'UserOtpEnableAuthenticationApi', 'UserOtpEnableBindApi',
    'SecuritySettingsCheckApi', 'VerifyCodeApi', 'UserDisableMFAAPI',
    'RegisterAccountAPI', 'ConfirmVerificationApi'
]


class UserQuerysetMixin:
    def get_queryset(self):
        queryset = utils.get_current_org_members()
        return queryset


class UserViewSet(CommonApiMixin, UserQuerysetMixin, BulkModelViewSet):
    """用户详细视图"""
    filter_fields = ('username', 'email', 'name', 'id')
    search_fields = filter_fields
    serializer_classes = {
        'default': serializers.UserSerializer,
        'display': serializers.UserDisplaySerializer
    }
    permission_classes = (IsOrgAdmin, CanUpdateDeleteUser)

    def get_queryset(self):
        return super().get_queryset().prefetch_related('groups')

    def send_created_signal(self, users):
        if not isinstance(users, list):
            users = [users]
        for user in users:
            signals.post_user_create.send(self.__class__, user=user)

    def perform_create(self, serializer):
        # 重写save的逻辑, username 用email
        users = serializer.save()
        users.username = serializer.data['email']
        users.save()
        if isinstance(users, User):
            users = [users]
        if current_org and current_org.is_real():
            current_org.users.add(*users)

        self.send_created_signal(users)

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            self.permission_classes = (IsOrgAdminOrAppUser,)
        if self.request.query_params.get('all'):
            self.permission_classes = (IsSuperUser,)
        return super().get_permissions()

    def perform_destroy(self, instance):
        if current_org.is_real():
            instance.delete()
        else:
            return super().perform_destroy(instance)

    def perform_bulk_destroy(self, objects):
        for obj in objects:
            self.check_object_permissions(self.request, obj)
            self.perform_destroy(obj)

    def perform_bulk_update(self, serializer):
        # TODO: 批量更新，需要测试
        users_ids = [
            d.get("id") or d.get("pk") for d in serializer.validated_data
        ]
        users = current_org.get_org_members().filter(id__in=users_ids)
        for user in users:
            self.check_object_permissions(self.request, user)
        return super().perform_bulk_update(serializer)


class AdminChangeUserPasswordApi(UserQuerysetMixin, generics.RetrieveUpdateAPIView):
    """管理员更改用户密码"""
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.ChangeUserPasswordSerializer

    def perform_update(self, serializer):
        user = self.get_object()
        user.password_raw = serializer.validated_data["password"]
        user.save()


class UserUpdateGroupApi(UserQuerysetMixin, generics.RetrieveUpdateAPIView):
    """用户更改组"""
    serializer_class = serializers.UserUpdateGroupSerializer
    permission_classes = (IsOrgAdmin,)


class UserUpdatePhoneApi(generics.CreateAPIView):
    pass


class ConfirmVerificationApi(APIView):
    """用户激活验证Token"""
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)
    success_message = {
        "code": 200,
        "error_code": 20016,
        "msg": "账户已激活"
    }

    def get(self, request, token):
        user = User.validate_reset_password_token(token)
        if user:
            users = User.objects.filter(id=user.id)
            users.update(is_active=True)
            User.expired_reset_password_token(token)

        else:
            msg = {
                "code": 400,
                "error_code": 40046,
                "error": "Token invalid or expired",
                "msg": "链接失效"
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.success_message, status=status.HTTP_200_OK)


class UserResetPasswordApi(generics.CreateAPIView):
    """用户重置密码"""
    serializer_class = serializers.UserResetPasswordSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def change_password(user, password):
        from common.send_email import send_reset_password_mail
        user.password_raw = password
        user.save()
        send_reset_password_mail(user)

    def perform_create(self, serializer):
        email = serializer.validated_data.get('email')
        mobile = serializer.validated_data.get('mobile')
        code = serializer.validated_data.get('code')
        confirm_password = serializer.validated_data.get('confirm_password')
        if email and mobile:
            return Response({"code": 400, "msg": "手机号码或Email只能输入一个☝哦️"}, status=status.HTTP_400_BAD_REQUEST)
        if email:
            user = User.objects.get(email=email)
            if code is None:
                raise ValidationError({"code": 400, "msg": "验证码不能为空"})
            else:
                if code != cache.get('reset_password_' + email):
                    raise ValidationError({"code": 400, "msg": "验证码错误"})
                else:
                    return self.change_password(user, confirm_password)

        if mobile:
            user = User.objects.get(phone=mobile)
            if code is None:
                raise ValidationError({"code": 400, "msg": "验证码不能为空"})
            else:
                if code != cache.get('reset_password_' + mobile, None):
                    raise ValidationError({"code": 400, "msg": "验证码错误"})
                else:
                    return self.change_password(user, confirm_password)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'code': 200, 'msg': 'ok'}, status=status.HTTP_200_OK)


class UserResetPKApi(UserQuerysetMixin, generics.UpdateAPIView):
    """用户重置公钥"""
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        # from ..utils import send_reset_ssh_key_mail
        user = self.get_object()
        user.public_key = None
        user.save()
        # send_reset_ssh_key_mail(user)


# 废弃
class UserUpdatePKApi(UserQuerysetMixin, generics.UpdateAPIView):
    """用户更新公钥"""
    serializer_class = serializers.UserPKUpdateSerializer
    permission_classes = (IsCurrentUserOrReadOnly,)

    def perform_update(self, serializer):
        user = self.get_object()
        user.public_key = serializer.validated_data['public_key']
        user.save()


class UserUnblockPKApi(UserQuerysetMixin, generics.UpdateAPIView):
    """禁用用户"""
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.UserSerializer
    key_prefix_limit = "_LOGIN_LIMIT_{}_{}"
    key_prefix_block = "_LOGIN_BLOCK_{}"

    def perform_update(self, serializer):
        user = self.get_object()
        username = user.username if user else ''
        key_limit = self.key_prefix_limit.format(username, '*')
        key_block = self.key_prefix_block.format(username)
        cache.delete_pattern(key_limit)
        cache.delete(key_block)


class UserProfileApi(generics.RetrieveAPIView):
    """用户个人信息"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserDisplaySerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        age = request.session.get_expiry_age()
        request.session.set_expiry(age)
        return super().retrieve(request, *args, **kwargs)


class SecuritySettingsCheckApi(APIView):
    """个人中心安全设置检查"""
    permission_classes = (IsAuthenticated,)
    # serializer_class = serializers.SecuritySettingsCheck
    mobile = None
    security_level = 0
    password = False
    mfa_level = False

    def get(self, request):
        if request.user.password:
            self.password = True

        if request.user.mfa_level != 0:
            self.mfa_level = True

        if request.user.password:
            self.security_level = self.security_level + 1
        if request.user.phone:
            self.security_level = self.security_level + 1
        if request.user.mfa_level != 0:
            self.security_level = self.security_level + 1
        phone = request.user.phone
        if phone:
            self.mobile = phone[0:2] + '*******' + phone[-2:]
        data = {
            "code": 200,
            "data": {
                'account_id': request.user.account_id,
                'username': request.user.email,
                'date_joined': request.user.date_joined,
                'name': request.user.name,
                'password': self.password,
                'phone': self.mobile,
                'mfa_level': self.mfa_level,
                'security_level': self.security_level
            },
            "msg": "个人中心安全设置检查"
        }
        return Response(data, status=status.HTTP_200_OK)


class UserOtpEnableAuthenticationApi(generics.CreateAPIView):
    """用户MFA启用身份验证Api"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserOtpEnableAuthenticationSerializer

    def perform_create(self, serializer):
        user = utils.get_user_or_tmp_user(self.request)
        password = serializer.validated_data["password"]
        user = authenticate(username=user.username, password=password)
        if not user:
            raise errors.AuthenticationFailed(
                {'detail': '身份认证失败，提供的凭证无效！', 'code': 'authentication_failed'}
            )

        if user.mfa_is_otp():
            raise errors.MovedPermanently(
                {'detail': '您已启用MFA请进行下一步操作！', 'code': 'moved_permanently'}
            )
        else:
            user.enable_mfa()
            user.save()
            # return redirect('users:user-otp-settings-success')

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'msg': 'ok'})


class UserOtpEnableBindApi(APIView):
    """用户启用MFA进行绑定"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserCheckOtpCodeSerializer
    error_data = {}

    def get(self, request):
        user = utils.get_user_or_tmp_user(self.request)
        try:
            otp_uri, otp_secret_key = utils.generate_otp_uri(self.request)
            data = {
                "code": 200,
                "data": {
                    'otp_uri': otp_uri,
                    'otp_secret_key': otp_secret_key,
                    'user': user.username
                },
                "msg": "生成二维码"
            }
            return Response(data, status=status.HTTP_200_OK)
        except TypeError:
            return Response(
                {
                    "code": status.HTTP_406_NOT_ACCEPTABLE,
                    "msg": "Cookies error"
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

    def post(self, request):
        otp_code = request.data.get('otp_code')
        try:
            otp_secret_key = cache.get(self.request.session.session_key + 'otp_key', '')
            if utils.check_otp_code(otp_secret_key, otp_code):
                self.save_otp(otp_secret_key)
                return Response({
                    'code': 200,
                    'data': {},
                    'msg': '提示信息'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "code": 400,
                    "error_code": 40011,
                    "error": "Invalid OTP key",
                    "msg": "MFA验证码不正确，或者服务器端时间不对!"

                }, status=status.HTTP_400_BAD_REQUEST)
        except TypeError:
            return Response(
                {
                    "code": status.HTTP_406_NOT_ACCEPTABLE,
                    "msg": "Cookies error"
                }, status=status.HTTP_406_NOT_ACCEPTABLE
            )

    def save_otp(self, otp_secret_key):
        user = utils.get_user_or_tmp_user(self.request)
        user.enable_mfa()
        user.otp_secret_key = otp_secret_key
        user.save()


class UserResetOTPApi(UserQuerysetMixin, generics.RetrieveAPIView):
    """用户重置MFA"""
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.ResetOTPSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object() if kwargs.get('pk') else request.user
        if user == request.user:
            msg = _("Could not reset self otp, use profile reset instead")
            return Response({"error": msg}, status=401)
        if user.mfa_enabled:
            user.reset_mfa()
            user.save()
            logout(request)
        return Response({"msg": "success"})


class RetrievePasswordSendSMSApi(generics.CreateAPIView):
    """发送验证码到手机"""
    throttle_scope = 'send_sms'
    permission_classes = (AllowAny,)
    serializer_class = serializers.MobileResetPasswordSerializer

    def perform_create(self, serializer):
        mobile = serializer.validated_data.get('mobile')
        if mobile:
            # 阿里云短信模版
            sms = SMSCaptcha(template_code='SMS_182546328')
            cache.set('reset_password_' + mobile, create_captcha(6), timeout=60 * 10)
            cache_captcha = cache.get('reset_password_' + mobile, None)
            if cache_captcha:
                # 发送验证码
                sms.send_sms(mobile, cache_captcha)
                logger.debug(f'手机{mobile}的验证码: {cache_captcha}')
            else:
                logger.debug(f'手机{mobile}的验证码: {cache_captcha}')
        else:
            raise ValidationError({"error": "手机号码不能为空！"})

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'code': 200, 'msg': 'ok'}, status=status.HTTP_200_OK)


class RetrievePasswordSendSESApi(generics.CreateAPIView):
    """发送验证码到邮箱"""
    throttle_scope = 'send_ses'
    permission_classes = (AllowAny,)
    serializer_class = serializers.EmailResetPasswordSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data.get('email')
        if email:
            captcha = create_captcha(6)
            cache.set('reset_password_' + email, captcha, timeout=60 * 10)
            cache_captcha = cache.get('reset_password_' + email, None)
            if cache_captcha:

                send_user_code_mail(email, cache_captcha)
                logger.debug(f"Email'{email}'的验证码: {cache_captcha}")
            else:
                logger.debug(f"Email'{email}'的验证码: {cache_captcha}")
        else:
            logger.error("Email为空")

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'code': 200, 'msg': 'ok'}, status=status.HTTP_200_OK)


class VerifyCodeApi(generics.CreateAPIView):
    """验证发送的验证码是否正确"""
    permission_classes = (AllowAny,)
    serializer_class = serializers.VerifyCodeSerializer

    def perform_create(self, serializer):
        code = serializer.validated_data.get('code')
        email = serializer.validated_data.get('email')
        mobile = serializer.validated_data.get('mobile')

        if email and mobile:
            raise errors.NotAcceptable({"detail": "手机号与邮箱只能选择一种"})

        if email:
            cache_email_captcha = cache.get('reset_password_' + email, None)
            if cache_email_captcha == code:
                return Response('验证成功', status.HTTP_200_OK)
            else:
                raise ValidationError({"detail": "验证失败，验证码不正确或者已过期"})
        elif mobile:
            cache_mobile_captcha = cache.get('reset_password_' + mobile, None)
            if cache_mobile_captcha == code:
                return Response('验证成功', status.HTTP_200_OK)
            else:
                raise ValidationError({"detail": "验证失败，验证码不正确或者已过期"})
        else:
            raise ValidationError({"detail": "字段不能为空"})

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'code': 200, 'msg': 'ok'}, status=status.HTTP_200_OK)


class UserDisableMFAAPI(generics.CreateAPIView):
    permission_classes = (IsValidUser,)
    serializer_class = serializers.OtpVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["otp_code"]

        user = self.request.user
        if user.mfa_level == 0:
            return Response({"msg": _("Account is not bound to MFA, no need to unbind")}, status=202)

        elif user.mfa_level == 1:
            if user.check_mfa(code):
                user.disable_mfa()
                user.save()
                return Response({"msg": _("Unbinding successfully, please log in again!")})
            else:
                return Response({"error": "Code not valid"}, status=400)

        elif user.mfa_level == 2:
            msg = _(
                "Unable to unbind, the account has been forcibly enabled by an administrator, "
                "please contact your administrator"
            )
            return Response(
                {"msg": msg}, status=202
            )


class RegisterAccountAPI(generics.CreateAPIView):
    """注册用户"""
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterAccountSerializer

    def perform_create(self, serializer):
        company = serializer.validated_data.get('company')
        name = serializer.validated_data.get('name')
        phone = serializer.validated_data.get('phone')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        terms_of_service = serializer.validated_data.get('terms_of_service')
        privacy_policy = serializer.validated_data.get('privacy_policy')
        if terms_of_service and privacy_policy:
            user = User.users.create_org_user(
                company=company, name=name, email=email,
                phone=phone, password=password
            )
            signals.post_user_registered.send(self.__class__, user=user)
        else:
            raise ValidationError({"code": 400, "msg": "请阅读并同意'服务条款' 和 '隐私条款'"})

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'code': 200, 'msg': 'ok'}, status=status.HTTP_200_OK)
