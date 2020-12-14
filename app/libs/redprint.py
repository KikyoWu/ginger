class Redprint:
    def __init__(self,name):
        self.name=name
        self.mound=[]

    #rule注册的URL，option其他可选选择
    def route(self,rule,**options):
        #f装饰器作用的函数
        def decorator(f):
            self.mound.append((f,rule,options))
            return f
        return decorator

    def register(self,bp,url_prefix=None):
        if url_prefix is None:
            url_prefix='/'+self.name
        for f,rule,options in self.mound:
            #字典中有endpoint取endpoint，没有取视图函数的名字作为endpoint
            # f.__name__取默认值
            endpoint = self.name+'+'+options.pop("endpoint", f.__name__)
            #蓝图注册到视图函数上
            bp.add_url_rule(url_prefix+rule,endpoint,f,**options)


