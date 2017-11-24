import requests
import pyodbc
from bs4 import BeautifulSoup

def isblank(a,b):
	if len(a)<1:
		return(b)
	else:
		return(a)
headers={
    'Cookie':'aliyungf_tc=AQAAAFNfvW+OGwMAB25Vcs52HlxDIra0; xq_a_token=82d9cefaa0793743cb186e53294ec0e61ac2abec; xq_a_token.sig=5N1bqGL6dBOdtpsJHPbhJk4l6_g; xq_r_token=11b86433a20d1d1eef63ecc12252297196a20e10; xq_r_token.sig=RPGspgHiNeURBrDthhch0e5_T0g; u=331500807840275; device_id=923502187b8a828f8a283f9134b3ea5d; s=gd12owoxky; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1500807845; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1500810074; __utma=1.1358685580.1500807993.1500807993.1500807993.1; __utmb=1.7.10.1500807993; __utmc=1; __utmz=1.1500807993.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }

db=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;PORT=1433;DATABASE=symbol;UID=sa;PWD=xiaotong123')
cur=db.cursor()

sqlquery="select distinct symbol,iif(exchange='Shenzhen','SZ','SH') as ex from [indexes]"
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
for codelst in codelist:
    print(j+1,end=':')
    ex=exchange[j]
    code=codelist[j]

    
    url='https://xueqiu.com/v4/stock/quote.json?code='+ex+code
    print(url,end='----')
    res=requests.get(url,headers=headers)
    res.encoding='utf-8'
    datastr=BeautifulSoup(res.text,'html.parser').text
    
    if len(datastr)>150:
        x=eval(datastr)
        excode=ex+code
        time=str(x[excode]['time'])[:10]+str(x[excode]['time'])[25:]
        delsql="delete from [symbol] where time='"+time+"' and symbol='"+excode+"';" 
        sql='''
        insert into symbol (update_time,symbol,name_cn,[current],pe_ttm,pe_lyr,pb,
        percentage,high52week,low52week,marketCapital,eps,beta,totalShares,net_assets,time)
        values(getdate(),'%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s')''' %(x[excode]['symbol'],
          x[excode]['name'],
          isblank(x[excode]['current'],0),
          isblank(x[excode]['pe_ttm'],0),
          isblank(x[excode]['pe_lyr'],0),
          isblank(x[excode]['pb'],0),
          isblank(x[excode]['percentage'],0),
          isblank(x[excode]['high52week'],0),
          isblank(x[excode]['low52week'],0),
          isblank(x[excode]['marketCapital'],0),
          isblank(x[excode]['eps'],0),
          isblank(x[excode]['beta'],0),
          isblank(x[excode]['totalShares'],0),
          isblank(x[excode]['net_assets'],0),
          time)

        try:
            cur.execute(delsql)
            cur.execute(sql)
            db.commit()
            print('数据提取成功')
        except:
            print(url)
            db.rollback()
            print('数据提取失败')
    else:
        print('股票代码不存在')
    j=j+1
db.close()
