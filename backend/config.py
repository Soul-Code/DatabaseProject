class Config(object):
    SECRET_KEY = 'a9087FFJFF9nnvc2@#$%FSD'
    # 格式为mysql+pymysql://数据库用户名:密码@数据库地址:端口号/数据库的名字?数据库格式
    SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:314219Yh@120.78.94.204:3306/school?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
