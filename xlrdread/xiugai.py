import xlrd
from xlutils.copy import copy
wb=xlrd.open_workbook('work.xls')
nwb=copy(wb)
nws1=nwb.add_sheet('上海分校')
nws2=nwb.get_sheet(1)
nws3=nwb.get_sheet('数字表')
nws3.write(30,2,'thhthth')
nwb.save('newwork.xls')