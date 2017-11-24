import requests
import pymysql
from bs4 import BeautifulSoup

def isblank(a,b):
	if len(a)<1:
		return(b)
	else:
		return(a)

db=pymysql.connect('localhost','root','xiaotong123','indexes',charset='utf8')
cur=db.cursor()

#sqlquery="select distinct s_code,if(exchange like '%hanghai%','sh',if(exchange like '%henzhen%','sz',exchange)) as ex from indexes"
sqlquery="select distinct s_code,if(exchange like '%hanghai%','sh',if(exchange like '%henzhen%','sz',exchange)) as ex from indexes where exchange is not null union  select distinct s_code,'sz' as ex from indexes where exchange is null union select distinct s_code,'sh' as ex from indexes"
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
    ex=exchange[j]
    code=codelist[j]
    headers={  
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'cache-control':'no-cache',
    'Connection':'keep-alive',
    'Cookie':'aliyungf_tc=AQAAAFNfvW+OGwMAB25Vcs52HlxDIra0; xq_a_token=82d9cefaa0793743cb186e53294ec0e61ac2abec; xq_a_token.sig=5N1bqGL6dBOdtpsJHPbhJk4l6_g; xq_r_token=11b86433a20d1d1eef63ecc12252297196a20e10; xq_r_token.sig=RPGspgHiNeURBrDthhch0e5_T0g; u=331500807840275; device_id=923502187b8a828f8a283f9134b3ea5d; s=gd12owoxky; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1500807845; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1500810074; __utma=1.1358685580.1500807993.1500807993.1500807993.1; __utmb=1.7.10.1500807993; __utmc=1; __utmz=1.1500807993.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'Host':'xueqiu.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
    }
    
    url='https://xueqiu.com/v4/stock/quote.json?code='+ex+code
    print(url,end='----')
    res=requests.get(url,headers=headers)
    res.encoding='utf-8'
    datastr=BeautifulSoup(res.text,'html.parser').text
    
    if len(datastr)>150:#存在该股票代码
        symbol_start=datastr.find('symbol')+len('symbol---');   len_symbol=str(datastr[symbol_start:]).find('"');   symbol=datastr[symbol_start:symbol_start+len_symbol]
        current_start=datastr.find('current')+len('current---');   len_current=str(datastr[current_start:]).find('"');   current=datastr[current_start:current_start+len_current]        
        pe_ttm_start=datastr.find('pe_ttm')+len('pe_ttm---');   len_pe_ttm=str(datastr[pe_ttm_start:]).find('"');   pre_pe_ttm=datastr[pe_ttm_start:pe_ttm_start+len_pe_ttm];  pe_ttm=isblank(pre_pe_ttm,'0');
        pe_lyr_start=datastr.find('pe_lyr')+len('pe_lyr---');   len_pe_lyr=str(datastr[pe_lyr_start:]).find('"');   pre_pe_lyr=datastr[pe_lyr_start:pe_lyr_start+len_pe_lyr]; pe_lyr=isblank(pre_pe_lyr,'0')
        pb_start=datastr.find('pb')+len('pb---');   len_pb=str(datastr[pb_start:]).find('"');   pb=datastr[pb_start:pb_start+len_pb]
        percentage_start=datastr.find('percentage')+len('percentage---');   len_percentage=str(datastr[percentage_start:]).find('"');   percentage=datastr[percentage_start:percentage_start+len_percentage]
        high52week_start=datastr.find('high52week')+len('high52week---');   len_high52week=str(datastr[high52week_start:]).find('"');   high52week=datastr[high52week_start:high52week_start+len_high52week]
        low52week_start=datastr.find('low52week')+len('low52week---');   len_low52week=str(datastr[low52week_start:]).find('"');   low52week=datastr[low52week_start:low52week_start+len_low52week]
        marketCapital_start=datastr.find('marketCapital')+len('marketCapital---');   len_marketCapital=str(datastr[marketCapital_start:]).find('"');   marketCapital=float(datastr[marketCapital_start:marketCapital_start+len_marketCapital])
        eps_start=datastr.find('eps')+len('eps---');   len_eps=str(datastr[eps_start:]).find('"');   eps=datastr[eps_start:eps_start+len_eps]
        beta_start=datastr.find('beta')+len('beta---');   len_beta=str(datastr[beta_start:]).find('"');   beta=datastr[beta_start:beta_start+len_beta]
        totalShares_start=datastr.find('totalShares')+len('totalShares---');   len_totalShares=str(datastr[totalShares_start:]).find('"');   totalShares=float(datastr[totalShares_start:totalShares_start+len_totalShares])
        time_start=datastr.find('time')+len('time---');   len_time=str(datastr[time_start:]).find('"');   time=datastr[time_start:time_start+len_time]
        net_assets_start=datastr.find('net_assets')+len('net_assets---');   len_net_assets=str(datastr[net_assets_start:]).find('"');   net_assets=datastr[net_assets_start:net_assets_start+len_net_assets]
        name_start=datastr.find('name')+len('name---');   len_name=str(datastr[name_start:]).find('"');   name_cn=datastr[name_start:name_start+len_name]

        sql="insert into symbol (update_time,symbol,name_cn,current,pe_ttm,pe_lyr,pb,percentage,high52week,low52week,marketCapital,eps,beta,totalShares,net_assets,time) values(now(),'%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s')" %(symbol,name_cn,current,pe_ttm,pe_lyr,pb,percentage,high52week,low52week,marketCapital,eps,beta,totalShares,net_assets,time)
        
        try:
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
