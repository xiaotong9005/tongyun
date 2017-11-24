import requests
import pymysql
from bs4 import BeautifulSoup
db=pymysql.connect('localhost','root','xiaotong123','test',charset='utf8')
cur=db.cursor()
#sqlquery="select distinct s_code,if(exchange like '%hanghai%','sh',if(exchange like '%henzhen%','sz',exchange)) as ex from indexes"
sqlquery="select distinct s_code,if(exchange like '%hanghai%','sh',if(exchange like '%henzhen%','sz',exchange)) as ex from indexes where exchange is not null union  select distinct s_code,'sz' as ex from indexes where exchange is null union select distinct s_code,'sh' as ex from indexes where i_code in('399553','399552')"
codelist=[]
exchange=[]
try:
    cur.execute(sqlquery)
    results=cur.fetchall()
    for row in results:
        codelist.append(row[0])
        exchange.append(row[1])
except:
    print('Codelist获取失败')
j=0    
for code in codelist:
    ex=exchange[j]
    code=codelist[j]
    res=requests.get('http://quote.eastmoney.com/'+ex+code+'.html')
    res.encoding='gb2312'
    soup=BeautifulSoup(res.text,'html.parser')
    for news in soup.select('.cwzb'):
        if news.select('td')[4].text!='-':
            pe=float(news.select('td')[4].text)
            pb=float(news.select('td')[5].text)
            roe=str(news.select('td')[8].text)
            sql="insert into fundamental (s_code,pe,pb,roe,update_time) values \
            ('"+code+"',"+news.select('td')[4].text+","+news.select('td')[5].text+",'"+roe+"',now()) "
            try:
                cur.execute(sql)
                db.commit()
                print(ex+code+'-成功:'+',pe:'+str(pe)+',pb:'+str(pb)+',roe:'+str(roe))
            except:
                db.rollback()
                print(ex+code+'-失败:'+',pe:'+str(pe)+',pb:'+str(pb)+',roe:'+str(roe))       
    j+=1
db.close()
