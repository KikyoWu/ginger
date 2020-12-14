from app import create_app
from app.libs.error import APIException
from werkzeug.exceptions import HTTPException

from app.libs.error_code import ServerError

app=create_app()

#捕获全局异常
@app.errorhandler(Exception)
def framework_error(e):
    #e可能是APIException，HTTPException,Exception
    if isinstance(e,APIException):
        return e
    if isinstance(e,HTTPException):
        code=e.code
        msg=e.description
        error_code=1007
        return APIException(msg,code,error_code)
    else:
        #调试模式把错误信息全爆出，其他情况爆出定义的have a mistake信息
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e

if __name__=='__main__':
    app.run(debug=True)

