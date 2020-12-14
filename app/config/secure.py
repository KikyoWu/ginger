#连接数据库
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123@127.0.0.1:3306/ginger'
# 设置密钥，保证会话安全
SECRET_KEY = '\x8d\x7f\xaf\xc8"a\xa1]c\xba\xcb\x80x\xbc\x97s'
#跟踪修改
SQLALCHEMY_TRACK_MODIFICATIONS = True
#自动提交
SQLALCHEMY_COMMIT_TEARDOWN = True