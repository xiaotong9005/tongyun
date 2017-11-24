import requests
import pyodbc
import xlrd     #Excel文件操作

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
print(len(codelist))

'''-----------------------读取并写入数据库------------------------------'''
for code in codelist:
    TC_workbook=xlrd.open_workbook(r""+code+".xls")   #打开文件
    first_sheet=TC_workbook.sheet_by_index(0)       #打开第一个Sheet
    first_row=first_sheet.row_values(1)             #读取第二行（0是第一行）
    date=xlrd.xldate.xldate_as_datetime(first_row[0],0)      #将日期列转化为datetime对象
    sql='''
        delete from [PriceReturnIndex]
            where [指数代码Index Code]='%s'
            and convert(datetime,[日期Date])='%s';
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
          ,[涨跌幅(%)Change(%)]
          ,[成交量（股）Volume(share)]
          ,[成交金额（元）Turnover]
          ,[成分股数目Number of Cons#]
          ,[市盈率1P/E1]
          ,[市盈率2P/E2]
          ,[股息率1D/P1]
          ,[股息率2D/P2])
        values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')

        '''%(code[1],code[0],code[0],code[1],code[2],code[3],code[4],code[5],code[6],code[7],code[8],code[9],code[10],code[11],code[12],code[13],code[14],code[15],code[16],code[17],code[18])
    try:
        cur.execute(sql)
        db.commit()
        print(code[0],code[1],'数据提取成功,简称:',code[1])
    except:
        db.rollback()
        print(code[1],'数据提取失败,简称:',code[1])               
    print (first_row)



        
'''-----------------------备份历史文件------------------------------'''
