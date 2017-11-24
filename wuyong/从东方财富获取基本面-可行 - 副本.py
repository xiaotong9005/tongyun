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
    print('CodeList获取失败')
j=0    
while j==0:
    ex=exchange[j]
    code=codelist[j]
    res=requests.get('http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code=sh603331')
    res.encoding='utf-8'
    soup=BeautifulSoup(res.text,'html.parser')
    #print(soup.prettify())
    print('-------季度报-------')
    for dubang_report in soup.select('.dubang_report'):
        print(dubang_report.text)
    print('-------年报-------')
    for dubang_year in soup.select('.dubang_year'):
        print(dubang_year.text)
    print('-------净资产收益率-------')
    for db_01 in soup.select('.db_01'):
        print(db_01.select('p')[0].text)
    print('-------硬指标-------')        
    for db_04 in soup.select('.db_04'):
        print('净利润'+db_04.select('p')[0].text)#净利润
        print('营业收入'+db_04.select('p')[1].text)#营业收入
        print('资产总额'+db_04.select('p')[3].text)#资产总额
        print('负债总额'+db_04.select('p')[4].text)#负债总额
        print('---------')
    
    j+=1
db.close()
string='''
hello,这里是许晓彤。
好久没有写过东西了，写点什么吧。
我从去年在成都的时候开始，常看非诚勿扰，有一年小多的时间了。今天是周六，依旧是看了。
看非诚勿扰，是个很有意思的事情，透过别人在台上的言行，在他们自己对过去的表述，猜测他是一个什么样的人，\
猜对猜错都觉得很有意思，'人'是这个平台上最有意思的事情。
最近有一个女嘉宾我比较关注，叫做马蓉。当然不是绿了宝宝那位。这两位







'''
print(string)
