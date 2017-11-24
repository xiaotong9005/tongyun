import pymysql
dbconn=pymysql.connect('localhost','root','xiaotong123','test')
cur=dbconn.cursor()
sql="insert into indexes (i_code) value (now())"
try:
        cur.execute(sql)
        dbconn.commit()
        print('data update has successed')
except:
        dbconn.rollback()
        print('data update has failed')
dbconn.close()
print('database has closed!')    
