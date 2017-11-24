import requests
import pymysql
from bs4 import BeautifulSoup
db=pymysql.connect('localhost','root','xiaotong123','test',charset='utf8')
cur=db.cursor()
res=requests.get('http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=020000&keyword=%E6%95%B0%E6%8D%AE%E5%BA%93%E5%BC%80%E5%8F%91&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9')
res.encoding='utf-8'
soup=BeautifulSoup(res.text,'html.parser')
print(soup.prettify())
'''for news in soup.select('.newlist_deatil_two'):
    print(new)'''

db.close()
