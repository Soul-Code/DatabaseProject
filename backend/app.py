from flask import Flask
from flask import make_response
from flask import request
from flask import session
from flask_cors import CORS
import os
from datetime import timedelta
import json
# 导入配置文件
from config import Config
import pymysql

# from flask_sqlalchemy import SQLAlchemy
# 建立数据库连接
db = pymysql.connect(
    user="root",
    password="314219Yh",
    host="120.78.94.204",
    port=3306,
    database="course_selection_system"
)
# # 新建游标
# cursor = db.cursor()
# # 使用 execute()  方法执行 SQL 查询
# cursor.execute("SELECT VERSION()")

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(Config)


# app.config['SECRET_KEY'] = os.urandom(24)
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)


# 建立数据库关系,使用SQLAlchemy
# db = SQLAlchemy(app)
@app.after_request
def af_request(resp):
    """
    #请求钩子，在所有的请求发生后执行，加入headers,允许跨域访问
    :param resp:
    :return:
    """
    resp = make_response(resp)
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


@app.route('/')
@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/api/login', methods=['POST'])
def login():
    cursor = db.cursor()
    request_data = request.json
    print(request_data)
    sql = "SELECT LOGN,PSWD,SNAME,SNO FROM s"
    cursor.execute(sql)
    students = cursor.fetchall()
    login = False
    response = {'ok': False}
    user = None
    for row in students:
        print(row)
        if row[0] == request_data['username']:
            print('用户名正确')
            if row[1] == request_data['psword']:
                print('密码正确')
                user = row
                login = True
                response['ok'] = True
                response['role'] = 'student'
                session.permanent = True
                session['role'] = 'student'
                session['user'] = user[3]
                print(session)
                break
    if login:
        response['msg'] = user[2] + '登陆成功！'
    else:
        response['msg'] = '用户名或密码错误！'
    cursor.close()
    return json.dumps(response)


@app.route('/var/<varname>')
def var(varname):
    return 'Var:  %s' % varname


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    response = {'ok': True}
    return json.dumps(response)


@app.route('/api/sdata', methods=['POST'])
def get_student_data():
    request_data = request.json  # request是从服务器返回的数据，后面加.json是将数据转化为python的字典，方便使用
    print(request_data)
    cursor = db.cursor()  # 新建一个数据库游标
    response = {'ok': True}  # response是返回给服务器的数据，也是字典格式
    print(session)  # session是会话，服务器端的全局变量，每个用户对应一个session
    if session.get('user', False):  # 看一下session里面有没有学号（登陆的时候会把学号存进去
        sql = "SELECT * FROM s WHERE SNO='%s'" % session['user']  # 构造sql语句
        cursor.execute(sql)  # 执行sql语句
        s = cursor.fetchall()  # 获取sql执行结果
        print(s)
        response['info'] = s  # 把结果保存在response里面
    return json.dumps(response)  # 将response从字典格式转化为json格式反馈给前端


@app.route('/api/get_students', methods=['POST'])
def get_students():
    request_data = request.json
    print(request_data)
    cursor = db.cursor()
    response = {'ok': True}
    print(session)
    sql = "SELECT * FROM s"
    cursor.execute(sql)
    s = cursor.fetchall()
    print(s)
    response['info'] = s
    return json.dumps(response)


# 教师端
@app.route('/api/get_courses', methods=['POST'])
def get_courses():
    request_data = request.json
    print(request_data)
    cursor = db.cursor()
    response = {'ok': True}
    sql = 'SELECT CNAME,CNO FROM c'
    cursor.execute(sql)
    response['courses'] = [i for i in cursor.fetchall()]
    print(response)
    return json.dumps(response)


@app.route('/api/get_score', methods=['POST'])
def get_score():
    request_data = request.json
    print(request_data)
    cursor = db.cursor()
    response = {'ok': True}
    sql = "SELECT SNAME,GRADE,s.SNO FROM sc,s WHERE sc.SNO=s.SNO AND sc.CNO='%s'" % request_data['cno']
    cursor.execute(sql)
    response['students'] = [i for i in cursor.fetchall()]
    print(response)
    return json.dumps(response)


@app.route('/api/save_score', methods=['POST'])
def save_score():
    request_data = request.json
    datas = request_data['datas']
    cno = request_data['cno']
    cursor = db.cursor()
    response = {'ok': True}
    for i in range(len(datas)):
        print(datas[i])
        sql = "UPDATE sc SET GRADE=%d WHERE SNO='%s' and CNO='%s'" % (int(datas[i]['score']), datas[i]['sno'], cno)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    # sql = ''
    # cursor.execute(sql)
    return json.dumps(response)


if __name__ == '__main__':
    app.run()
