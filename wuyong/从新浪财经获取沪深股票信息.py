import requests
import pymysql
from bs4 import BeautifulSoup
db=pymysql.connect('localhost','root','xiaotong123','test',charset='utf8')
cur=db.cursor()
sqlquery="select distinct s_code,if(exchange like '%hanghai%','sh',if(exchange like '%henzhen%','sz',exchange)) as ex from indexes"
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
#for code in codelist:
while j<1:
    ex=exchange[j]
    code=codelist[j]
    res=requests.get('http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code=sz000656')
    res.encoding='gb2312'
    soup=BeautifulSoup(res.text,'html.parser')
    print(soup.select('.jssz'))

    j+=1
db.close()
