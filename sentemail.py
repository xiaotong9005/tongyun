import smtplib  
from email.mime.text import MIMEText  
from email.header import Header
import pyodbc
from datetime import datetime

dayOfWeek = datetime.now().weekday()        
if dayOfWeek==0 or dayOfWeek==1 or dayOfWeek==2 or dayOfWeek==3 or dayOfWeek==4 or dayOfWeek==5:


    db=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;PORT=1433;DATABASE=symbol;UID=sa;PWD=xiaotong123')
    cur=db.cursor()

    sqlquery='''
        select [performance] from [v_performance]
        where performance not like '%跌势持续1天%'
        and symbol in('SH000170','SH000905','SH501029','SH000925','SH000300')
        '''
    msglist=[]
    try:
        cur.execute(sqlquery)
        results=cur.fetchall()
        for row in results:
            msglist.append(row[0])
    except:
        print('MsgList获取失败')

    if len(msglist)==0:
        msg='Everything goes well.'
    else:
        msg=';\n'.join(msglist)

     
    smtpserver = 'smtp.exmail.qq.com'  
    username = 'xiaotong.xu@analyticservice.net'  
    password = 'Aas2017'  
    sender = 'xiaotong.xu@analyticservice.net'  
    receiver = ['2675059005@qq.com']

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
