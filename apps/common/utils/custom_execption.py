#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: custom_execption.py
@ide: PyCharm
@time: 2019/12/30 21:09
@desc:
"""
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        error = response.data.get('code')
        # response.data.clear()
        response.data['code'] = response.status_code
        if error:
            response.data['error'] = error
        else:
            response.data['error'] = response.status_text
        response.data['data'] = []
        try:
            response.data['msg'] = response.data.pop('detail')
        except KeyError:
            pass

        if response.status_code == 400:
            if response.data.get('msg') is None:
                response.data['msg'] = "输入错误"

        elif response.status_code == 401:
            if response.data.get('msg') is None:
                response.data['msg'] = "验证失败"

        # elif response.status_code == 403:
        #     print(response.data.pop('detail'))
        #     # response.data['msg'] = "访问被拒绝"

        elif response.status_code == 404:
            try:
                response.data['msg'] = response.data.pop('detail')
                response.data['msg'] = "未找到"
            except KeyError:
                response.data['msg'] = "未找到"

        elif response.status_code == 405:
            response.data['msg'] = '请求的方法不正确'

        elif response.status_code >= 500:
            response.data['msg'] = "内部服务错误"

    return response
