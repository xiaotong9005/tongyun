import requests
import pyodbc
import xlrd     #Excel文件操作
import os
import shutil
import time

db=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;PORT=1433;DATABASE=symbol;UID=sa;PWD=xiaotong123')
cur=db.cursor()
'''-----------------------获取指数数据文件------------------------------'''

codelist=['000925','000300','000905','000001','000016','930903','000852']


for code in codelist:
    file_url = "http://www.csindex.com.cn/uploads/file/autofile/perf/"+code+"perf.xls"
    r = requests.get(file_url) # create HTTP response object
    with open(""+code+".xls",'wb') as f:
        f.write(r.content)
        print(code,'下载完成。')


'''-----------------------读取并写入数据库------------------------------'''
for code in codelist:
    TC_workbook=xlrd.open_workbook(r""+code+".xls")   #打开文件
    first_sheet=TC_workbook.sheet_by_index(0)       #打开第一个Sheet
    first_row=first_sheet.row_values(15)             #读取第二行（0是第一行）
    date=str(xlrd.xldate.xldate_as_datetime(first_row[0],0))      #将日期列转化为datetime对象
    #print(date,first_row)
    #其中转义[涨跌幅(%)Change(%)]字段中的%需要使用%%,请注意。
    sql='''
        delete from [PriceReturnIndex]  
            where [指数代码Index Code]='%s'
            and convert(datetime,[日期Date])='%s'
        insert [PriceReturnIndex] (
	   [日期Date]
          ,[指数代码Index Code]
          ,[指数中文全称Index Chinese Name(Full)]
          ,[指数中文简称Index Chinese Name]
          ,[指数英文全称Index English Name(Full)]
          ,[指数英文简称Index English Name]
          ,[开盘Open]
          ,[最高High]
          ,[最低Low]
          ,[收盘Close]
          ,[涨跌Change]
          ,[涨跌幅(%%)Change(%%)]
          ,[成交量（股）Volume(share)]
          ,[成交金额（元）Turnover]
          ,[成分股数目Number of Cons#]
          ,[市盈率1P/E1]
          ,[市盈率2P/E2]
          ,[股息率1D/P1]
          ,[股息率2D/P2])
        values('%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,%s,'%s','%s',%s,%s,%s,%s,%s)
        '''  % (first_row[1],date,date,first_row[1]
               ,first_row[2],first_row[3],first_row[4]
               ,first_row[5],first_row[6],first_row[7]
               ,first_row[8],first_row[9],first_row[10]
               ,first_row[11],first_row[12],first_row[13]
               ,first_row[14],first_row[15],first_row[16]
               ,first_row[17],first_row[18])
    try:
        cur.execute(sql)
        db.commit()
        print(date,first_row[1],'数据提取成功,简称：',first_row[2])
    except:
        db.rollback()
        print(first_row[1],'数据提取失败,简称:',first_row[2])               
    #print (first_row)



        
'''-----------------------备份历史文件------------------------------'''

date=str((time.strftime("%y%m%d", time.localtime())))

extensions='.xls'
olddir='F:\\py\\中证官方指数行情\\'
newdir='F:\\py\\中证官方指数行情\history\\'
for code in codelist:
    try:
        os.rename(code+extensions,code+'-'+date+extensions)       #重命名
        shutil.move(olddir+code+'-'+date+extensions,newdir+code+'-'+date+extensions)#备份文件到newdir
        print(code,'转移完成')
    except IOError as err:
        print('File Error:'+str(err))   
