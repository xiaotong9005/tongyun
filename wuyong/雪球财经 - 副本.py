import requests
import pymysql
from bs4 import BeautifulSoup
db=pymysql.connect('localhost','root','xiaotong123','indexes',charset='utf8')
cur=db.cursor()
headers={  
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'cache-control':'no-cache',
    'Connection':'keep-alive',
    'Cookie':'aliyungf_tc=AQAAAFNfvW+OGwMAB25Vcs52HlxDIra0; xq_a_token=82d9cefaa0793743cb186e53294ec0e61ac2abec; xq_a_token.sig=5N1bqGL6dBOdtpsJHPbhJk4l6_g; xq_r_token=11b86433a20d1d1eef63ecc12252297196a20e10; xq_r_token.sig=RPGspgHiNeURBrDthhch0e5_T0g; u=331500807840275; device_id=923502187b8a828f8a283f9134b3ea5d; s=gd12owoxky; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1500807845; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1500810074; __utma=1.1358685580.1500807993.1500807993.1500807993.1; __utmb=1.7.10.1500807993; __utmc=1; __utmz=1.1500807993.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'Host':'xueqiu.com',
    'Referer':'https://xueqiu.com/s/SH600000',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
    }  
res=requests.get('https://xueqiu.com/v4/stock/quote.json?code=SH600000',headers=headers)
res.encoding='utf-8'
soup=BeautifulSoup(res.text,'html.parser')
#print(soup.prettify())
#soup.select('.dubang_report')

sql="insert into symbol (update_time,remarks) values(now(),'"+soup.text+"')"
try:
    cur.execute(sql)
    db.commit()
    print('成功')
except:
    db.rollback()
    print('失败')
    
updatesql='''
    update symbol set current=substring(remarks,LOCATE('current',remarks)+length('current')+3,locate('"',substring(remarks,LOCATE('current',remarks)+length('current')+3,100))-1)
    ,pe_ttm=substring(remarks,LOCATE('pe_ttm',remarks)+length('pe_ttm')+3,locate('"',substring(remarks,LOCATE('pe_ttm',remarks)+length('pe_ttm')+3,100))-1)
    ,pe_lyr=substring(remarks,LOCATE('pe_lyr',remarks)+length('pe_lyr')+3,locate('"',substring(remarks,LOCATE('pe_lyr',remarks)+length('pe_lyr')+3,100))-1)
    ,pb=substring(remarks,LOCATE('pb',remarks)+length('pb')+3,locate('"',substring(remarks,LOCATE('pb',remarks)+length('pb')+3,100))-1)
    ,percentage=substring(remarks,LOCATE('percentage',remarks)+length('percentage')+3,locate('"',substring(remarks,LOCATE('percentage',remarks)+length('percentage')+3,100))-1)
    ,high52week=substring(remarks,LOCATE('high52week',remarks)+length('high52week')+3,locate('"',substring(remarks,LOCATE('high52week',remarks)+length('high52week')+3,100))-1)
    ,low52week=substring(remarks,LOCATE('low52week',remarks)+length('low52week')+3,locate('"',substring(remarks,LOCATE('low52week',remarks)+length('low52week')+3,100))-1)
    ,marketCapital=substring(remarks,LOCATE('marketCapital',remarks)+length('marketCapital')+3,locate('"',substring(remarks,LOCATE('marketCapital',remarks)+length('marketCapital')+3,100))-1)
    ,eps=substring(remarks,LOCATE('eps',remarks)+length('eps')+3,locate('"',substring(remarks,LOCATE('eps',remarks)+length('eps')+3,100))-1)
    ,beta=substring(remarks,LOCATE('beta',remarks)+length('beta')+3,locate('"',substring(remarks,LOCATE('beta',remarks)+length('beta')+3,100))-1)
    ,totalShares=substring(remarks,LOCATE('totalShares',remarks)+length('totalShares')+3,locate('"',substring(remarks,LOCATE('totalShares',remarks)+length('totalShares')+3,100))-1)
    ,time=substring(remarks,LOCATE('time',remarks)+length('time')+3,locate('"',substring(remarks,LOCATE('time',remarks)+length('time')+3,100))-1)
    ,net_assets=substring(remarks,LOCATE('net_assets',remarks)+length('net_assets')+3,locate('"',substring(remarks,LOCATE('net_assets',remarks)+length('net_assets')+3,100))-1)
    ,name_cn=substring(remarks,LOCATE('name_cn',remarks)+length('name_cn')+3,locate('"',substring(remarks,LOCATE('name_cn',remarks)+length('name_cn')+3,100))-1)
    ,symbol=substring(remarks,LOCATE('symbol',remarks)+length('symbol')+3,locate('"',substring(remarks,LOCATE('symbol',remarks)+length('symbol')+3,100))-1)
    ;
    '''
try:
    cur.execute(updatesql)
    db.commit()
    print('成功')
except:
    db.rollback()
    print('失败')
db.close()
