import pymysql
db=pymysql.connect('localhost','root','xiaotong123','test')
cur=db.cursor()
sql = "insert into indexes(i_code,s_code,name_cn,name_en,exchange) values(\'1\',\'1\',\'1\',\'1\',\'1\');"
try:
    cur.execute(sql)
    db.commit()
    print('执行成功')
except:
    db.rollback()
    print('执行失败')
db.close()
