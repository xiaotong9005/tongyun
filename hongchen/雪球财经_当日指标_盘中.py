import requests
import pyodbc
from bs4 import BeautifulSoup
from time import strftime
def isblank(a,b):
        if len(a)<1:
                return(b)
        else:
                return(a)
        
def monthnum(string):
    if string.lower()=='jan':
        return('01')
    elif string.lower()=='feb':
        return('02')
    elif string.lower()=='mar':
        return('03')
    elif string.lower()=='apr':
        return('04')
    elif string.lower()=='may':
        return('05')
    elif string.lower()=='jun':
        return('06')
    elif string.lower()=='jul':
        return('07')
    elif string.lower()=='aug':
        return('08')
    elif string.lower()=='sep':
        return('09')
    elif string.lower()=='oct':
        return('10')    
    elif string.lower()=='nov':
        return('11')
    elif string.lower()=='dec':
        return('12')
    else:
        return(0)


headers={
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'no-cache',
'Connection':'keep-alive',
'Cookie':'s=f912lcxbln; webp=0; device_id=ac8c5b627b0dd85a469ec02b62aba4a0; bid=52059a060047074a47353ec1117d051a_j4sbyrwa; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=3896b48d52744ac940d3169aa1c3735af58e4634; xq_a_token.sig=dSWI5hhACBemKxLJxTvBPZsm1j4; xq_r_token=210a1c6546e187874216d052d303f6a395545705; xq_r_token.sig=1ROOOx_pzUeNo9vtlC21hqMBV4I; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=4638404960; u.sig=eg9ViMeUGocmuzlXM5UIAF_U9IM; aliyungf_tc=AQAAACEh0w2G7gYAtv9F3k54OqnS412K; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1505307634,1505317009,1505400535,1505401635; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1505401719; __utma=1.1318945200.1493526591.1505317016.1505400544.43; __utmb=1.10.9.1505401719479; __utmc=1; __utmz=1.1504535903.35.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
'Host':'xueqiu.com',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3397.16 Safari/537.36',
'X-Requested-With':'XMLHttpRequest'
    }

db=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;PORT=1433;DATABASE=symbol;UID=sa;PWD=xiaotong123')
cur=db.cursor()

sqlquery="select distinct symbol,iif(exchange='Shenzhen','SZ','SH') as ex from [indexes] where [indexes]='000300'"
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
    print(ex+code,end='----')
    res=requests.get(url,headers=headers)
    res.encoding='utf-8'
    datastr=BeautifulSoup(res.text,'html.parser').text

    if len(datastr)>150:
        x=eval(datastr)
        excode=ex+code
        time=str(x[excode]['time'])[25:]+'-'+monthnum(str(x[excode]['time'])[4:7])+'-'+str(x[excode]['time'])[8:10]
        sql='''
               
        delete from [symbol_盘中] where time='%s' and symbol='%s';
                
        insert into [symbol_盘中] (update_time,symbol,name_cn,[current],pe_ttm,pe_lyr,pb,
        percentage,high52week,low52week,marketCapital,eps,beta,totalShares,net_assets,time)
        values(getdate(),'%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s')

        ''' %(
            time,
            excode,
            x[excode]['symbol'],
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
            cur.execute(sql)
            db.commit()
            print('成功')
        except:
            db.rollback()
            print('数据提取失败')
    else:
        print('股票代码不存在')
    j=j+1
print('股票信息提取完成')
try:
        cur.execute('exec [sp_fall4_盘中] ; exec [sp_fall5_盘中];')
        db.commit()
        print('Proc has done')
except:
        db.rollback()
        print('数据提取失败')
db.close()

        
