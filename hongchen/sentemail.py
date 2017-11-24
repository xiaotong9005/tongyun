import smtplib
from email.mime.text import MIMEText  
from email.header import Header
import pyodbc
from datetime import datetime

dayOfWeek = datetime.now().weekday()
if dayOfWeek==0 or dayOfWeek==1 or dayOfWeek==2 or dayOfWeek==3 or dayOfWeek==4 or dayOfWeek==5 or dayOfWeek==6:


    db=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;PORT=1433;DATABASE=symbol;UID=sa;PWD=xiaotong123')
    cur=db.cursor()

    sqlquery='''
	select right('0'+concat(ROW_NUMBER() over(order by [status],symbol),'.'),3) as id,* from (
	select [date],'连跌4天后第5天的状态' as remarks,f.[symbol],s.name_cn,[status]
        from [fall4] as f
        left join (select distinct 
			iif(exchange='shenzhen','sz','sh')+symbol as symbol,
		 [name_cn] from [indexes]) as s 
        on s.symbol=f.symbol
        where date =convert(date,getdate())
        union all
        select [date],'连跌5天后第6天的状态' as remarks,f.[symbol],s.name_cn,[status]
        from [fall5] as f
        left join (select distinct 
			iif(exchange='shenzhen','sz','sh')+symbol as symbol,
		 [name_cn] from [indexes]) as s 
        on s.symbol=f.symbol
        where date =convert(date,getdate())
	) as t
        order by status,symbol
    '''
    msglist=[]
    try:
        cur.execute(sqlquery)
        results=cur.fetchall()
        for row in results:
            msglist.append(row[0])
            msglist.append(row[1])
            msglist.append(row[2])
            msglist.append(row[3])
            msglist.append(row[4])
            msglist.append(row[5])
            msglist.append('\n')
    except:
        print('MsgList获取失败')
    msg="     #      交易日              说明                           证券代码      中文名称    状态    （数据为14:30的盘中数据）\n"+"    ".join(msglist)

  
    smtpserver = 'smtp.exmail.qq.com'  
    username = 'xiaotong.xu@analyticservice.net'  
    password = 'Aas2017'  
    sender = 'xiaotong.xu@analyticservice.net'  
    receiver = ['1215548085@qq.com','2675059005@qq.com']

    subject = 'quotations'
    context=msg

    msg =MIMEText(context, 'plain', 'utf-8')#中文需参数‘utf-8’，单字节字符不需要  
    msg['Subject'] = Header(subject, 'utf-8')  
    msg['From'] = Header('xiaotong', 'utf-8')
    try:  
        smtp = smtplib.SMTP()  
        smtp.connect('smtp.exmail.qq.com')  
        smtp.login(username, password)  
        smtp.sendmail(sender, receiver, msg.as_string())
        print("发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")
    smtp.quit()  
     
else:
    print('非工作日，我也要休息了')

