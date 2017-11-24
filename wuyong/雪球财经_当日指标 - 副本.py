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
    if string.lower()=='aug':
        return('08')
    elif string.lower()=='sep':
        return('09')
    else:
        return(0)

if strftime("%H:%M")>'15:05' or strftime("%H:%M")<'08:00':
        headers={
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Cookie':'s=f912lcxbln; webp=0; device_id=ac8c5b627b0dd85a469ec02b62aba4a0; bid=52059a060047074a47353ec1117d051a_j4sbyrwa; xq_a_token=45fd777f51337c7a4673f1f5a14b63c417bf8b07; xqat=45fd777f51337c7a4673f1f5a14b63c417bf8b07; xq_r_token=a09e0b1f8f26eb4cc6153cc169d2466c83f24126; u=4638404960; xq_token_expire=Mon%20Aug%2028%202017%2023%3A34%3A55%20GMT%2B0800%20(CST); aliyungf_tc=AQAAAG3VuTeugQ0AzNSutK6WTHg+zLEH; xq_is_login=1; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1502202716,1502459709,1502460446,1502594602; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1502594640; __utma=1.1318945200.1493526591.1502460458.1502594608.24; __utmb=1.6.9.1502594640427; __utmc=1; __utmz=1.1501766009.16.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        'Host':'xueqiu.com',
        'Referer':'https://xueqiu.com/S/SZ000625',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3228.1 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
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
                #delsql="delete from [symbol] where time='"+time+"' and symbol='"+excode+"';" 
                sql='''
                declare @count int
                select @count=count(*) from [symbol] where time='%s' and symbol='%s';
                if @count=0 
                begin
                insert into symbol (update_time,symbol,name_cn,[current],pe_ttm,pe_lyr,pb,
                percentage,high52week,low52week,marketCapital,eps,beta,totalShares,net_assets,time)
                values(getdate(),'%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s')
                end
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
                    print('数据提取成功')
                except:
                    db.rollback()
                    print('数据提取失败')
            else:
                print('股票代码不存在')
            j=j+1
        db.close()
else:
        print('此时更新数据不一定准确哦。')

        
