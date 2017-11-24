import requests
import pymysql
from bs4 import BeautifulSoup

res=requests.get('http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code=sh600000')
res.encoding='utf-8'
soup=BeautifulSoup(res.text,'html.parser')
print(soup.prettify())
#soup.select('.dubang_report')
   
