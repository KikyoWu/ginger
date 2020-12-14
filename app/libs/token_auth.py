from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scopy import is_in_scope

auth=HTTPBasicAuth()
User=namedtuple('User',['uid','ac_type','scope'])

#传输token
@auth.verify_password
def verify_password(token,password):
    #通过http传递参数
    #header key:value
    #key Authorization
    #value basic base64(kikyo:123456)
    user_info=verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user=user_info
        return True

#验证token
def verify_auth_token(token):
    s=Serializer(current_app.config['SECRET_KEY'])
    try:
        data=s.loads(token)#解密token
    except BadSignature:#通过特定异常检测token是否合法
        raise AuthFailed(msg='token不合法',error_code=1002)
    except SignatureExpired:#检测token是否过期
        raise AuthFailed(msg='token过期',error_code=1003)
    uid=data['uid']
    ac_type=data['type']
    scope=data['scope']
    #request 视图函数
    allow=is_in_scope(scope,request.endpoint)#当前请求要访问的视图函数
    if not allow:
        raise Forbidden()
    return User(uid,ac_type,scope)