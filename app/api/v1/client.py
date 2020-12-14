from flask import request
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import ClientTypeError, Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm
from app.libs.enums import ClientTypeEnum

api=Redprint('client')

@api.route('/register',methods=['POST'])
def create_client():
    form=ClientForm().validate_for_api()#实例化validators的forms客户端表单验证类
    promise={
        ClientTypeEnum.USER_EMAIL:__register_user_by_email,
        ClientTypeEnum.USER_WX: __register_user_by_wx
    }
    #获取登陆类型的枚举对象
    promise[form.type.data]()
    return Success()
        #switch不同的客户端编写不同的注册代码
    #request.args.to_dict()
    #表单 json
    #注册 登陆
    #参数 校验 接受参数
    #WTForms 校验表单

#用户用emil注册的相关代码
def __register_user_by_email():#从form的验证器中获取注册需要的参数
    #request.json['nickname']
    form=UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data, form.account.data, form.secret.data)

def __register_user_by_wx():
    pass