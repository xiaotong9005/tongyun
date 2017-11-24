import pymysql

# 打开数据库连接
db = pymysql.connect("localhost","root","xiaotong123","test" )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# SQL 插入语句
sql = "INSERT INTO indexes(i_code) \
       VALUES ('%s')" % \
       ('Mac')
try:
   # 执行sql语句
   cursor.execute(sql)
   # 执行sql语句
   db.commit()
   print('suce')
except:
   # 发生错误时回滚
   db.rollback()
   print('fail')
# 关闭数据库连接
db.close()
