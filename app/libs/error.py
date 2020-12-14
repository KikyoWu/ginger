from flask import request, json
from werkzeug.exceptions import HTTPException

class APIException(HTTPException):
    code=500#错误状态码500服务器产生一个未知的错误
    msg='sorry,we have a mistake 😆'
    error_code=999#错误代码，未知错误

    #设置构造函数，改变默认值
    #headers是HTTP的头信息
    def __init__(self,msg=None,code=None,error_code=None,headers=None):
        #判断传了参数，用传的参数替代默认参数
        if code:
            self.code=code
        if error_code:
            self.error_code=error_code
        if msg:
            self.msg=msg
        #使用super继承HTTPException的构造方法
        #description是msg,
        super(APIException,self).__init__(msg,None)

    #重写get_body
    def get_body(self, environ=None):
        """Get the json body."""
        body=dict(
            msg=self.msg,
            error_code=self.error_code,
            #当前错误信息是访问哪个api接口产生的
            #当前请求的http动词，当前请求的URL路径（不包括主机名和端口号）
            request=request.method+' '+self.get_url_no_param()
        )
        #返回json文本信息
        text=json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [("Content-Type", "application/json; charset=utf-8")]

    #静态方法，类和实例化对象都能调用
    #不包含？的URL
    @staticmethod
    def get_url_no_param():
        full_path=str(request.full_path)#拿到完整的url的路径
        #分割？前后，只保留？前的url（？用来过滤信息）
        main_path=full_path.split('?')
        return main_path[0]