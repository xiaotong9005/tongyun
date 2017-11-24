import requests
import pyodbc
from bs4 import BeautifulSoup

def isblank(a,b):
	if len(str(a))<1:
		return(b)
	else:
		return(a)

headers={
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'no-cache',
'Connection':'keep-alive',
'Cookie':'s=f912lcxbln; webp=0; device_id=ac8c5b627b0dd85a469ec02b62aba4a0; bid=52059a060047074a47353ec1117d051a_j4sbyrwa; xq_a_token=45fd777f51337c7a4673f1f5a14b63c417bf8b07; xqat=45fd777f51337c7a4673f1f5a14b63c417bf8b07; xq_r_token=a09e0b1f8f26eb4cc6153cc169d2466c83f24126; u=4638404960; xq_token_expire=Mon%20Aug%2028%202017%2023%3A34%3A55%20GMT%2B0800%20(CST); aliyungf_tc=AQAAAHbepDx5SgwANUNZcgVSFHqw57W7; xq_is_login=1; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1501774200,1501807127,1501855516,1501856563; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1501858639; __utma=1.1318945200.1493526591.1501855542.1501858620.21; __utmb=1.5.9.1501858625689; __utmc=1; __utmz=1.1501766009.16.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
'Host':'xueqiu.com',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3228.1 Safari/537.36',
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
    url='https://xueqiu.com/stock/f10/compinfo.json?symbol='+ex+code
    print('数据来自:'+url,end=';')
    res=requests.get(url,headers=headers)
    res.encoding='utf-8'
    datastr=BeautifulSoup(res.text,'html.parser').text
    if len(datastr)>150:#存在该股票代码
        fi=eval(datastr.replace("null","''",500))
        sqldel="delete from [compinfo] where symbol='"+ex+code+"'"
        sql='''
                insert into CompInfo(
                symbol,
                compname,
                engname,
                orgtype,
                leconstant,
                accfirm,
                regaddr,
                officeaddr,
                bizscope,
                majorbiz,
                compsname
                ) values(
                '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'
                )
                ''' %(          ex+code
                                ,fi['tqCompInfo']['compname']
                                ,fi['tqCompInfo']['engname']
                                ,fi['tqCompInfo']['orgtype']
                                ,fi['tqCompInfo']['leconstant']
                                ,fi['tqCompInfo']['accfirm']
                                ,fi['tqCompInfo']['regaddr']
                                ,fi['tqCompInfo']['officeaddr']
                                ,fi['tqCompInfo']['bizscope']
                                ,fi['tqCompInfo']['majorbiz']
                                ,fi['tqCompInfo']['compsname']
                      )
        try:
            cur.execute(sqldel)
            cur.execute(sql)
            db.commit()
            print('提取成功--'+fi['tqCompInfo']['compname'])
        except:
            db.rollback()
            print(code+fi['tqCompInfo']['compname']+'提取失败')
    else:
        print('股票代码不存在')
    j=j+1
db.close()
