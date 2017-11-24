import requests
import pyodbc
from bs4 import BeautifulSoup

def isblank(a,b):
	if len(str(a))<1:
		return(b)
	else:
		return(a)
headers={
        'Cookie':'device_id=923502187b8a828f8a283f9134b3ea5d; s=gd12owoxky; aliyungf_tc=AQAAAMhBEBAKwwUAGNKutLDP13gosQvd; xq_a_token=82d9cefaa0793743cb186e53294ec0e61ac2abec; xq_a_token.sig=5N1bqGL6dBOdtpsJHPbhJk4l6_g; xq_r_token=11b86433a20d1d1eef63ecc12252297196a20e10; xq_r_token.sig=RPGspgHiNeURBrDthhch0e5_T0g; u=381501259919928; __utmt=1; __utma=1.1358685580.1500807993.1501259925.1501293474.3; __utmb=1.6.10.1501293474; __utmc=1; __utmz=1.1500807993.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_1db88642e346389874251b5a1eded6e3=1500807845,1501259921; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1501293544',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
db=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;PORT=1433;DATABASE=symbol;UID=sa;PWD=xiaotong123')
cur=db.cursor()
codelist=[]
exchange=[]
sqlquery="select distinct symbol,iif(exchange='Shenzhen','SZ','SH') as ex from [indexes]"
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
    url='https://xueqiu.com/stock/f10/finmainindex.json?symbol='+ex+code
    print('数据来自:'+url,end=';')
    res=requests.get(url,headers=headers)
    res.encoding='utf-8'
    datastr=BeautifulSoup(res.text,'html.parser').text
    if len(datastr)>150:#存在该股票代码
        fi=eval(datastr.replace("null","''",500))
        for ireport in fi['list']:
                sql='''
                        insert into finance(
                        compcode
                        ,reportdate
                        ,basiceps
                        ,epsdiluted
                        ,epsweighted
                        ,naps
                        ,opercashpershare
                        ,peropecashpershare
                        ,netassgrowrate
                        ,dilutedroe
                        ,weightedroe
                        ,mainbusincgrowrate
                        ,netincgrowrate
                        ,totassgrowrate
                        ,salegrossprofitrto
                        ,mainbusiincome
                        ,mainbusiprofit
                        ,totprofit
                        ,netprofit
                        ,totalassets
                        ,totalliab
                        ,totsharequi
                        ,operrevenue
                        ,invnetcashflow
                        ,finnetcflow
                        ,chgexchgchgs
                        ,cashnetr
                        ,cashequfinbal
                        ,symbol
                        ,name
                        ,totalshare
                        ) values(
                        '%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s','%s',%s
                        )
                        ''' %(   ireport['compcode']
                                ,ireport['reportdate']
                                ,isblank(ireport['basiceps'],0)
                                ,isblank(ireport['epsdiluted'],0)
                                ,isblank(ireport['epsweighted'],0)
                                ,isblank(ireport['naps'],0)
                                ,isblank(ireport['opercashpershare'],0)
                                ,isblank(ireport['peropecashpershare'],0)
                                ,isblank(ireport['netassgrowrate'],0)
                                ,isblank(ireport['dilutedroe'],0)
                                ,isblank(ireport['weightedroe'],0)
                                ,isblank(ireport['mainbusincgrowrate'],0)
                                ,isblank(ireport['netincgrowrate'],0)
                                ,isblank(ireport['totassgrowrate'],0)
                                ,isblank(ireport['salegrossprofitrto'],0)
                                ,isblank(ireport['mainbusiincome'],0)
                                ,isblank(ireport['mainbusiprofit'],0)
                                ,isblank(ireport['totprofit'],0)
                                ,isblank(ireport['netprofit'],0)
                                ,isblank(ireport['totalassets'],0)
                                ,isblank(ireport['totalliab'],0)
                                ,isblank(ireport['totsharequi'],0)
                                ,isblank(ireport['operrevenue'],0)
                                ,isblank(ireport['invnetcashflow'],0)
                                ,isblank(ireport['finnetcflow'],0)
                                ,isblank(ireport['chgexchgchgs'],0)
                                ,isblank(ireport['cashnetr'],0)
                                ,isblank(ireport['cashequfinbal'],0)
                                ,ex+code
                                ,ireport['name']
                                ,isblank(ireport['totalshare'],0)
                              )
                sqldel="delete from [finance] where symbol='"+ex+code+"' and reportdate='"+ireport['reportdate']+"'"
                try:
                    cur.execute(sqldel)
                    cur.execute(sql)
                    db.commit()
                except:
                    db.rollback()
        print(fi['list'][len(fi)]['reportdate']+'至'+fi['list'][0]['reportdate']+'提取成功')
    else:
        print('股票代码不存在.')
    j=j+1
db.close()
