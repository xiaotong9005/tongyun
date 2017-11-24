import xlrd
TC_workbook=xlrd.open_workbook(r"000001.xls")   #打开文件
first_sheet=TC_workbook.sheet_by_index(0)       #打开第一个Sheet
first_row=first_sheet.row_values(1)             #读取第二行（0是第一行）
date=xlrd.xldate.xldate_as_datetime(first_row[0],0)      #将日期列转化为datetime对象 

print(date)
