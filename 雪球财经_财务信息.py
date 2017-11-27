import requests
import pyodbc
from bs4 import BeautifulSoup

def isblank(a,b):
	if len(str(a))<1:
		return(b)
	else:
		return(a)
headers={
        'Cookie':'device_id=d9386e7d5baba9d2a4c917754d3c0f41; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=533ee92f6b8c235e8c4a616942a644ed228f9143; xq_a_token.sig=P7m6dJXADGBCqVKrLs2wpMjy_uQ; xq_r_token=7504c3605b03433d12104e983e35b826ad5b099b; xq_r_token.sig=S1zJtwESNRpJ6tgAW_QNhKKbFgI; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=4638404960; u.sig=eg9ViMeUGocmuzlXM5UIAF_U9IM; s=f312jmpyty; bid=52059a060047074a47353ec1117d051a_ja7sfsjh; isPast=true; isPast.sig=Q1zWad3glPfOy3Ye-506BMax-a0; aliyungf_tc=AQAAAKaG6WTvigoAMZv0Zd8GAyR2TlSO; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1511271702,1511279285,1511681023,1511787958; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1511788141; __utma=1.600829631.1511157314.1511681045.1511787964.4; __utmb=1.3.10.1511787964; __utmc=1; __utmz=1.1511157314.1.1.utmcsr=xueqiu.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
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
