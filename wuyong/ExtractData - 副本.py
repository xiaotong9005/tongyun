import pymysql
db=pymysql.connect('localhost','root','xiaotong123','test',charset='utf8')
cur=db.cursor()
f=open('F:\\securities\\000300cons.txt')
f.readline() 
for i_f in f:
    strlist=i_f.split('	',i_f.count('	'))
    sql = "insert into indexes(i_code,s_code,name_cn,name_en,exchange,updatetime) values \
        ('"+strlist[0]+"','"+strlist[1]+"','"+strlist[2]+"','"+strlist[3]+"','"+strlist[4]+"',now())" 
    try:
        cur.execute(sql)
        db.commit()
        print("执行成功,值：('"+strlist[0]+"','"+strlist[1]+"','"+strlist[2]+"','"+strlist[3]+"','"+strlist[4]+"')")
    except:
        db.rollback()
        print("执行成功,值：('"+strlist[0]+"','"+strlist[1]+"','"+strlist[2]+"','"+strlist[3]+"','"+strlist[4]+"')")
db.close()
