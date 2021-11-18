import xlwt
for m in range(1,13):
    wb=xlwt.Workbook(encoding='utf-8')
    wb.add_sheet('统计表')
    wb.save('%d月.xls'%m)