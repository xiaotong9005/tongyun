import requests
import pyodbc
from bs4 import BeautifulSoup
db=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;PORT=1433;DATABASE=symbol;UID=sa;PWD=xiaotong123')
cur=db.cursor()
headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'emstat_bc_emcount=889591589860051134; st_pvi=55363004631362; qgqp_b_id=24763416641872512753; _qddaz=QD.me2qq3.9yte39.j2t5pp7o; vjuids=4fb4adb49.15c171754db.0.e5b16a3e95f62; vjlast=1495036024.1495036024.30; _ga=GA1.2.199522707.1486901183; em_hq_fls=old; emstat_ss_emcount=7_1503438956_3351538101; Hm_lvt_557fb74c38569c2da66471446bbaea3f=1503410064; st_si=19718990691583; HAList=a-sz-002895-%u5DDD%u6052%u80A1%u4EFD%2Ca-sz-002896-%u4E2D%u5927%u529B%u5FB7%2Ca-sz-002044-%u7F8E%u5E74%u5065%u5EB7%2Ca-sh-600177-%u96C5%u6208%u5C14%2Ca-sz-000402-%u91D1%u878D%u8857%2Ca-sz-300224-%u6B63%u6D77%u78C1%u6750%2Ca-sz-002024-%u82CF%u5B81%u4E91%u5546',
    'Host':'data.eastmoney.com',
    'If-Modified-Since':'Sat, 02 Sep 2017 02:42:07 GMT',
    'Referer':'http://data.eastmoney.com/center/',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3397.16 Safari/537.36'
    }
res=requests.get('http://data.eastmoney.com/zjlx/dpzjlx.html',headers=headers)
res.encoding='gb2312'
soup=str(BeautifulSoup(res.text,'html.parser'))

str1=(soup[soup.find('DefaultJson')+12:])
str2=(str1[:str1.find(']')+1])
str3=eval((str2.replace('%','')).replace(",","','").replace("\"','\"","'],['").replace('"]',"']]").replace('["',"[['"))

for list in str3:
    date=list[0]
    zhuli=list[1]
    zhulizhanbi=list[2]
    chaodadan=list[3]
    chaodadanzhanbi=list[4]
    dadan=list[5]
    dadanzhanbi=list[6]
    zhongdan=list[7]
    zhongdanzhanbi=list[8]
    xiaodan=list[9]
    xiaodanzhanbi=list[10]
    shangzheng=list[11]
    shangzhengzhangdie=list[12]
    shenzheng=list[13]
    shenzhengzhangdie=list[14]


    
    sql='''
        declare @count int 
        select @count=count(*) from [沪深资金流向] where [交易日期]='%s'
        if @count=0 
        begin 
         insert into [dbo].[沪深资金流向] ([交易日期]
          ,[上证收盘价]
          ,[上证涨跌幅]
          ,[深证收盘价]
          ,[深证涨跌幅]
          ,[主力净流入净额]
          ,[主力净流入净占比]
          ,[超大单净流入净额]
          ,[超大单净流入净占比]
          ,[大单净流入净额]
          ,[大单净流入净占比]
          ,[中单净流入净额]
          ,[中单净流入净占比]
          ,[小单净流入净额]
          ,[小单净流入净占比])
	  values('%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
	 end
    ''' % (date,date,shangzheng,shangzhengzhangdie,shenzheng,shenzhengzhangdie,zhuli,zhulizhanbi,chaodadan,chaodadanzhanbi,dadan,dadanzhanbi,zhongdan,zhongdanzhanbi,xiaodan,xiaodanzhanbi)

    try:
        cur.execute(sql)
        db.commit()
        print(date,'数据提取成功')
    except:
        db.rollback()
        print(date,'数据提取失败')


db.close()
