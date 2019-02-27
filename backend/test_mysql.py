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
# 新建游标
cursor = db.cursor()

# 增
sql = """INSERT INTO c(CNO, CNAME, CREDIT, CDEPT, TNAME)
         VALUES ('C10', '联合大作业', 10, '计算机应用', '吴邵刚')"""
try:
    # 执行SQL语句
    print('增加------')
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
    print("Error: unable to insert data")

# 删
sql = "DELETE FROM c WHERE CREDIT>8"
try:
    # 执行SQL语句
    print('删除-----')
    cursor.execute(sql)
    # 提交修改
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()
    print("Error: unable to delete data")

# 查
sql = "SELECT * FROM c;"
try:
    # 执行SQL语句
    print('查询------')
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        print(row)
except:
    print("Error: unable to fetch data")

# 改
# SQL 更新语句
sql = "UPDATE c SET CREDIT = CREDIT + 1 WHERE CNO = 'C5'"
try:
    # 执行SQL语句
    print("修改-----")
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()

# 关闭数据库连接
db.close()
