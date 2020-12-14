from werkzeug.exceptions import HTTPException
from app.libs.error import APIException

#注册成功
class Success(APIException):
    code=201
    msg='ok，注册成功'
    error_code=0

#客户端类型错误
class ClientTypeError(APIException):
    #401未授权 403禁止访问 404没有找到资源
    #500服务器产生一个未知的错误
    #200查询成功 201创建、更新成功 204删除成功
    #301 302重定向
    code=400#请求参数错误
    msg="client is invalid"
    error_code = 1006

#公共参数异常
class ParameterException(APIException):
    code=400
    msg='invalid parameter'
    error_code=1000

#服务器未知 错误
class ServerError(APIException):
    code = 500  # 错误状态码500服务器产生一个未知的错误
    msg = 'sorry,we have a mistake 😆'
    error_code = 999  # 错误代码，未知错误

#没找到账号
class NotFound(APIException):
    code = 404  # 404没有找到资源
    msg = '对不起，资源没有找到'
    error_code = 1001  # 没找到资源

#token授权失败
class AuthFailed(APIException):
    code = 401  # 401未授权
    msg = '授权失败'
    error_code = 1005

#删除成功
class DeleteSuccess(Success):
    code=202
    msg='成功删除'
    error_code = -1

#禁止访问
class Forbidden(APIException):
    code=403
    error_code = 1004
    msg='禁止访问，您没有该类权限'
