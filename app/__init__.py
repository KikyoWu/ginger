from .app import Flask

#蓝图注册到app
def register_blueprint(app):
    '''from app.api.v1.user import user
    from app.api.v1.book import book
    app.register_blueprint(user)
    app.register_blueprint(book)'''
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(),url_prefix='/v1')

#使SQLALcjhemy生效
def register_plugin(app):
    from app.models.base import db#导入db
    db.init_app(app)#db注册
    #create_all要在app的上下文环境中进行操作
    with app.app_context():
        db.create_all()#创建所有数据库的数据表

def create_app():
    app=Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    register_blueprint(app)
    register_plugin(app)
    return app