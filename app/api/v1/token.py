from flask import current_app, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.libs.enums import ClientTypeEnum
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm

api=Redprint('token')
#登陆
@api.route('',methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()  #实例化validators的forms客户端表单验证类
    promise = {
        ClientTypeEnum.USER_EMAIL:User.verify
    }
    identify=promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )
    #过期时间调整，写到配置文件中
    expiration=current_app.config['TOKEN_EXPIRATION']
    token=generate_auth_token(identify['uid'],
                              form.type.data,
                              identify['scope'],
                              expiration)
    #返回的数据需要是json格式，原来的是字符串
    t={
        'token':token.decode('ascii')
    }
    #返回序列化的t,http状态码
    return jsonify(t),201

#生成令牌
#uid用户ID，ac_type客户端类型，scope权限作用域，expiration过期时间
def generate_auth_token(uid,ac_type,scope=None,expiration=7200):
    #实例化一个序列化器,SECRET_KEY设置密钥，保证会话安全,expires_in有效期
    s=Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
    #把字典格式改为字符串格式
    return s.dumps(
        {
            'uid':uid,
            'type':ac_type.value,
            'scope':scope
        }
    )
