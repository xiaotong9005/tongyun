import requests
from bs4 import BeautifulSoup
res=requests.get('https://trade.xincai.com/web/goodsFund?from=financefund')
res.encoding='utf-8'
soup=BeautifulSoup(res.text,'html.parser')
i=0
for news in soup.select('.row-box'):
    while i<len(news.select('td')):
        if i%13==0:
            print('-----------------',i/13+1,'--------------------')
        print('Item',i,':',news.select('td')[i].text);
        i=i+1;
