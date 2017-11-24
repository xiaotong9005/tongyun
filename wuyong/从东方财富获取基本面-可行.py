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
    print('CodeList获取失败')
j=0    
while j==0:
    ex=exchange[j]
    code=codelist[j]
    res=requests.get('http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code=sh600000')
    res.encoding='utf-8'
    soup=BeautifulSoup(res.text,'html.parser')
    #print(soup.prettify())
    #-------季度报告期list-------
    code_num=1
    print('-------季度报-------')
    for dubang_report in soup.select('.dubang_report'):
        print(dubang_report.text+','+str(code_num))
        code_num+=1
    #--------年报list--------
    print('-------年报-------')
    for dubang_year in soup.select('.dubang_year'):
        print(dubang_year.text+','+str(code_num))
        code_num+=1
    #-------净资产收益率（ROE）-------
    code_num=1
    print('-------净资产收益率（ROE）-------')
    for db_01 in soup.select('.db_01'):
        print(db_01.select('p')[0].text+','+str(code_num))
        code_num+=1
    #-------其他指标-------
    code_num=1
    print('-------硬指标-------')        
    for db_04 in soup.select('.db_04'):
        print(str(code_num))
        print('净利润'+db_04.select('p')[0].text)#净利润
        print('营业收入'+db_04.select('p')[1].text)#营业收入
        print('资产总额'+db_04.select('p')[3].text)#资产总额
        print('负债总额'+db_04.select('p')[4].text)#负债总额
        print('------------')
        code_num+=1
    
    j+=1
db.close()
