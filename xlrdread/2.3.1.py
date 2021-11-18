import xlrd #导入模块
wb=xlrd.open_workbook('work.xls') #读取工作簿
ws=wb.sheets() #读取所有工作表
wsname=wb.sheet_names() #读取所有工作表name
ws1=wb.sheet_by_name('数字表') #通过名称获取工作表
ws2=wb.sheet_by_index(1) #通过index获取工作表
ws3=wb.sheets()[0]   #通过序号获取工作表
print(ws3)
print(ws2)
print(ws1)
print(wsname)