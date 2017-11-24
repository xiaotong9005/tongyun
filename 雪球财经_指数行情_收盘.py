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


if strftime("%H:%M")<'8:30' or strftime("%H:%M")>'15:01':
        headers={
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Cookie':'device_id=d9386e7d5baba9d2a4c917754d3c0f41; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=533ee92f6b8c235e8c4a616942a644ed228f9143; xq_a_token.sig=P7m6dJXADGBCqVKrLs2wpMjy_uQ; xq_r_token=7504c3605b03433d12104e983e35b826ad5b099b; xq_r_token.sig=S1zJtwESNRpJ6tgAW_QNhKKbFgI; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=4638404960; u.sig=eg9ViMeUGocmuzlXM5UIAF_U9IM; s=f312jmpyty; bid=52059a060047074a47353ec1117d051a_ja7sfsjh; aliyungf_tc=AQAAACY4lw3QFwoAMZv0ZbdRtmiF1aao; isPast=true; isPast.sig=Q1zWad3glPfOy3Ye-506BMax-a0; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1511156932,1511189526; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1511189542; __utma=1.600829631.1511157314.1511157314.1511189530.2; __utmb=1.2.10.1511189530; __utmc=1; __utmz=1.1511157314.1.1.utmcsr=xueqiu.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        'Host':'xueqiu.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'            }

        db=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;PORT=1433;DATABASE=symbol;UID=sa;PWD=xiaotong123')
        cur=db.cursor()

        sqlquery="select [icode] from [大盘指数主数据]"
        codelist=[]
        try:
            cur.execute(sqlquery)
            results=cur.fetchall()
            for row in results:
                codelist.append(row[0])
        except:
            print('CodeList获取失败')
        j=0    
        for code in codelist:
            print(j+1,end=':')

            url='https://xueqiu.com/v4/stock/quote.json?code='+code
            print(code,end='----')
            res=requests.get(url,headers=headers)
            res.encoding='utf-8'
            datastr=BeautifulSoup(res.text,'html.parser').text

            if len(datastr)>150:
                x=eval(datastr)
                time=str(x[code]['time'])[25:]+'-'+monthnum(str(x[code]['time'])[4:7])+'-'+str(x[code]['time'])[8:10]
                sql='''
                declare @count int
                select @count=count(*) from [大盘指数行情中心_收盘] where time='%s' and symbol='%s';
                if @count=0 
                begin
                insert into [大盘指数行情中心_收盘] (update_time,symbol,name_cn,[current],pe_ttm,pe_lyr,pb,
                percentage,high52week,low52week,marketCapital,eps,beta,totalShares,net_assets,time)
                values(getdate(),'%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s')
                end
                ''' %(
                  time,
                  code,
                  x[code]['symbol'],
                  x[code]['name'],
                  isblank(x[code]['current'],0),
                  isblank(x[code]['pe_ttm'],0),
                  isblank(x[code]['pe_lyr'],0),
                  isblank(x[code]['pb'],0),
                  isblank(x[code]['percentage'],0),
                  isblank(x[code]['high52week'],0),
                  isblank(x[code]['low52week'],0),
                  isblank(x[code]['marketCapital'],0),
                  isblank(x[code]['eps'],0),
                  isblank(x[code]['beta'],0),
                  isblank(x[code]['totalShares'],0),
                  isblank(x[code]['net_assets'],0),
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
        
        db.close()
else:
        print('这个时候不该更新这部分数据，滚蛋吧。')

        
