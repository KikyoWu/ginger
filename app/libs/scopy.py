#添加权限
class scope:
    allow_api=[]#视图函数
    allow_module=[]#模块
    forbidden=[]#排除的视图函数
    def __add__(self, other):
        #视图函数
        self.allow_api+=other.allow_api
        self.allow_api=list(set(self.allow_api))#去重

        #模块
        self.allow_module += other.allow_module
        self.allow_module = list(set(self.allow_module))

        # 排除
        self.forbidden += other.forbidden
        self.forbidden = list(set(self.forbidden))
        return self

#管理员权限
class AdminScope(scope):
    #记录可以访问哪些视图函数
    #allow_api=['v1.user+super_get_user','v1.user+super_delete_user']
    allow_module=['v1.user']
    #视图函数权限相加
    def __init__(self):
        pass
        #self+UserScope()

#用户权限
class UserScope(scope):
    forbidden=['v1.user+super_get_user','v1.user+super_delete_user']
    def __init__(self):
        self+AdminScope()
    #allow_api = ['v1.user+get_user','v1.user+delete_user']

#判断某个scope是否能访问某个视图函数
def is_in_scope(scope,endpoint):
    scope=globals()[scope]()#将字符串的类对象实例化
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    #endpoint=v1.view_func 改成v1.red_name+view_func
    splits=endpoint.split('+')
    red_name=splits[0]
    if red_name in scope.allow_module:#某个模块名是否在用户权限模块名下
        return True
    else:
        return False
