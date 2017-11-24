import requests
from bs4 import BeautifulSoup
res=requests.get('https://trade.xincai.com/web/goodsFund?from=financefund')
res.encoding='utf-8'
'''print(res.text)'''
soup=BeautifulSoup(res.text,'html.parser')
i=0
for news in soup.select('.row-box'):
    while i<len(news.select('td')):
        print(news.select('td')[i].text)
        i=i+1;
