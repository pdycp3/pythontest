import xlwt
newb=xlwt.Workbook(encoding='utf-8')
nws=newb.add_sheet('成绩表')
nws.write(1,2,'100')
newb.save('成绩单.xls')