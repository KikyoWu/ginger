from wtforms import StringField,IntegerField
from wtforms.validators import DataRequired,length, Email, Regexp
from wtforms import ValidationError
from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form

#表单验证基类，通用
class ClientForm(Form):
    #validators=[DataRequired()]必须传入
    account=StringField(validators=[DataRequired(message='账号不允许为空'),length(min=5,max=32)])
    secret=StringField()
    type=IntegerField(validators=[DataRequired()])

    #自定义客户端类型验证,把数字转换成枚举
    def validate_type(self,value):
        try:
            client=ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data=client

#用户注册类验证
class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email('邮箱地址无效')
    ])
    secret = StringField(validators=[
        DataRequired('密码不能为空'),
        # password can only include letters , numbers and "_",6~12位
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$',message='密码必须为6~12位'),
    ])
    nickname = StringField(validators=[DataRequired('用户名不能为空'),
                                       length(min=2, max=22,message='用户名长度为2~22位')])

    #验证账号是否已经被注册过
    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError('该账号已注册')
