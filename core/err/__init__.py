#!/usr/bin/env python
# encoding:utf-8

from flask import jsonify


class Response(object):
    @staticmethod
    def re(err=None, data=None):
        if err is None:
            err = ErrSuccess

        if data is None:
            return jsonify(code=err.errcode, msg=err.errmsg)
        else:
            return jsonify(code=err.errcode, msg=err.errmsg, data=data)


class ErrSuccess(object):
    errcode = 0
    errmsg = 'Success'


class Err(object):
    errcode = 9001
    errmsg = '未知错误'


class ErrToken(object):
    errcode = 9002
    errmsg = 'TOKEN 失效'


class Err403(object):
    errcode = 9003
    errmsg = '权限不存在'


class ErrUserNot(object):
    errcode = 9004
    errmsg = '账号不存在'


class ErrUserPassword(object):
    errcode = 9005
    errmsg = '密码不正确'


class ErrUser(object):
    errcode = 9006
    errmsg = '账号已经存在'


class ErrType(object):
    errcode = 9007
    errmsg = '分类已经存在'


class ErrTypeUse(object):
    errcode = 9008
    errmsg = '分类正在使用'


class ErrVariablenUse(object):
    errcode = 9009
    errmsg = '变量已经存在'


class ErrUserDel(object):
    errcode = 9090
    errmsg = '不能删除本人账号'


class ErrUserSwitch(object):
    errcode = 9011
    errmsg = '不能禁用本人账号'


class ErrUserLoginSwitch(object):
    errcode = 9012
    errmsg = '该账户已经被禁用'


class ErrAppNullUpdate(object):
    errcode = 9013
    errmsg = 'APP 目前无更新'


class ErrWebhookText(object):
    errcode = 9014
    errmsg = 'WebHook 内容不能为空'


class ErrWebhookUUID(object):
    errcode = 9015
    errmsg = 'WebHook UUID 不能为空'


class ErrWebhookUUIDNot(object):
    errcode = 9016
    errmsg = 'WebHook UUID 不正确'


class ErrWebhookkey(object):
    errcode = 9017
    errmsg = 'API kEY 不能为空'


class ErrWebhookKeyNot(object):
    errcode = 9018
    errmsg = 'API KEY 不正确'


class ErrWebhookStatus(object):
    errcode = 9020
    errmsg = '工作流状态不可用'


class ErrAppDel(object):
    errcode = 9021
    errmsg = '删除 APP 失败'


class ErrImportUrl(object):
    errcode = 9022
    errmsg = '请求失败 或 URL不正确'


class ErrIsNotPlayBook(object):
    errcode = 9023
    errmsg = '剧本不存在'


class ErrUploadZip(object):
    errcode = 9024
    errmsg = '上传文件非 ZIP 压缩文件'


class ErrUploadZipR(object):
    errcode = 9025
    errmsg = 'APP 格式不正确 或 压缩文件损坏'


class ErrUploadAppExist(object):
    errcode = 9026
    errmsg = 'APP 已经存在'
