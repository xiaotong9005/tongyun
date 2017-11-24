import requests
from bs4 import BeautifulSoup
res=requests.get('http://stockhtm.finance.qq.com/fund/jzzx/index.htm')

soup=BeautifulSoup(res.text,'html.parser')

print(soup.select('.color-blue')[0].text)
