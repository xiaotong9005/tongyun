import requests
import pyodbc
from bs4 import BeautifulSoup

def transf(a,b):
	if a=='--':
		return(b)
	else:
		return(a)
headers={
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Cookie':'tvfe_boss_uuid=5e27e9f9701779d7; pac_uid=1_2675059005; _gscu_661903259=79824025jlu8xj64; RK=GIdvB2Bv/C; pgv_pvi=2648977408; UM_distinctid=15cd7d528361a5-0902ce33389b2a-3715834-100200-15cd7d52837ef; ts_uid=8007293614; ts_refer=www.baidu.com/link; ts_uid=8007293614; RECENT_CODE=000737_51%7C603129_1%7C164906_51%7C161219_51%7C160716_51%7C000876_51%7C601857_1%7C600104_1%7C000988_0%7C000193_0%7C100022_0%7C001781_0%7C165521_0%7C162214_0%7C000898_51%7C399550_51%7C070032_0%7C001852_0%7C000969_0%7C001728_0%7C150276_51%7C16181L_0; dm_login_weixin_rem=; dm_login_weixin_scan=; logout_page=; ptcz=5c8223be0ba5004c0268b6238147a7e3d5e2dcfcac5d1662006b9feecc402eba; pt2gguin=o2675059005; mbCardUserNotLoginTips=1; pgv_info=ssid=s8630159920; pgv_pvid=7066792342; o_cookie=2675059005',
        'Host':'stock.finance.qq.com',
        'Referer':'http://stockhtm.finance.qq.com/fund/jzzx/index.htm',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3397.16 Safari/537.36'
       }
db=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;PORT=1433;DATABASE=symbol;UID=sa;PWD=xiaotong123')
cur=db.cursor()
datelist=[]
qsql="select [dateid] from [symbol].[dbo].[date] where dateid<='20150530'"
try:
        cur.execute(qsql)
        results=cur.fetchall()
        for row in results:
                datelist.append(row[0])

except:
        print('DateList获取失败')
for i in datelist:
        url="http://stock.finance.qq.com/cgi-bin/fund/jzzx_d?fm=js&d="+i+""
        #print(url,end='...')
        res=requests.get(url,headers=headers)
        datastr=BeautifulSoup(res.text,'html.parser').text
        a=datastr.find('var v_kfs=')+len('var v_kfs=')#字符串开头无用的字符开始位置
        c=datastr.find(';/*')#字符串结束无用的字符开始位置
        datastr=eval(datastr[a:c])
        
        num=1

        for code in datastr:
                #print(num,end=' ')
                if code[0]in ('001275'):#提取之针对某个基金
                        sql='''
                        declare @count int 
                        select @count=count(*)
                          from [基金净值中心_HIS]
                        where [基金代码]='%s'
                        and [净值日期]='%s'
                        if @count=0 
                        begin 
                                insert into [基金净值中心_HIS] ([基金代码],[简称],[单位净值],[涨跌],[增长率],[累计净值],[净值日期])
                                values('%s','%s',%s,%s,%s,%s,'%s')
                        end 
                        '''%(code[0],code[6],code[0],code[1],transf(code[2],0),transf(code[3],0),transf(code[4],0),transf(code[5],0),code[6])
                        try:
                            cur.execute(sql)
                            db.commit()
                            print(code[0],code[6],'数据提取成功,简称:',code[1])
                        except:
                            db.rollback()
                            print(code[0],'数据提取失败,简称:',code[1])
                        num=num+1                    
                        
db.close()
