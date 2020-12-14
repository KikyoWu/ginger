from sqlalchemy import Column, Integer, String, SmallInteger,DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db
from datetime import datetime,date


#User模型，继承自定义的base.py中的Base类
class User(Base):
    id=Column(Integer,primary_key=True)
    email=Column(String(24),unique=True,nullable=False)
    nickname=Column(String(24),unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    auth=Column(SmallInteger,default=1)
    _password=Column('password',String(100))

    def keys(self):
        return ['id','email','nickname','auth','addtime']


    #把类中定义的实例方法变成类属性
    @property
    def password(self):
        return self._password

    #@property对于新式类来说定义的属性是一个只读属性，如果需要可写，则需要一个@属性.setter装饰器装饰该函数
    @password.setter
    def password(self,raw):
        self._password=generate_password_hash(raw)

    #注册方法
    @staticmethod#在对象下面再创建对象本身不合理，要用静态方法
    def register_by_email(nickname,account,secret):
        #在数据库中使用auto_commit()方法新增用户
        with db.auto_commit():
            user=User()
            user.nickname=nickname
            user.email=account
            user.password=secret
            db.session.add(user)
            db.session.flush()

    #获取账号验证的方法
    @staticmethod
    def verify(email,password):
        user=User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope='AdminScope' if user.auth==2 else 'UserScope'
        return {'uid':user.id,'scope':scope}

    #检查账号密码
    def check_password(self,raw):
        if not self._password:
            return False
        return check_password_hash(self._password,raw)

