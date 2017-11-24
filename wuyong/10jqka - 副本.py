import requests
import pymysql
from bs4 import BeautifulSoup
db=pymysql.connect('localhost','root','xiaotong123','test',charset='utf8')
cur=db.cursor()
sqlquery="select distinct s_code from indexes"
codelist=[]
try:
    cur.execute(sqlquery)
    results=cur.fetchall()
    for row in results:
        codelist.append(row[0])
except:
    print('Codelist获取失败')
j=0    
for code in codelist:
    i=codelist[j]
    res=requests.get('http://quote.eastmoney.com/sh'+str(i)+'.html')
    res.encoding='gb2312'
    soup=BeautifulSoup(res.text,'html.parser')
    #print(soup.prettify())
    for news in soup.select('.cwzb'):
        if news.select('td')[4].text!='-':
            pe=float(news.select('td')[4].text)
            pb=float(news.select('td')[5].text)
            roe=str(news.select('td')[8].text)
            sql="insert into fundamental (s_code,pe,pb,roe,updatetime) values \
            ('"+str(i)+"',"+news.select('td')[4].text+","+news.select('td')[5].text+",'"+roe+"',now()) "
            try:
                cur.execute(sql)
                db.commit()
                print(str(i)+'-成功:'+',pe:'+str(pe)+',pb:'+str(pb)+',roe:'+str(roe))
            except:
                db.rollback()
                print(str(i)+'-失败:'+',pe:'+str(pe)+',pb:'+str(pb)+',roe:'+str(roe))
    j+=1
db.close()
