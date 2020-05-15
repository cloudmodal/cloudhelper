#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: aliyunsm.py.py
@ide: PyCharm
@time: 2020/1/6 23:08
@desc:
"""
import uuid
import json
from django.conf import settings
from dysms_python.aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider

from common.utils import get_logger

logger = get_logger(__name__)


class SMSCaptcha(object):
    """
    短信业务调用接口，版本号：v20170525
    Created on 2017-06-12
    """
    def __init__(self, template_code):
        self.ACCESS_KEY_ID = settings.ALI_ACCESS_KEY_ID
        self.ACCESS_KEY_SECRET = settings.ALI_ACCESS_KEY_SECRET
        # 应用名称
        self.sign_name = settings.ALI_SIGN_NAME
        # 模板名称
        self.template_code = template_code
        self.count = 6

    def _init_connection_aliyun(self, PRODUCT_NAME, REGION, DOMAIN):
        acs_client = AcsClient(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET, REGION)
        region_provider.modify_point(PRODUCT_NAME, REGION, DOMAIN)
        return acs_client

    # def create_captcha(self):
    #     """
    #     create and return captcha
    #     :param self:
    #     :return: A six-digit verification code
    #     """
    #     captcha = ''
    #     for i in range(self.count):
    #         now_number = str(random.randint(0, 9))
    #         captcha += now_number
    #     return captcha

    def send_sms(self, phone_numbers, code):
        """
        发送短信接口，在需要使用的地方引用该模块，然后调用该接口即可
        :param phone_numbers:发送的手机号码
        :param code:验证码
        :return:
        """
        # 模板变量参数
        template_param = json.dumps({'code': code})
        business_id = uuid.uuid1()
        sms_response = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        sms_response.set_TemplateCode(self.template_code)
        # 短信模板变量参数
        if template_param is not None:
            sms_response.set_TemplateParam(template_param)
        # 设置业务请求流水号，必填。
        sms_response.set_OutId(business_id)
        # 短信签名
        sms_response.set_SignName(self.sign_name)
        # 数据提交方式
        # smsRequest.set_method(MT.POST)
        # 数据提交格式
        # smsRequest.set_accept_format(FT.JSON)
        # 短信发送的号码列表，必填。
        sms_response.set_PhoneNumbers(phone_numbers)
        # 调用短信发送接口，返回json
        # 注意：如非特使情况请不要更改此参数
        sm = self._init_connection_aliyun(
            PRODUCT_NAME=settings.ALI_PRODUCT_NAME, REGION=settings.ALI_REGION, DOMAIN=settings.ALI_DOMAIN
        )
        sms_response = sm.do_action_with_exception(sms_response)
        response = eval(str(sms_response, encoding="utf-8"))
        if response['Code'] != 'OK':
            logger.error(f'发送短信验证码错误，{response["Message"]},错误代码：{response["Code"]}')
        return sms_response
