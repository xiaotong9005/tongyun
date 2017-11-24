import requests
from bs4 import BeautifulSoup
res=requests.get('http://news.sina.com.cn/china/')
res.encoding='utf-8'
'''print(res.text)'''
soup=BeautifulSoup(res.text,'html.parser')
i=0
for news in soup.select('.blk122'):
    while i<len(news.select('a')):
        print(news.select('a')[i].text)
        i=i+1;
