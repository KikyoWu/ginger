from flask import request
from wtforms import Form
from app.libs.error_code import ParameterException

#通用异常验证
class BaseForm(Form):
    def __init__(self):
        data=request.json#获得客户端参数
        super().__init__(data=data)
    '''重写validate方法
    def validate(self):
        pass'''
    #保留原有validate方法，实现类似于validate方法
    def validate_for_api(self):
        valid=super().validate()#实现原有验证方法
        if not valid:
            #使不同错误参数传递不同错误信息，从form errors
            raise ParameterException(msg=self.errors)
        return self
